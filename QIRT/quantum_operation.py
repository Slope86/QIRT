"""
Module to extend Qiskit's QuantumCircuit with additional functionalities.

This module provides an extended version of Qiskit's QuantumCircuit class, adding
methods for basis conversion and visualization in matrix form. The extended class,
QuantumOperation, includes methods to convert the basis of qubits and to generate
a LaTeX representation of the quantum circuit.

The functionalities added in this module are:

- Conversion of the quantum circuit to a matrix form.\n
- Drawing the quantum circuit or its matrix representation.\n
- Adding gates to convert qubits from one basis to another.\n

See Also:
    [Qiskit QuantumCircuit documentation](https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.html)
"""

import numpy as np
from numpy.typing import NDArray
from qiskit import QuantumCircuit, quantum_info

from QIRT import latex_drawer


class QuantumOperation(QuantumCircuit):
    """An extended class of QuantumCircuit from Qiskit.

    This class extends the QuantumCircuit class from Qiskit to provide additional
    functionalities for converting basis and visualizing the quantum circuit in
    matrix form.

    See Also:
        [Qiskit QuantumCircuit documentation](https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.html)
    """

    def to_matrix(self) -> NDArray[np.complex128]:
        """Return matrix form of the quantum circuit as a numpy array.

        This method returns the matrix representation of the quantum circuit by
        reversing the order of qubits to match textbook notation.

        Returns:
            NDArray[np.complex128]: The matrix representation of the quantum circuit.
        """
        reverse_qc = self.reverse_bits()  # REVERSE the order of qubits to match textbook notation
        return np.asarray(quantum_info.Operator(reverse_qc).data, dtype=np.complex128)

    def draw(self, output: str | None = "mpl", source: bool = False, *args, **kwargs):
        """Draw the quantum circuit, or show its matrix form if output is 'matrix'.

        Args:
            output (str | None, optional): The output format for drawing the circuit.
                If 'text', generates ASCII art TextDrawing that can be printed in the console.\n
                If 'mpl', generates images with color rendered purely in Python using matplotlib.\n
                If 'latex', generates high-quality images compiled via latex.\n
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
                    return super().draw(output="latex_source", *args, **kwargs)
                return super().draw(output="latex", *args, **kwargs)
            case _:
                return super().draw(output=output, *args, **kwargs)

    def _xyz_convert_circ(self, target_basis: str, current_basis: str, qubit_index: int) -> None:
        """Add the corresponding gate that converts different basis.

        This method adds the appropriate gates to the circuit to convert a qubit
        from the current basis to the target basis.

        Args:
            target_basis (str): The target basis to convert to.
            current_basis (str): The current basis of the qubit.
            qubit_index (int): The index of the qubit to be converted.
        """
        if current_basis == target_basis:
            return
        current_basis += target_basis
        match current_basis:
            case "zx" | "xz":
                self.h(qubit_index)
            case "zy":
                self.sdg(qubit_index)
                self.h(qubit_index)
            case "yz":
                self.h(qubit_index)
                self.s(qubit_index)
            case "xy":
                self.h(qubit_index)
                self.sdg(qubit_index)
                self.h(qubit_index)
            case "yx":
                self.h(qubit_index)
                self.s(qubit_index)
                self.h(qubit_index)
        return
