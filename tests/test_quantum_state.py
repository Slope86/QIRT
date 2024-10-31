import math

import numpy as np
from numpy.typing import NDArray

from QIRT import QuantumState
from QIRT.utils import Ket

ABS_TOL = 1e-15  # absolute tolerance for close comparisons

Z0 = Ket.z0
Z1 = Ket.z1
X0 = Ket.x0
X1 = Ket.x1
Y0 = Ket.y0
Y1 = Ket.y1


def test_from_label():
    """Test the creation of a quantum state from a label."""
    # (|00> + |11>) / sqrt(2)
    bell_state_z = QuantumState.from_label((Z0 + Z0), (Z1 + Z1))
    # (|++> + |-->) / sqrt(2)
    bell_state_x = QuantumState.from_label((X0 + X0), (X1 + X1))

    expected_state_data = np.array([0.70710678 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.70710678 + 0.0j])
    assert np.allclose(bell_state_z.data, expected_state_data, atol=ABS_TOL)
    assert np.allclose(bell_state_x.data, expected_state_data, atol=ABS_TOL)

    # (|0+> + |1->) / sqrt(2)
    graph_state = QuantumState.from_label((Z0 + X0), (Z1 + X1))

    expected_state_data = np.array([0.5 + 0.0j, 0.5 + 0.0j, 0.5 + 0.0j, -0.5 + 0.0j])
    assert np.allclose(graph_state.data, expected_state_data, atol=ABS_TOL)

    # (|0i> + |1j>) / sqrt(2)
    state = QuantumState.from_label((Z0 + Y0), (Z1 + Y1))

    expected_state_data = np.array([0.5 + 0.0j, 0.0 + 0.5j, 0.5 + 0.0j, 0.0 - 0.5j])
    assert np.allclose(state.data, expected_state_data, atol=ABS_TOL)


def test_entropy():
    """Test the calculation of the entropy of a quantum state."""
    # |000>
    state = QuantumState.from_label(Z0 * 3)
    assert math.isclose(state.entropy(), 0.0, abs_tol=ABS_TOL)

    # |0+0> + |0-0>
    state_zxz = state._basis_convert("-x-")[0]
    assert math.isclose(state_zxz.entropy(), 1.0, abs_tol=ABS_TOL)

    # |r0r> + |r0l> + |l0r> + |l0l>
    state_yzy = state._basis_convert("y-y")[0]
    assert math.isclose(state_yzy.entropy(), 2.0, abs_tol=ABS_TOL)

    # |000>
    state_zzz = state._basis_convert("")[0]
    assert math.isclose(state_zzz.entropy(), 0.0, abs_tol=ABS_TOL)


def test_to_matrix():
    """Test the conversion of a quantum state to a matrix."""
    test_state_vector: NDArray
    expect_state_vector: NDArray

    # |000>
    test_state_vector = QuantumState.from_label(Z0 * 3).to_matrix().squeeze()
    expect_state_vector = np.array([1, 0, 0, 0, 0, 0, 0, 0])
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)

    # |01>
    test_state_vector = QuantumState.from_label(Z0 + Z1).to_matrix().squeeze()
    expect_state_vector = np.array([0, 1, 0, 0])
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)

    # |0+>
    test_state_vector = QuantumState.from_label(Z0 + X0).to_matrix().squeeze()
    expect_state_vector = np.array([1, 1, 0, 0]) / math.sqrt(2)
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)

    # |0->
    test_state_vector = QuantumState.from_label(Z0 + X1).to_matrix().squeeze()
    expect_state_vector = np.array([1, -1, 0, 0]) / math.sqrt(2)
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)

    # |1+>
    test_state_vector = QuantumState.from_label(Z1 + X0).to_matrix().squeeze()
    expect_state_vector = np.array([0, 0, 1, 1]) / math.sqrt(2)
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)

    # |1->
    test_state_vector = QuantumState.from_label(Z1 + X1).to_matrix().squeeze()
    expect_state_vector = np.array([0, 0, 1, -1]) / math.sqrt(2)
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)

    # |0++> + |1-->
    test_state_vector = QuantumState.from_label(Z0 + X0 + X0, Z1 + X1 + X1).to_matrix().squeeze()
    expect_state_vector = np.array([1, 1, 1, 1, 1, -1, -1, 1]) / math.sqrt(8)
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)

    # |i>
    test_state_vector = QuantumState.from_label(Y0).to_matrix().squeeze()
    expect_state_vector = np.array([1 + 0j, 0 + 1j]) / math.sqrt(2)
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)

    # |j>
    test_state_vector = QuantumState.from_label(Y1).to_matrix().squeeze()
    expect_state_vector = np.array([1 + 0j, 0 - 1j]) / math.sqrt(2)
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)

    # |0i> + |1j>
    test_state_vector = QuantumState.from_label(Z0 + Y0, Z1 + Y1).to_matrix().squeeze()
    expect_state_vector = np.array([1 + 0j, 0 + 1j, 1 + 0j, 0 - 1j]) / 2
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)


def test_state_after_measurement():
    """Test measuring method."""
    # |000> + |1-->
    state = QuantumState.from_label(Z0 * 3, Z1 + X1 * 2)

    # Measure the first qubit in the Z basis
    result_state_list = state.state_after_measurement(measure_bit=[0], target_basis="z--")

    # |0>: |000>
    test_state_vector = result_state_list[0].to_matrix().squeeze()
    expect_state_vector = np.array([1, 0, 0, 0, 0, 0, 0, 0])
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)

    # |1>: |1-->
    test_state_vector = result_state_list[1].to_matrix().squeeze()
    expect_state_vector = np.array(
        [0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.5 + 0.0j, -0.5 + 0.0j, -0.5 + 0.0j, 0.5 + 0.0j]
    )
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)

    # |+->
    state = QuantumState.from_label(X0 + X1)

    # Measure the first qubit in the X basis
    result_state_list = state.state_after_measurement(measure_bit=[0], target_basis="x-")

    # |+>: |+->
    test_state_vector = result_state_list[0].to_matrix().squeeze()
    expect_state_vector = np.array([ 0.5+0.j, -0.5+0.j,  0.5+0.j, -0.5+0.j])
    assert np.allclose(test_state_vector, expect_state_vector, atol=ABS_TOL)

    # |->: None
    assert result_state_list[1] is None
