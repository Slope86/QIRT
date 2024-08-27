r"""Module to extend Qiskit's QuantumCircuit with additional functionalities.

This module provides an extended version of Qiskit's QuantumCircuit class, adding
methods for basis conversion and visualization in matrix form. The extended class,
QuantumCircuit, includes methods to convert the basis of qubits and to generate
a LaTeX representation of the quantum circuit.

The functionalities added in this module are:

- Conversion of the quantum circuit to a matrix form.
- Drawing the quantum circuit or its matrix representation.
- Adding gates to convert qubits from one basis to another.
- Applying unitary matrices to specified qubits.

See Also:
    [Qiskit QuantumCircuit documentation](https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.html)
"""

from __future__ import annotations

import typing
from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray
from qiskit import QuantumCircuit as QiskitQC
from qiskit import quantum_info
from qiskit.circuit.parameterexpression import ParameterExpression
from qiskit.circuit.quantumcircuit import QubitSpecifier

from QIRT import latex_drawer
from QIRT.utils import inverse_tensor

if typing.TYPE_CHECKING:
    from qiskit.quantum_info import Statevector

    from QIRT import QuantumState


class QuantumCircuit:
    """An extended class of QuantumCircuit from Qiskit.

    This class extends the QuantumCircuit class from Qiskit to provide additional
    functionalities for converting basis and visualizing the quantum circuit in
    matrix form.

    See Also:
        [Qiskit QuantumCircuit documentation](https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.html)
    """

    def __init__(self, *args, **kwargs):
        """Initialize the QuantumCircuit class."""
        self._qiskit_qc = QiskitQC(*args, **kwargs)

    def to_matrix(self) -> NDArray[np.complex128]:
        """Return matrix form of the quantum circuit as a numpy array.

        This method returns the matrix representation of the quantum circuit by
        reversing the order of qubits to match textbook notation.

        Returns:
            NDArray[np.complex128]: The matrix representation of the quantum circuit.
        """
        reverse_qc = self._qiskit_qc.reverse_bits()  # REVERSE the order of qubits to match textbook notation
        return np.asarray(quantum_info.Operator(reverse_qc).data, dtype=np.complex128)

    def draw(self, output: str | None = "mpl", source: bool = False, *args, **kwargs):
        r"""Draw the quantum circuit, or show its matrix form if output is 'matrix'.

        Args:
            output (str | None, optional): The output format for drawing the circuit.
                If 'text', generates ASCII art TextDrawing that can be printed in the console.
                If 'mpl', generates images with color rendered purely in Python using matplotlib.
                If 'latex', generates high-quality images compiled via latex.
                If 'matrix', shows the matrix form of the circuit. Defaults to "mpl".
            source (bool, optional): Whether to return the latex source code for the visualization. Defaults to False.
            *args: Additional positional arguments to pass to the draw method.
            **kwargs: Additional keyword arguments to pass to the draw method.

        Returns:
            The drawn circuit in the specified format.
        """
        match output:
            case "matrix":
                return latex_drawer.matrix_to_latex(self.to_matrix(), source=source)
            case "latex":
                if source:
                    return self._qiskit_qc.draw(output="latex_source", *args, **kwargs)
                return self._qiskit_qc.draw(output="latex", *args, **kwargs)
            case _:
                return self._qiskit_qc.draw(output=output, *args, **kwargs)

    def _xyz_convert_circ(self, target_basis: str, current_basis: str, qubit_index: int) -> QuantumCircuit:
        """Add the corresponding gate that converts different basis.

        This method adds the appropriate gates to the circuit to convert a qubit
        from the current basis to the target basis.

        Args:
            target_basis (str): The target basis to convert to.
            current_basis (str): The current basis of the qubit.
            qubit_index (int): The index of the qubit to be converted.
        """
        if current_basis == target_basis:
            return self
        current_basis += target_basis
        match current_basis:
            case "zx" | "xz":
                self._qiskit_qc.h(qubit_index)
            case "zy":
                self._qiskit_qc.sdg(qubit_index)
                self._qiskit_qc.h(qubit_index)
            case "yz":
                self._qiskit_qc.h(qubit_index)
                self._qiskit_qc.s(qubit_index)
            case "xy":
                self._qiskit_qc.h(qubit_index)
                self._qiskit_qc.sdg(qubit_index)
                self._qiskit_qc.h(qubit_index)
            case "yx":
                self._qiskit_qc.h(qubit_index)
                self._qiskit_qc.s(qubit_index)
                self._qiskit_qc.h(qubit_index)
        return self

    def unitary(
        self,
        matrix: NDArray[np.complex128] | list[list[int]],
        qubits: Sequence[QubitSpecifier],
        label: str | None = None,
    ) -> QuantumCircuit:
        """Apply a unitary matrix to specified qubits.

        This method applies a given unitary matrix to the specified qubits in the
        quantum circuit. The matrix is converted to match the qubit order of the
        quantum circuit by reversing the order of qubits.

        Args:
            matrix (NDArray[np.complex128] | list[list[int]]): The unitary matrix to apply.
            qubits (Sequence[QubitSpecifier]): The qubits to which the unitary matrix will be applied.
            label (str | None, optional): An optional label for the unitary gate. Defaults to None.

        Returns:
            QuantumCircuit: Quantum circuit with the applied unitary matrix.
        """
        matrix = np.asarray(matrix, dtype=np.complex128)
        matrix = inverse_tensor(matrix)  # REVERSE the order of qubits to match textbook notation
        self._qiskit_qc.unitary(matrix, qubits, label=label)
        return self

    # --------------------------------------------------------------------
    # The following methods are copied from Qiskit's QuantumCircuit class.
    # --------------------------------------------------------------------

    def barrier(self, *qargs: QubitSpecifier, label=None) -> QuantumCircuit:
        """Apply :class:`~.library.Barrier`.

        If ``qargs`` is empty, applies to all qubits
        in the circuit.

        Args:
            qargs (QubitSpecifier): Specification for one or more qubit arguments.
            label (str): The string label of the barrier.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.barrier(*qargs, label=label)
        return self

    def delay(
        self,
        duration: float | int | ParameterExpression,
        qarg: QubitSpecifier | None = None,
        unit: str = "dt",
    ) -> QuantumCircuit:
        """Apply :class:`~.circuit.Delay`.

        If qarg is ``None``, applies to all qubits.
        When applying to multiple qubits, delays with the same duration will be created.

        Args:
            duration (int or float or ParameterExpression): duration of the delay.
            qarg (Object): qubit argument to apply this delay.
            unit (str): unit of the duration. Supported units: ``'s'``, ``'ms'``, ``'us'``,
                ``'ns'``, ``'ps'``, and ``'dt'``. Default is ``'dt'``, i.e. integer time unit
                depending on the target backend.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.

        Raises:
            CircuitError: if arguments have bad format.
        """
        self._qiskit_qc.delay(duration, qarg=qarg, unit=unit)
        return self

    def h(self, qubit: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.HGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.h(qubit)
        return self

    def ch(
        self,
        control_qubit: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.CHGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubit: The qubit(s) used as the control.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.ch(control_qubit, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def id(self, qubit: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.IGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.id(qubit)
        return self

    def ms(self, theta: ParameterExpression | float, qubits: Sequence[QubitSpecifier]) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.MSGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The angle of the rotation.
            qubits: The qubits to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.ms(theta, qubits)
        return self

    def p(self, theta: ParameterExpression | float, qubit: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.PhaseGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: THe angle of the rotation.
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.p(theta, qubit)
        return self

    def cp(
        self,
        theta: ParameterExpression | float,
        control_qubit: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.CPhaseGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The angle of the rotation.
            control_qubit: The qubit(s) used as the control.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.cp(theta, control_qubit, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def mcp(
        self,
        lam: ParameterExpression | float,
        control_qubits: Sequence[QubitSpecifier],
        target_qubit: QubitSpecifier,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.MCPhaseGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            lam: The angle of the rotation.
            control_qubits: The qubits used as the controls.
            target_qubit: The qubit(s) targeted by the gate.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.mcp(lam, control_qubits, target_qubit, ctrl_state=ctrl_state)
        return self

    def r(
        self, theta: ParameterExpression | float, phi: ParameterExpression | float, qubit: QubitSpecifier
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.RGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The angle of the rotation.
            phi: The angle of the axis of rotation in the x-y plane.
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.r(theta, phi, qubit)
        return self

    def rv(
        self,
        vx: ParameterExpression | float,
        vy: ParameterExpression | float,
        vz: ParameterExpression | float,
        qubit: QubitSpecifier,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.RVGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Rotation around an arbitrary rotation axis :math:`v`, where :math:`|v|` is the angle of
        rotation in radians.

        Args:
            vx: x-component of the rotation axis.
            vy: y-component of the rotation axis.
            vz: z-component of the rotation axis.
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.rv(vx, vy, vz, qubit)
        return self

    def rccx(
        self,
        control_qubit1: QubitSpecifier,
        control_qubit2: QubitSpecifier,
        target_qubit: QubitSpecifier,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.RCCXGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubit1: The qubit(s) used as the first control.
            control_qubit2: The qubit(s) used as the second control.
            target_qubit: The qubit(s) targeted by the gate.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.rccx(control_qubit1, control_qubit2, target_qubit)
        return self

    def rcccx(
        self,
        control_qubit1: QubitSpecifier,
        control_qubit2: QubitSpecifier,
        control_qubit3: QubitSpecifier,
        target_qubit: QubitSpecifier,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.RC3XGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubit1: The qubit(s) used as the first control.
            control_qubit2: The qubit(s) used as the second control.
            control_qubit3: The qubit(s) used as the third control.
            target_qubit: The qubit(s) targeted by the gate.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.rcccx(control_qubit1, control_qubit2, control_qubit3, target_qubit)
        return self

    def rx(self, theta: ParameterExpression | float, qubit: QubitSpecifier, label: str | None = None) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.RXGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The rotation angle of the gate.
            qubit: The qubit(s) to apply the gate to.
            label: The string label of the gate in the circuit.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.rx(theta, qubit, label=label)
        return self

    def crx(
        self,
        theta: ParameterExpression | float,
        control_qubit: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.CRXGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The angle of the rotation.
            control_qubit: The qubit(s) used as the control.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.crx(theta, control_qubit, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def rxx(self, theta: ParameterExpression | float, qubit1: QubitSpecifier, qubit2: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.RXXGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The angle of the rotation.
            qubit1: The qubit(s) to apply the gate to.
            qubit2: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.rxx(theta, qubit1, qubit2)
        return self

    def ry(self, theta: ParameterExpression | float, qubit: QubitSpecifier, label: str | None = None) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.RYGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The rotation angle of the gate.
            qubit: The qubit(s) to apply the gate to.
            label: The string label of the gate in the circuit.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.ry(theta, qubit, label=label)
        return self

    def cry(
        self,
        theta: ParameterExpression | float,
        control_qubit: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.CRYGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The angle of the rotation.
            control_qubit: The qubit(s) used as the control.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.cry(theta, control_qubit, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def ryy(self, theta: ParameterExpression | float, qubit1: QubitSpecifier, qubit2: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.RYYGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The rotation angle of the gate.
            qubit1: The qubit(s) to apply the gate to.
            qubit2: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.ryy(theta, qubit1, qubit2)
        return self

    def rz(self, phi: ParameterExpression | float, qubit: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.RZGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            phi: The rotation angle of the gate.
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.rz(phi, qubit)
        return self

    def crz(
        self,
        theta: ParameterExpression | float,
        control_qubit: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.CRZGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The angle of the rotation.
            control_qubit: The qubit(s) used as the control.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.crz(theta, control_qubit, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def rzx(self, theta: ParameterExpression | float, qubit1: QubitSpecifier, qubit2: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.RZXGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The rotation angle of the gate.
            qubit1: The qubit(s) to apply the gate to.
            qubit2: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.rzx(theta, qubit1, qubit2)
        return self

    def rzz(self, theta: ParameterExpression | float, qubit1: QubitSpecifier, qubit2: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.RZZGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The rotation angle of the gate.
            qubit1: The qubit(s) to apply the gate to.
            qubit2: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.rzz(theta, qubit1, qubit2)
        return self

    def ecr(self, qubit1: QubitSpecifier, qubit2: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.ECRGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit1: The first qubit(s) to apply the gate to.
            qubit2: The second qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.ecr(qubit1, qubit2)
        return self

    def s(self, qubit: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.SGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.s(qubit)
        return self

    def sdg(self, qubit: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.SdgGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.sdg(qubit)
        return self

    def cs(
        self,
        control_qubit: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.CSGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubit: The qubit(s) used as the control.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.cs(control_qubit, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def csdg(
        self,
        control_qubit: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.CSdgGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubit: The qubit(s) used as the control.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.csdg(control_qubit, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def swap(self, qubit1: QubitSpecifier, qubit2: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.SwapGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit1: The first qubit to apply the gate to.
            qubit2: The second qubit to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.swap(qubit1, qubit2)
        return self

    def iswap(self, qubit1: QubitSpecifier, qubit2: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.iSwapGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit1: The first qubit to apply the gate to.
            qubit2: The second qubit to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.iswap(qubit1, qubit2)
        return self

    def cswap(
        self,
        control_qubit: QubitSpecifier,
        target_qubit1: QubitSpecifier,
        target_qubit2: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.CSwapGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubit: The qubit(s) used as the control.
            target_qubit1: The qubit(s) targeted by the gate.
            target_qubit2: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. ``'1'``).  Defaults to controlling
                on the ``'1'`` state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.cswap(control_qubit, target_qubit1, target_qubit2, label=label, ctrl_state=ctrl_state)
        return self

    def sx(self, qubit: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.SXGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.sx(qubit)
        return self

    def sxdg(self, qubit: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.SXdgGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.sxdg(qubit)
        return self

    def csx(
        self,
        control_qubit: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.CSXGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubit: The qubit(s) used as the control.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.csx(control_qubit, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def t(self, qubit: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.TGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.t(qubit)
        return self

    def tdg(self, qubit: QubitSpecifier) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.TdgGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.tdg(qubit)
        return self

    def u(
        self,
        theta: ParameterExpression | float,
        phi: ParameterExpression | float,
        lam: ParameterExpression | float,
        qubit: QubitSpecifier,
    ) -> QuantumCircuit:
        r"""Apply :class:`~qiskit.circuit.library.UGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The :math:`\theta` rotation angle of the gate.
            phi: The :math:`\phi` rotation angle of the gate.
            lam: The :math:`\lambda` rotation angle of the gate.
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.u(theta, phi, lam, qubit)
        return self

    def cu(
        self,
        theta: ParameterExpression | float,
        phi: ParameterExpression | float,
        lam: ParameterExpression | float,
        gamma: ParameterExpression | float,
        control_qubit: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        r"""Apply :class:`~qiskit.circuit.library.CUGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            theta: The :math:`\theta` rotation angle of the gate.
            phi: The :math:`\phi` rotation angle of the gate.
            lam: The :math:`\lambda` rotation angle of the gate.
            gamma: The global phase applied of the U gate, if applied.
            control_qubit: The qubit(s) used as the control.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.cu(theta, phi, lam, gamma, control_qubit, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def x(self, qubit: QubitSpecifier, label: str | None = None) -> QuantumCircuit:
        r"""Apply :class:`~qiskit.circuit.library.XGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit: The qubit(s) to apply the gate to.
            label: The string label of the gate in the circuit.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.x(qubit, label=label)
        return self

    def cx(
        self,
        control_qubit: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        r"""Apply :class:`~qiskit.circuit.library.CXGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubit: The qubit(s) used as the control.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.cx(control_qubit, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def dcx(self, qubit1: QubitSpecifier, qubit2: QubitSpecifier) -> QuantumCircuit:
        r"""Apply :class:`~qiskit.circuit.library.DCXGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit1: The qubit(s) to apply the gate to.
            qubit2: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.dcx(qubit1, qubit2)
        return self

    def ccx(
        self,
        control_qubit1: QubitSpecifier,
        control_qubit2: QubitSpecifier,
        target_qubit: QubitSpecifier,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        r"""Apply :class:`~qiskit.circuit.library.CCXGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubit1: The qubit(s) used as the first control.
            control_qubit2: The qubit(s) used as the second control.
            target_qubit: The qubit(s) targeted by the gate.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.ccx(control_qubit1, control_qubit2, target_qubit, ctrl_state=ctrl_state)
        return self

    def mcx(
        self,
        control_qubits: Sequence[QubitSpecifier],
        target_qubit: QubitSpecifier,
        ancilla_qubits: QubitSpecifier | Sequence[QubitSpecifier] | None = None,
        mode: str = "noancilla",
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.MCXGate`.

        The multi-cX gate can be implemented using different techniques, which use different numbers
        of ancilla qubits and have varying circuit depth. These modes are:

        - ``'noancilla'``: Requires 0 ancilla qubits.
        - ``'recursion'``: Requires 1 ancilla qubit if more than 4 controls are used, otherwise 0.
        - ``'v-chain'``: Requires 2 less ancillas than the number of control qubits.
        - ``'v-chain-dirty'``: Same as for the clean ancillas (but the circuit will be longer).

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubits: The qubits used as the controls.
            target_qubit: The qubit(s) targeted by the gate.
            ancilla_qubits: The qubits used as the ancillae, if the mode requires them.
            mode: The choice of mode, explained further above.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.

        Raises:
            ValueError: if the given mode is not known, or if too few ancilla qubits are passed.
            AttributeError: if no ancilla qubits are passed, but some are needed.
        """
        self._qiskit_qc.mcx(
            control_qubits, target_qubit, ancilla_qubits=ancilla_qubits, mode=mode, ctrl_state=ctrl_state
        )
        return self

    def y(self, qubit: QubitSpecifier) -> QuantumCircuit:
        r"""Apply :class:`~qiskit.circuit.library.YGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.y(qubit)
        return self

    def cy(
        self,
        control_qubit: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        r"""Apply :class:`~qiskit.circuit.library.CYGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubit: The qubit(s) used as the controls.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.cy(control_qubit, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def z(self, qubit: QubitSpecifier) -> QuantumCircuit:
        r"""Apply :class:`~qiskit.circuit.library.ZGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            qubit: The qubit(s) to apply the gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.z(qubit)
        return self

    def cz(
        self,
        control_qubit: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        r"""Apply :class:`~qiskit.circuit.library.CZGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubit: The qubit(s) used as the controls.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '1').  Defaults to controlling
                on the '1' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.cz(control_qubit, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def ccz(
        self,
        control_qubit1: QubitSpecifier,
        control_qubit2: QubitSpecifier,
        target_qubit: QubitSpecifier,
        label: str | None = None,
        ctrl_state: str | int | None = None,
    ) -> QuantumCircuit:
        r"""Apply :class:`~qiskit.circuit.library.CCZGate`.

        For the full matrix form of this gate, see the underlying gate documentation.

        Args:
            control_qubit1: The qubit(s) used as the first control.
            control_qubit2: The qubit(s) used as the second control.
            target_qubit: The qubit(s) targeted by the gate.
            label: The string label of the gate in the circuit.
            ctrl_state:
                The control state in decimal, or as a bitstring (e.g. '10').  Defaults to controlling
                on the '11' state.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.ccz(control_qubit1, control_qubit2, target_qubit, label=label, ctrl_state=ctrl_state)
        return self

    def pauli(
        self,
        pauli_string: str,
        qubits: Sequence[QubitSpecifier],
    ) -> QuantumCircuit:
        """Apply :class:`~qiskit.circuit.library.PauliGate`.

        Args:
            pauli_string: A string representing the Pauli operator to apply, e.g. 'XX'.
            qubits: The qubits to apply this gate to.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.
        """
        self._qiskit_qc.pauli(pauli_string, qubits)
        return self

    def prepare_state(
        self,
        state: QuantumState | Statevector | Sequence[complex] | str | int,
        qubits: Sequence[QubitSpecifier] | None = None,
        label: str | None = None,
        normalize: bool = False,
    ) -> QuantumCircuit:
        r"""Prepare qubits in a specific state.

        This class implements a state preparing unitary. Unlike
        :meth:`.initialize` it does not reset the qubits first.

        Args:
            state: The state to initialize to, can be either of the following.

                * Statevector or vector of complex amplitudes to initialize to.
                * Labels of basis states of the Pauli eigenstates Z, X, Y. See
                  :meth:`.Statevector.from_label`. Notice the order of the labels is reversed with
                  respect to the qubit index to be applied to. Example label '01' initializes the
                  qubit zero to :math:`|1\rangle` and the qubit one to :math:`|0\rangle`.
                * An integer that is used as a bitmap indicating which qubits to initialize to
                  :math:`|1\rangle`. Example: setting params to 5 would initialize qubit 0 and qubit
                  2 to :math:`|1\rangle` and qubit 1 to :math:`|0\rangle`.

            qubits: Qubits to initialize. If ``None`` the initialization is applied to all qubits in
                the circuit.
            label: An optional label for the gate
            normalize: Whether to normalize an input array to a unit vector.

        Returns:
            A handle to the instruction that was just initialized

        Examples:
            Prepare a qubit in the state :math:`(|0\rangle - |1\rangle) / \sqrt{2}`.

            .. code-block::

                import numpy as np
                from qiskit import QuantumCircuit

                circuit = QuantumCircuit(1)
                circuit.prepare_state([1/np.sqrt(2), -1/np.sqrt(2)], 0)
                circuit.draw()

            output:

            .. parsed-literal::

                     ┌─────────────────────────────────────┐
                q_0: ┤ State Preparation(0.70711,-0.70711) ├
                     └─────────────────────────────────────┘


            Prepare from a string two qubits in the state :math:`|10\rangle`.
            The order of the labels is reversed with respect to qubit index.
            More information about labels for basis states are in
            :meth:`.Statevector.from_label`.

            .. code-block::

                import numpy as np
                from qiskit import QuantumCircuit

                circuit = QuantumCircuit(2)
                circuit.prepare_state('01', circuit.qubits)
                circuit.draw()

            output:

            .. parsed-literal::

                     ┌─────────────────────────┐
                q_0: ┤0                        ├
                     │  State Preparation(0,1) │
                q_1: ┤1                        ├
                     └─────────────────────────┘


            Initialize two qubits from an array of complex amplitudes
            .. code-block::

                import numpy as np
                from qiskit import QuantumCircuit

                circuit = QuantumCircuit(2)
                circuit.prepare_state([0, 1/np.sqrt(2), -1.j/np.sqrt(2), 0], circuit.qubits)
                circuit.draw()

            output:

            .. parsed-literal::

                     ┌───────────────────────────────────────────┐
                q_0: ┤0                                          ├
                     │  State Preparation(0,0.70711,-0.70711j,0) │
                q_1: ┤1                                          ├
                     └───────────────────────────────────────────┘
        """
        from QIRT import QuantumState

        if isinstance(state, QuantumState):
            state = state.state_vector
        self._qiskit_qc.prepare_state(state, qubits=qubits, label=label, normalize=normalize)
        return self

    def initialize(
        self,
        params: QuantumState | Statevector | Sequence[complex] | str | int,
        qubits: Sequence[QubitSpecifier] | None = None,
        normalize: bool = False,
    ):
        r"""Initialize qubits in a specific state.

        Qubit initialization is done by first resetting the qubits to :math:`|0\rangle`
        followed by calling :class:`~qiskit.circuit.library.StatePreparation`
        class to prepare the qubits in a specified state.
        Both these steps are included in the
        :class:`~qiskit.circuit.library.Initialize` instruction.

        Args:
            params: The state to initialize to, can be either of the following.

                * Statevector or vector of complex amplitudes to initialize to.
                * Labels of basis states of the Pauli eigenstates Z, X, Y. See
                  :meth:`.Statevector.from_label`. Notice the order of the labels is reversed with
                  respect to the qubit index to be applied to. Example label '01' initializes the
                  qubit zero to :math:`|1\rangle` and the qubit one to :math:`|0\rangle`.
                * An integer that is used as a bitmap indicating which qubits to initialize to
                  :math:`|1\rangle`. Example: setting params to 5 would initialize qubit 0 and qubit
                  2 to :math:`|1\rangle` and qubit 1 to :math:`|0\rangle`.

            qubits: Qubits to initialize. If ``None`` the initialization is applied to all qubits in
                the circuit.
            normalize: Whether to normalize an input array to a unit vector.

        Returns:
            QuantumCircuit: Quantum circuit with the applied gate.

        Examples:
            Prepare a qubit in the state :math:`(|0\rangle - |1\rangle) / \sqrt{2}`.

            .. code-block::

                import numpy as np
                from qiskit import QuantumCircuit

                circuit = QuantumCircuit(1)
                circuit.initialize([1/np.sqrt(2), -1/np.sqrt(2)], 0)
                circuit.draw()

            output:

            .. parsed-literal::

                     ┌──────────────────────────────┐
                q_0: ┤ Initialize(0.70711,-0.70711) ├
                     └──────────────────────────────┘


            Initialize from a string two qubits in the state :math:`|10\rangle`.
            The order of the labels is reversed with respect to qubit index.
            More information about labels for basis states are in
            :meth:`.Statevector.from_label`.

            .. code-block::

                import numpy as np
                from qiskit import QuantumCircuit

                circuit = QuantumCircuit(2)
                circuit.initialize('01', circuit.qubits)
                circuit.draw()

            output:

            .. parsed-literal::

                     ┌──────────────────┐
                q_0: ┤0                 ├
                     │  Initialize(0,1) │
                q_1: ┤1                 ├
                     └──────────────────┘

            Initialize two qubits from an array of complex amplitudes.

            .. code-block::

                import numpy as np
                from qiskit import QuantumCircuit

                circuit = QuantumCircuit(2)
                circuit.initialize([0, 1/np.sqrt(2), -1.j/np.sqrt(2), 0], circuit.qubits)
                circuit.draw()

            output:

            .. parsed-literal::

                     ┌────────────────────────────────────┐
                q_0: ┤0                                   ├
                     │  Initialize(0,0.70711,-0.70711j,0) │
                q_1: ┤1                                   ├
                     └────────────────────────────────────┘
        """
        from QIRT import QuantumState

        if isinstance(params, QuantumState):
            params = params.state_vector
        self._qiskit_qc.initialize(params, qubits=qubits, normalize=normalize)
        return self
