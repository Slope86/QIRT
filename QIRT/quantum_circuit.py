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

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray
from qiskit import QuantumCircuit as QiskitQC
from qiskit import quantum_info
from qiskit.circuit.instructionset import InstructionSet
from qiskit.circuit.quantumcircuit import QubitSpecifier

from QIRT import latex_drawer
from QIRT.utils import inverse_tensor


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

    def __getattr__(self, name: str) -> QuantumCircuit:
        """Return the original method if it returns an InstructionSet.

        Args:
            name (str): The name of the method to call

        Raises:
            AttributeError: If the method is not found in QuantumCircuit

        Returns:
            QuantumCircuit: The original method if it returns an InstructionSet.
        """
        original_method = getattr(self._qiskit_qc, name)

        def wrapper(*args, **kwargs):
            result = original_method(*args, **kwargs)
            if isinstance(result, InstructionSet):
                return self
            raise AttributeError(f"Method {name} not found in QuantumCircuit")

        return wrapper
