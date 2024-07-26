"""
Module to extend Qiskit's Statevector with additional functionalities.

This module provides an extended version of Qiskit's Statevector class, adding
methods for quantum state manipulations, basis conversions, and visualizations.
The extended class, QuantumState, includes methods to convert the basis of qubits,
perform measurements, and visualize the quantum state in various formats.

The functionalities added in this module are:

- Initialization of QuantumState with automatic calculation of qubit count.\n
- Creation of state vectors from input coefficients and label strings.\n
- Calculation of Shannon entropy for the quantum state.\n
- Evolution of the quantum state using various operators.\n
- Conversion of the state vector to a column matrix representation.\n
- Visualization of the quantum state in different formats (LaTeX, matrix form).\n
- Measurement of specified qubits and obtaining the resulting states.\n
- Basis conversion to minimize entropy either globally or locally.\n

See Also:
    [Qiskit Statevector documentation](https://qiskit.org/documentation/stubs/qiskit.quantum_info.Statevector.html)
"""

from __future__ import annotations

import itertools
import re
import typing

import numpy as np
from qiskit.exceptions import QiskitError
from qiskit.quantum_info import Statevector
from scipy import stats

from QIRT import QuantumCircuit, latex_drawer
from QIRT.utils import Ket

if typing.TYPE_CHECKING:
    from typing import List, Tuple

    from IPython.display import Latex
    from numpy.typing import NDArray


class QuantumState:
    """An extended class of Statevector from Qiskit.

    This class extends the Statevector class from Qiskit to provide additional
    functionalities specific to quantum state manipulations and measurements.

    Attributes:
        _num_of_qubit (int): The number of qubits in the quantum state.

    See Also:
        [Qiskit Statevector documentation](https://qiskit.org/documentation/stubs/qiskit.quantum_info.Statevector.html)
    """

    def __init__(self, *args, **kwargs):
        """Initialize a QuantumState object.

        This constructor initializes the QuantumState object by calling the
        constructor of the base Statevector class from Qiskit. It also calculates
        and stores the number of qubits in the quantum state.
        """
        self.state_vector = Statevector(*args, **kwargs)
        self._num_of_qubit = int(np.log2(len(self.state_vector.data)))

    @property
    def data(self) -> NDArray[np.complex128]:
        """Get the data of the quantum state vector.

        This property returns the data of the quantum state vector stored in the object.

        Returns:
            NDArray[np.complex128]: The data of the quantum state vector.
        """
        return self.state_vector.data

    @property
    def num_of_qubit(self) -> int:
        """Get the number of qubits in the quantum state.

        This property returns the total number of qubits that are currently
        represented in the quantum state vector.

        Returns:
            int: The number of qubits in the quantum state.
        """
        return self._num_of_qubit

    @classmethod
    def from_label(cls, *args: str | Tuple[complex, str]) -> QuantumState:
        """Create a state vector from input coefficients and label strings.

        Examples:
            >>> QuantumState.from_label("0", "1")
            (|0> + |1>)/√2 QuantumState object.

            >>> QuantumState.from_label("00", "01", "10", "11")
            (|00> + |01> + |10> + |11>)/2 = |++> QuantumState object.

            >>> QuantumState.from_label("+", (-1, "-"))
            (|+> - |->)/√2 QuantumState object.

            >>> QuantumState.from_label((2**0.5, "0"), "+", (-1, "-"))
            (√2|0> + |+> - |->)/2 = |+> QuantumState object.

        Args:
            args (str | Tuple[complex, str]): Input label strings or tuples of coefficients and label strings.

        Returns:
            QuantumState: The state vector object.

        Raises:
            QiskitError: If labels contain invalid characters or if labels have different numbers of qubits.
        """
        # Separate the input into coefficients and labels
        coefficients: List[complex] = []
        labels: List[str] = []
        for i, arg in enumerate(args):
            if isinstance(arg, tuple):  # Check if the input is a tuple of coefficient and label or just a label
                coefficients.append(arg[0])
                labels.append(arg[1])
            else:
                coefficients.append(1.0)
                labels.append(arg)

            if not Ket.check_valid(labels[i]):
                raise QiskitError("Invalid label string.")

            if len(labels[0]) != len(labels[i]):
                raise QiskitError("Each label's number of qubits must be the same.")

            labels[i] = Ket.to_qiskit_notation(labels[i])  # Convert the label to qiskit notation

        # Create the state vector based on the input
        state_vector: Statevector = Statevector.from_label(labels[0]) * coefficients[0]
        for coefficient, label in zip(coefficients[1:], labels[1:]):
            state_vector += Statevector.from_label(label) * coefficient

        state_vector /= state_vector.trace() ** 0.5  # Normalize the state
        return QuantumState(state_vector)

    def entropy(self) -> np.float_:
        """Calculate and return the Shannon  entropy of the quantum state.

        The Shannon  entropy is a measure of the quantum state's uncertainty or mixedness.

        Returns:
            np.float_: The Shannon  entropy of the quantum state, calculated in base 2.
        """
        entropy = stats.entropy(self.state_vector.probabilities(), base=2)
        if type(entropy) is np.float_:
            return entropy
        raise QiskitError("Entropy calculation failed.")

    def apply(self, other: QuantumCircuit, qargs: list[int] | None = None) -> QuantumState:
        """Apply a quantum operation to the quantum state.

        This method applies the given operator to the quantum state, evolving it
        according to the operator's effect.

        Args:
            other (QuantumOperation):
                The operator used to evolve the quantum state.
            qargs (list[int] | None, optional): A list of subsystem positions of
                the QuantumState to apply the operator on. Defaults to None.

        Returns:
            QuantumState: The quantum state after evolution.

        Raises:
            QiskitError: If the operator dimension does not match the specified
                quantum state subsystem dimensions.
        """
        reversed_state_vector: Statevector = self.state_vector.reverse_qargs()
        evolved_state_vector: Statevector = Statevector.evolve(
            reversed_state_vector, other._qiskit_qc, qargs
        ).reverse_qargs()
        return QuantumState(evolved_state_vector)

    def to_matrix(self) -> NDArray[np.complex128]:
        """Convert the quantum state vector to a column matrix representation.

        This method takes the quantum state vector stored in the object and converts
        it into a column matrix form, which can be useful for various matrix-based
        operations and calculations.

        Returns:
            NDArray[np.complex128]: The quantum state represented as a column matrix.
        """
        vector = self.state_vector.data
        matrix = vector[np.newaxis].T
        return matrix

    def draw(
        self,
        output: str = "latex",
        target_basis: List[str] | str | None = None,
        show_qubit_index: bool = True,
        output_length: int = 2,
        source: bool = False,
    ):
        """Visualize the statevector.

        This method provides different visualization options for the quantum state vector,
        such as LaTeX, matrix form, or other specified formats.

        Args:
            output (str, optional): Visualization method. Defaults to "latex". Options include:
                - "matrix": Outputs the state vector as a LaTeX formatted matrix.
                - "latex": Outputs the state vector as a LaTeX formatted expression.
            target_basis (List[str] | str | None, optional): The target basis for visualization. Defaults to None.
            show_qubit_index (bool, optional): Whether to show qubit indices in the visualization. Defaults to True.
            output_length (int, optional): The number of terms in each line, defined as 2^output_length.
                                        Defaults to 2 (i.e., 4 terms per line).
            source (bool, optional): Whether to return the latex source code for the visualization. Defaults to False.

        Returns:
            matplotlib.Figure | str | TextMatrix | IPython.display.Latex | Latex: The visualization
                output depending on the chosen method.
        """
        match output:
            case "matrix":
                return latex_drawer.matrix_to_latex(self.to_matrix(), source=source)
            case "latex":
                return latex_drawer.state_to_latex(
                    state=self,
                    state_basis=["z"] * self.num_of_qubit,
                    target_basis=target_basis,
                    show_qubit_index=show_qubit_index,
                    output_length=output_length,
                    source=source,
                )
            case _:
                raise QiskitError("Invalid output format.")

    def state_after_measure(
        self, measure_bit: List[int] | str, state_basis: List[str] | str = [], shot=100
    ) -> Tuple[List[QuantumState], List[QuantumState]]:
        """Obtain the quantum state after a measurement.

        This method returns the quantum states resulting from measuring specified qubits in a given basis.
        It provides two lists of quantum states: the measured states in the Z basis and the system states
        after measurement.

        Args:
            measure_bit (List[int] | str): The bits (qubits) to measure. Can be a list of indices or a
                string specifying the bits.
            state_basis (List[str] | str, optional): The basis in which to perform the measurement.
                Defaults to an empty list.
            shot (int, optional): The number of measurement shots to perform. Defaults to 100.

        Returns:
            Tuple[List[QuantumState], List[QuantumState]]:
                - A list of quantum states representing the measurement results in the Z basis.
                - A list of quantum states representing the system state after the measurement in the Z basis.
        """
        z_basis_measure_state_list, z_basis_system_state_list, _, _, _, _ = self._measure(
            measure_bit=measure_bit, state_basis=state_basis, shot=shot
        )
        return (z_basis_measure_state_list, z_basis_system_state_list)

    def draw_measure(
        self,
        measure_bit: List[int] | str,
        state_basis: List[str] | str = [],
        show_qubit_index: bool = True,
        output_length: int = 2,
        source: bool = False,
        shot: int = 100,
    ) -> str | Latex:
        """Visualize the measurement results of the quantum state.

        This method performs a measurement on specified qubits and visualizes the
        resulting quantum states and their measurement outcomes in a specified format.

        Args:
            measure_bit (List[int] | str): The bits (qubits) to measure. Can be a list
                of indices or a string specifying the bits.
            state_basis (List[str] | str, optional): The basis in which to perform the
                measurement. Defaults to an empty list.
            show_qubit_index (bool, optional): Whether to show qubit indices in the
                visualization. Defaults to True.
            output_length (int, optional): The number of terms in each line, defined as
                2^output_length. Defaults to 2 (i.e., 4 terms per line).
            source (bool, optional): Whether to return the source code for the
                visualization. Defaults to False.
            shot (int, optional): The number of measurement shots to perform.
                Defaults to 100.

        Returns:
            str | Latex: The visualization of the measurement results, either
            as an image or a string representing the source code.

        Raises:
            QiskitError: If the measurement basis or bit specifications are invalid.
        """
        _, _, measure_state_list, system_state_list, measure_basis, system_basis = self._measure(
            measure_bit, state_basis, shot
        )
        return latex_drawer.measure_result_to_latex(
            measure_state_list=measure_state_list,
            system_state_list=system_state_list,
            measure_basis=measure_basis,
            system_basis=system_basis,
            measure_bit=measure_bit,
            show_qubit_index=show_qubit_index,
            output_length=output_length,
            source=source,
        )

    def _basis_convert(
        self,
        target_basis: List[str] | str = [],
        current_basis: List[str] | str = [],
        algorithm: str = "global",
    ) -> tuple[QuantumState, List[str]]:
        """Convert the quantum state to a target basis.

        This method converts the quantum state from its current basis to a specified
        target basis using a quantum circuit. If the target basis is not fully specified,
        it will auto-choose the basis with minimum entropy for unspecified qubits.

        Args:
            target_basis (List[str] | str, optional): The target basis for conversion. Defaults to an empty list.
            current_basis (List[str] | str, optional): The current basis of the quantum state.
                Defaults to an empty list.
            algorithm (str, optional): The algorithm used for finding the minimum entropy basis. Defaults to "global".
                Options are:
                - "global": Global minimum entropy basis conversion.
                - "local": Local minimum entropy basis conversion.

        Returns:
            tuple[QuantumState, List[str]]: The converted quantum state and the list of the basis used for conversion.

        Raises:
            QiskitError: If the input basis is invalid or if an invalid algorithm is specified.
        """
        # Default target_basis is auto choose basis with minimum entropy (basis = "*")
        target_basis = list(target_basis) + ["*"] * (self.num_of_qubit - len(target_basis))
        # Default current_basis is Z basis
        current_basis = list(current_basis) + ["z"] * (self.num_of_qubit - len(current_basis))

        # Check if input is valid
        if re.match(R"^[\-\*xyz]+$", "".join(target_basis)) is None:
            raise QiskitError("Invalid basis.")

        # Empty list to save auto-choose-basis index
        auto_basis_index = []
        # Convert basis using QuantumCircuit
        convert_circ = QuantumCircuit(self.num_of_qubit)
        for i in range(self.num_of_qubit):
            if target_basis[i] == current_basis[i]:
                continue
            if target_basis[i] == "*" or target_basis[i] == "-":
                auto_basis_index.append(i)
                continue
            convert_circ._xyz_convert_circ(target_basis=target_basis[i], current_basis=current_basis[i], qubit_index=i)
            current_basis[i] = target_basis[i]

        converted_state = self.apply(convert_circ)
        if not auto_basis_index:
            return (converted_state, current_basis)

        # If user don't specify which basis to convert, convert basis to basis with minimum entropy
        match algorithm:
            case "global":
                if len(auto_basis_index) > 8:
                    print(
                        "Notice: global minimum entropy basis convert with more then 8 qubits might take a long time."
                    )
                optimize_basis = converted_state._global_min_entropy_basis(auto_basis_index, current_basis)
            case "local":
                optimize_basis = converted_state._local_min_entropy_basis(auto_basis_index, current_basis)
            case _:
                raise QiskitError("Invalid min_entropy_basis_find_method.")

        return converted_state._basis_convert(target_basis=optimize_basis, current_basis=current_basis)

    def _global_min_entropy_basis(self, auto_basis_index: List[int], current_basis: List[str]) -> List[str]:
        """Find the basis with global minimum entropy.

        This method searches for the basis configuration that minimizes the entropy
        of the quantum state globally, by trying all possible combinations of the
        specified bases at the auto-choose-basis indices.

        Args:
            auto_basis_index (List[int]): Indices of the qubits for which the basis
                should be auto-chosen to minimize entropy.
            current_basis (List[str]): The current basis of the quantum state.

        Returns:
            List[str]: The basis configuration with the global minimum entropy.
        """
        num_of_auto_basis = len(auto_basis_index)
        min_entropy = float("inf")
        min_basis = current_basis.copy()
        try_basis = current_basis.copy()
        for basis in itertools.product(["z", "x", "y"], repeat=num_of_auto_basis):
            for i in range(num_of_auto_basis):
                try_basis[auto_basis_index[i]] = basis[i]
                try_state = self._basis_convert(target_basis=try_basis, current_basis=current_basis)[0]
            if (entropy := try_state.entropy()) < min_entropy:
                min_entropy = entropy
                min_basis = try_basis.copy()
        return min_basis

    def _local_min_entropy_basis(self, auto_basis_index: List[int], current_basis: List[str]) -> List[str]:
        """Find the basis with local minimum entropy.

        This method searches for the basis configuration that locally minimizes the entropy
        of the quantum state by iteratively selecting the best basis for each qubit.

        Args:
            auto_basis_index (List[int]): Indices of the qubits for which the basis should be auto-chosen to
                minimize entropy.
            current_basis (List[str]): The current basis of the quantum state.

        Returns:
            List[str]: The basis configuration with the local minimum entropy.
        """
        # Step 1: Change all auto-choose-basis to y, e.g. [-, -, -, -] -> [z, z, z, z], calculate entropy
        # Step 2,3: Same as Step 1, but with x-basis and y-basis
        # Step 4: from Step 1 to 3, choose the basis with minimum entropy.
        min_entropy = float("inf")
        min_basis = current_basis.copy()
        for basis in ["z", "x", "y"]:
            try_basis = min_basis.copy()
            for i in auto_basis_index:
                try_basis[i] = basis
            try_state = self._basis_convert(target_basis=try_basis, current_basis=current_basis)[0]
            if (entropy := try_state.entropy()) < min_entropy:
                min_entropy = entropy
                min_basis = try_basis.copy()

        # Step 1: Change the first auto-choose-basis to y, e.g. [-, -, -, -] -> [y, -, -, -], calculate entropy,
        # Step 2,3: Same as Step 1, but with x-basis and z-basis
        # Step 4: from Step 1 to 3, choose the basis with minimum entropy.
        # Step 5: Repeat Step 1 to 4 for the second auto-choose-basis, and so on. (greedy)
        # e.g. [-, -, -, -] -> [x, -, -, -] -> [x, z, -, -] -> [x, z, y, -] -> [x, z, y, z]
        for i in auto_basis_index:
            try_basis = min_basis.copy()
            for basis in ["y", "x", "z"]:
                try_basis[i] = basis
                try_state = self._basis_convert(target_basis=try_basis, current_basis=current_basis)[0]
                if (entropy_tmp := try_state.entropy()) < min_entropy:
                    min_entropy = entropy_tmp
                    min_basis[i] = basis
        return min_basis

    def _measure(
        self, measure_bit: List[int] | str, state_basis: List[str] | str = [], shot=100
    ) -> Tuple[List[QuantumState], List[QuantumState], List[QuantumState], List[QuantumState], List[str], List[str]]:
        """Perform a measurement on the quantum state.

        This method measures the specified qubits in the given basis and returns the
        resulting quantum states and measurement outcomes.

        Args:
            measure_bit (List[int] | str): The bits (qubits) to measure. Can be a list
                of indices or a string specifying the bits.
            state_basis (List[str] | str, optional): The basis in which to perform the
                measurement. Defaults to an empty list.
            shot (int, optional): The number of measurement shots to perform. Defaults to 100.

        Returns:
            Tuple[List[QuantumState], List[QuantumState], List[QuantumState], List[QuantumState], List[str], List[str]]:
                - z_basis_measure_state_list: Measurement states in the Z basis.
                - z_basis_system_state_list: System states in the Z basis.
                - measure_state_list: Measurement states in the original basis.
                - system_state_list: System states in the original basis.
                - measure_basis: The basis used for the measurement.
                - system_basis: The system basis after conversion.
        """
        if isinstance(measure_bit, str):
            measure_bit = [int(i) for i in measure_bit]

        converted_state, system_basis = self._basis_convert(
            target_basis=state_basis, current_basis=["z"] * self.num_of_qubit
        )

        # crate empty list for output
        z_basis_measure_state_list = [None] * 2 ** len(measure_bit)
        z_basis_system_state_list = [None] * 2 ** len(measure_bit)
        measure_state_list = [None] * 2 ** len(measure_bit)
        system_state_list = [None] * 2 ** len(measure_bit)
        for _ in range(shot):
            measure_result: Tuple[str, Statevector] = Statevector(converted_state.data).measure(qargs=measure_bit)
            measure_ket: str = measure_result[0]
            system_state = QuantumState(measure_result[1])
            measure_ket = measure_ket[::-1]  # REVERSE the order of qubits to fit textbook notation
            if measure_state_list[int(measure_ket, 2)] is None:
                measure_basis = []
                for i in measure_bit:
                    measure_basis.append(system_basis[i])

                basis_convert_measure_ket = ""
                for b, k in zip(measure_basis, measure_ket):
                    match b:
                        case "z":
                            basis_convert_measure_ket += Ket.z1 if int(k) else Ket.z0
                        case "x":
                            basis_convert_measure_ket += Ket.x1 if int(k) else Ket.x0
                        case "y":
                            basis_convert_measure_ket += Ket.y1 if int(k) else Ket.y0

                measure_state_z_basis = self.from_label(basis_convert_measure_ket)
                system_state = QuantumState(system_state)

                z_basis_measure_state_list[int(measure_ket, 2)] = measure_state_z_basis
                z_basis_system_state_list[int(measure_ket, 2)] = system_state._basis_convert(
                    target_basis=["z"] * self.num_of_qubit, current_basis=system_basis
                )[0]
                measure_state_list[int(measure_ket, 2)] = measure_state_z_basis._basis_convert(
                    target_basis=measure_basis
                )[0]
                system_state_list[int(measure_ket, 2)] = system_state

        return (
            z_basis_measure_state_list,
            z_basis_system_state_list,
            measure_state_list,
            system_state_list,
            measure_basis,
            system_basis,
        )
