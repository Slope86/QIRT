r"""Module to extend Qiskit's Statevector with additional functionalities.

This module provides an extended version of Qiskit's Statevector class, adding
methods for quantum state manipulations, basis conversions, and visualizations.
The extended class, QuantumState, includes methods to convert the basis of qubits,
perform measurements, and visualize the quantum state in various formats.

The functionalities added in this module are:

- Initialization of QuantumState with automatic calculation of qubit count.
- Creation of state vectors from input coefficients and label strings.
- Calculation of Shannon entropy for the quantum state.
- Evolution of the quantum state using various operators.
- Conversion of the state vector to a column matrix representation.
- Visualization of the quantum state in different formats (LaTeX, matrix form).
- Measurement of specified qubits and obtaining the resulting states.
- Basis conversion to minimize entropy either globally or locally.

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
    from IPython.display import Latex
    from numpy.typing import NDArray
    from qiskit.circuit.instruction import Instruction
    from qiskit.circuit.quantumcircuit import QuantumCircuit as QiskitQC
    from qiskit.quantum_info.operators.operator import Operator


class QuantumState:
    """An extended class of Statevector from Qiskit.

    This class extends the Statevector class from Qiskit to provide additional
    functionalities specific to quantum state manipulations and measurements.

    Attributes:
        _num_of_qubit (int): The number of qubits in the quantum state.

    See Also:
        [Qiskit Statevector documentation](https://qiskit.org/documentation/stubs/qiskit.quantum_info.Statevector.html)
    """

    # TODO: Add Bell measurement method.

    def __init__(
        self,
        data: np.ndarray | list | Statevector | Operator | QiskitQC | Instruction,
        dims: int | tuple | list | None = None,
    ):
        """Initialize a QuantumState object.

        This constructor initializes the QuantumState object by calling the
        constructor of the base Statevector class from Qiskit. It also calculates
        and stores the number of qubits in the quantum state.

        Args:
            data (np.array or list or Statevector or Operator or QuantumCircuit or qiskit.circuit.Instruction):
                Data from which the statevector can be constructed. This can be either a complex
                vector, another statevector, a ``Operator`` with only one column or a
                ``QuantumCircuit`` or ``Instruction``.  If the data is a circuit or instruction,
                the statevector is constructed by assuming that all qubits are initialized to the
                zero state.
            dims (int or tuple or list): Optional. The subsystem dimension of the state (See additional information).
        """
        if isinstance(data, (list | np.ndarray)):
            # Normalize the state vector
            data = np.asarray(data, dtype=complex)
            data /= np.linalg.norm(data)
        self.state_vector = Statevector(data, dims)
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
    def from_label(cls, *args: str | tuple[complex, str]) -> QuantumState:
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

            >>> QuantumState.from_label("0", (1j, "1"))
            (|0> + i|1>)/√2 = |i> QuantumState object.

        Args:
            args (str | Tuple[complex, str]): Input label strings or tuples of coefficients and label strings.

        Returns:
            QuantumState: The state vector object.

        Raises:
            QiskitError: If labels contain invalid characters or if labels have different numbers of qubits.
        """
        # Separate the input into coefficients and labels
        coefficients: list[complex] = []
        labels: list[str] = []
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

    def tensor(self, other: QuantumState) -> QuantumState:
        """Return the tensor product state self ⊗ other.

        This method calculates the tensor product of the quantum states stored in the
        object and another given quantum state, returning the resulting quantum state.

        Args:
            other (QuantumState): The other quantum state to tensor with.

        Returns:
            QuantumState: the tensor product operator self ⊗ other.
        """
        return QuantumState(self.state_vector.tensor(other.state_vector))

    def entropy(self) -> np.float64:
        """Calculate and return the Shannon  entropy of the quantum state.

        The Shannon  entropy is a measure of the quantum state's uncertainty or mixedness.

        Returns:
            np.float64: The Shannon  entropy of the quantum state, calculated in base 2.
        """
        entropy = stats.entropy(self.state_vector.probabilities(), base=2)
        if type(entropy) is np.float64:
            return entropy
        raise QiskitError("Entropy calculation failed.")

    def apply(self, other: QuantumCircuit, qargs: list[int] | None = None) -> QuantumState:
        """Apply a quantum circuit to the quantum state.

        This method applies the given operator to the quantum state, evolving it
        according to the operator's effect.

        Args:
            other (QuantumCircuit):
                The operator used to evolve the quantum state.
            qargs (list[int] | None, optional): A list of subsystem positions of
                the QuantumState to apply the operator on. Defaults to None.

        Returns:
            QuantumState: The quantum state after evolution.

        Raises:
            QiskitError: If the operator dimension does not match the specified
                quantum state subsystem dimensions.
        """
        # REVERSE the order of qubits to fit qiskit notation
        reversed_state_vector: Statevector = self.state_vector.reverse_qargs()
        evolved_state_vector: Statevector = reversed_state_vector.evolve(other._qiskit_qc, qargs).reverse_qargs()
        return QuantumState(evolved_state_vector)

    def to_matrix(self) -> NDArray[np.complex128]:
        """Convert the quantum state vector to a column matrix representation.

        This method takes the quantum state vector stored in the object and converts
        it into a column matrix form, which can be useful for various matrix-based
        operations and calculations.

        Returns:
            NDArray[np.complex128]: The quantum state represented as a column matrix.
        """
        flat_vector = self.state_vector.data
        matrix = flat_vector[np.newaxis].T
        return matrix

    # TODO: Add optional argument to disable coefficient simplification in draw() & draw_measurement() methods.
    # TODO: Add document about draw() & draw_measurement() methods' output options:
    #           target_basis can be "-" to hide the corresponding qubit or "*" to auto-choose basis.
    def draw(
        self,
        output: str = "latex",
        target_basis: list[str] | str | None = None,
        show_qubit_index: bool = True,
        output_length: int = 2,
        source: bool = False,
    ):
        """Visualize the statevector.

        This method provides different visualization options for the quantum state vector,
        such as LaTeX, matrix/vector form, or other specified formats.

        Args:
            output (str, optional): Visualization method. Defaults to "latex". Options include:
                - "matrix" or "vector": Outputs the QuantumState as a LaTeX formatted matrix.
                - "latex": Outputs the QuantumState as a LaTeX formatted expression.
                - "repr": ASCII TextMatrix of the QuantumState's `__repr__`.
                - "text": ASCII TextMatrix that can be printed in the console.
                - "qsphere": Matplotlib figure rendering the QuantumState using `plot_state_qsphere()`.
                - "hinton": Matplotlib figure rendering the QuantumState using `plot_state_hinton()`.
                - "bloch": Matplotlib figure rendering the QuantumState using `plot_bloch_multivector()`.
                - "city": Matplotlib figure rendering the QuantumState using `plot_state_city()`.
                - "paulivec": Matplotlib figure rendering the QuantumState using `plot_state_paulivec()`.
            target_basis (List[str] | str | None, optional): The target basis for visualization. Defaults to None.
            show_qubit_index (bool, optional): Whether to show qubit indices in the visualization. Defaults to True.
            output_length (int, optional): The number of terms in each line, defined as 2^output_length.
                Defaults to 2 (i.e., 4 terms per line).
            source (bool, optional): Whether to return the latex source code for the visualization option "matrix" and
                "latex". Defaults to False.

        Returns:
            (matplotlib.Figure | str | TextMatrix | IPython.display.Latex | Latex): The visualization
                output depending on the chosen method.
        """
        match output:
            case "matrix" | "vector":
                return latex_drawer.matrix_to_latex(self.to_matrix(), source=source)
            case "latex":
                return latex_drawer.state_to_latex(
                    state=self,
                    current_basis=["z"] * self.num_of_qubit,
                    target_basis=target_basis,
                    show_qubit_index=show_qubit_index,
                    output_length=output_length,
                    source=source,
                )
            case "repr" | "text" | "qsphere" | "hinton" | "city" | "paulivec":
                return self.state_vector.draw(output=output)
            case "bloch":
                reversed_state_vector = self.state_vector.reverse_qargs()
                return reversed_state_vector.draw(output=output)
            case _:
                raise QiskitError("Invalid output format.")

    def draw_measurement(
        self,
        measure_bit: list[int] | str,
        target_basis: list[str] | str = [],
        show_qubit_index: bool = True,
        output_length: int = 2,
        source: bool = False,
    ) -> str | Latex:
        """Visualize the measurement results of the quantum state.

        This method performs a measurement on specified qubits and visualizes the
        resulting quantum states and their measurement outcomes in a specified format.

        Args:
            measure_bit (List[int] | str): The bits (qubits) to measure. Can be a list
                of indices or a string specifying the bits.
            target_basis (List[str] | str, optional): The basis in which to perform the
                measurement. Defaults to basis with minimum entropy.
            show_qubit_index (bool, optional): Whether to show qubit indices in the
                visualization. Defaults to True.
            output_length (int, optional): The number of terms in each line, defined as
                2^output_length. Defaults to 2 (i.e., 4 terms per line).
            source (bool, optional): Whether to return the source code for the
                visualization. Defaults to False.

        Returns:
            (str | Latex): The visualization of the measurement results,
                either as an image or a string representing the source code.

        Raises:
            QiskitError: If the measurement basis or bit specifications are invalid.
        """
        _, _, measure_state_list, system_state_list, measure_basis, system_basis = self._measurement(
            measure_bit, target_basis
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

    def state_after_measurement(
        self, measure_bit: list[int] | str, target_basis: list[str] | str = [], shot=100
    ) -> list[QuantumState]:
        """Simulate quantum measurement and return resulting states.

        This method simulates the measurement of specified qubits in a given basis and returns the possible
        post-measurement states of the system.

        Examples:
            >>> state = QuantumState.from_label("000", "111")

            Measure qubit 0 in Z-basis:
            >>> z_states = state.state_after_measurement(measure_bit=[0], target_basis="z--")
            >>> z_states[0].draw()
            |000>
            >>> z_states[1].draw()
            |111>

            Measure qubit 0 in X-basis:
            >>> x_states = state.state_after_measurement(measure_bit=[0], target_basis="x--")
            >>> x_states[0].draw()
            1/√2(|+++> + |+-->)
            >>> x_states[1].draw()
            1/√2(|-+-> - |--+>)

            Measure qubit 0 in Y-basis:
            >>> y_states = state.state_after_measurement(measure_bit=[0], target_basis="y--")
            >>> y_states[0].draw()
            1/√2(|i00> - i|i11>)
            >>> y_states[1].draw()
            1/√2(|j00> + i|j11>)

            Measure qubit 2 in Y-basis:
            >>> y_states = state.state_after_measurement(measure_bit=[2], target_basis="--y")
            >>> y_states[0].draw()
            1/√2(|00i> - i|11i>)
            >>> y_states[1].draw()
            1/√2(|00j> + i|11j>)

            Measure qubits 1 and 2 in X-basis:
            >>> x_states = state.state_after_measurement(measure_bit=[1, 2], target_basis="-xx")
            >>> x_states[0b00].draw()
            |+++>
            >>> x_states[0b01].draw()
            |-+->
            >>> x_states[0b10].draw()
            |--+>
            >>> x_states[0b11].draw()
            |+-->

        Understanding and Using the Results:
            1. List Structure:
            The returned list contains QuantumState objects, each representing a possible
            post-measurement state. The number of states in the list depends on the number
            of measured qubits.

            2. Indexing:
            - For a single qubit measurement (in any basis: Z, X, or Y):
                * states[0]: State corresponding to the measurement result '0'
                * states[1]: State corresponding to the measurement result '1'
            - For multi-qubit measurements:
                The index corresponds to the binary representation of the measurement outcome.
                E.g., for a two-qubit measurement:
                * states[0b00]: Outcome '00'
                * states[0b01]: Outcome '01'
                * states[0b10]: Outcome '10'
                * states[0b11]: Outcome '11'

            3. Basis-Specific Interpretations:
            - Z-basis: '0' represents |0>, '1' represents |1>
            - X-basis: '0' represents |+>, '1' represents |->
            - Y-basis: '0' represents |+i>, '1' represents |-i>

        Args:
            measure_bit (List[int] | str): Indices of qubits to be measured. Can be a list of integers
                or a string of qubit indices (e.g., "01" for qubits 0 and 1).
            target_basis (List[str] | str, optional): Measurement basis for each measured qubit.
                Supported bases are "x", "y", "z". If not specified, Z-basis is used by default.
                Can be a list of strings or a string (e.g., ["x", "z"] or "xz").
            shot (int, optional): Number of measurement simulations to perform. Higher values give
                more accurate probability distributions. Defaults to 100.

        Returns:
            List[QuantumState]: A list of possible post-measurement quantum states. Each state
            represents a possible outcome of the measurement process.
        """
        _, z_basis_system_state_list, _, _, _, _ = self._measurement(
            measure_bit=measure_bit, target_basis=target_basis, shot=shot
        )
        return z_basis_system_state_list

    def _basis_convert(
        self,
        target_basis: list[str] | str = [],
        current_basis: list[str] | str = [],
        algorithm: str = "local",
    ) -> tuple[QuantumState, list[str]]:
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
            (tuple[QuantumState, List[str]]): The converted quantum state and the list of the basis used for conversion.

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

    def _global_min_entropy_basis(self, auto_basis_index: list[int], current_basis: list[str]) -> list[str]:
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

    def _local_min_entropy_basis(self, auto_basis_index: list[int], current_basis: list[str]) -> list[str]:
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

    def _measurement(
        self, measure_bit: list[int] | str, target_basis: list[str] | str = [], shot=-1
    ) -> tuple[list[QuantumState], list[QuantumState], list[QuantumState], list[QuantumState], list[str], list[str]]:
        """Perform a measurement on the quantum state.

        This method measures the specified qubits in the given basis and returns the
        resulting quantum states and measurement outcomes.

        Args:
            measure_bit (List[int] | str): The bits (qubits) to measure. Can be a list
                of indices or a string specifying the bits.
            target_basis (List[str] | str, optional): The basis in which to perform the
                measurement. Defaults to basis with minimum entropy.
            shot (int, optional): The number of measurement shots to perform.
                Defaults to depend on the number of qubits you want to measure. (2^(len(measure_bit) + 2))

        Returns:
            (tuple[list[QuantumState], list[QuantumState], list[QuantumState], list[QuantumState], list[str], list[str]]):
                - z_basis_measure_state_list: Measurement states in the Z basis.
                - z_basis_system_state_list: System states in the Z basis.
                - measure_state_list: Measurement states in the original basis.
                - system_state_list: System states in the original basis.
                - measure_basis: The basis used for the measurement.
                - system_basis: The system basis after conversion.
        """  # noqa: E501
        if shot == -1:
            shot = 2 ** (len(measure_bit) + 2)

        if isinstance(measure_bit, str):
            measure_bit = [int(i) for i in measure_bit]

        converted_state, system_basis = self._basis_convert(
            target_basis=target_basis, current_basis=["z"] * self.num_of_qubit
        )

        # crate empty list for output
        z_basis_measure_state_list: list[QuantumState] = [None] * 2 ** len(measure_bit)
        z_basis_system_state_list: list[QuantumState] = [None] * 2 ** len(measure_bit)
        measure_state_list: list[QuantumState] = [None] * 2 ** len(measure_bit)
        system_state_list: list[QuantumState] = [None] * 2 ** len(measure_bit)

        # TODO: Use mathematical method to get all the measurement results instead of using Qiskit's measure method.
        for _ in range(shot):
            measure_ket, system_state = self._perform_single_shot_measurement(converted_state, measure_bit)
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

    def _perform_single_shot_measurement(
        self, converted_state: QuantumState, measure_bit: list[int]
    ) -> tuple[str, QuantumState]:
        """Perform a single shot measurement on the given quantum state.

        This method measures the specified qubits in the given state and returns
        the measurement result along with the post-measurement system state.

        Args:
            converted_state (QuantumState): The quantum state to measure.
            measure_bit (List[int]): The indices of qubits to measure.

        Returns:
            Tuple[str, QuantumState]: A tuple containing:
                - measure_ket (str): The measurement result as a ket string.
                - system_state (QuantumState): The post-measurement system state.

        Note:
            This method reverses qubit ordering to match Qiskit's notation for measurement,
            and then reverses the result to match standard textbook notation.
        """
        measure_result: tuple[str, Statevector] = Statevector(converted_state.data).measure(
            qargs=[self.num_of_qubit - 1 - i for i in measure_bit]  # REVERSE the order of qubits to fit qiskit notation
        )
        measure_ket: str = measure_result[0][::-1]  # REVERSE the order of qubits to fit textbook notation
        system_state = QuantumState(measure_result[1])
        return measure_ket, system_state
