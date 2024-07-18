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
    # (|00> + |11>) / sqrt(2)
    Bell_state_Z = QuantumState.from_label((Z0 + Z0), (Z1 + Z1))
    # (|++> + |-->) / sqrt(2)
    Bell_state_X = QuantumState.from_label((X0 + X0), (X1 + X1))

    expected_state_data = np.array([0.70710678 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.70710678 + 0.0j])
    assert np.allclose(Bell_state_Z.data, expected_state_data, atol=ABS_TOL)
    assert np.allclose(Bell_state_X.data, expected_state_data, atol=ABS_TOL)

    # (|0+> + |1->) / sqrt(2)
    graph_state = QuantumState.from_label((Z0 + X0), (Z1 + X1))

    expected_state_data = np.array([0.5 + 0.0j, 0.5 + 0.0j, 0.5 + 0.0j, -0.5 + 0.0j])
    assert np.allclose(graph_state.data, expected_state_data, atol=ABS_TOL)

    # (|0i> + |1j>) / sqrt(2)
    state = QuantumState.from_label((Z0 + Y0), (Z1 + Y1))

    expected_state_data = np.array([0.5 + 0.0j, 0.0 + 0.5j, 0.5 + 0.0j, 0.0 - 0.5j])
    assert np.allclose(state.data, expected_state_data, atol=ABS_TOL)


def test_entropy():
    # |000>
    state = QuantumState.from_label(Z0 * 3)
    assert math.isclose(state.entropy(), 0.0, abs_tol=ABS_TOL)

    # |0+0> + |0-0>
    stateZXZ = state._basis_convert("-x-")[0]
    assert math.isclose(stateZXZ.entropy(), 1.0, abs_tol=ABS_TOL)

    # |r0r> + |r0l> + |l0r> + |l0l>
    stateYZY = state._basis_convert("y-y")[0]
    assert math.isclose(stateYZY.entropy(), 2.0, abs_tol=ABS_TOL)

    # |000>
    stateZZZ = state._basis_convert("")[0]
    assert math.isclose(stateZZZ.entropy(), 0.0, abs_tol=ABS_TOL)


def test_to_matrix():
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

    # |j>
    test_state_vector = QuantumState.from_label(Y1).to_matrix().squeeze()
    expect_state_vector = np.array([1 + 0j, 0 - 1j]) / math.sqrt(2)

    # |0i> + |1j>
    test_state_vector = QuantumState.from_label(Z0 + Y0, Z1 + Y1).to_matrix().squeeze()
    expect_state_vector = np.array([1 + 0j, 0 + 1j, 1 + 0j, 0 - 1j]) / 2
