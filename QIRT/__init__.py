"""Quantum Information Research Toolkit

The Quantum Information Research Toolkit (QIRT) provides enhanced functionalities
for working with quantum circuits and state vectors, extending the capabilities
of Qiskit's QuantumCircuit and Statevector classes. QIRT includes modules for
basis conversion, state vector manipulations, and various visualizations in LaTeX.

Modules:
    quantum_operation: Extends Qiskit's QuantumCircuit class with additional methods
                       for basis conversion and visualization.
    quantum_state: Extends Qiskit's Statevector class with methods for state manipulations,
                   basis conversions, and visualizations.

The functionalities added in QIRT are:

- Conversion of quantum circuits to matrix form.\n
- Drawing quantum circuits or their matrix representations.\n
- Basis conversion for qubits within circuits.\n
- Creation and manipulation of state vectors.\n
- Calculation of quantum state entropy.\n
- Evolution of quantum states using various operators.\n
- Visualization of quantum states in LaTeX or matrix form.\n
- Measurement of qubits and obtaining resulting states.\n

See Also:
    [Qiskit QuantumCircuit documentation](https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.html)\n
    [Qiskit Statevector documentation](https://qiskit.org/documentation/stubs/qiskit.quantum_info.Statevector.html)
"""

from .quantum_circuit import QuantumCircuit
from .quantum_state import QuantumState

__all__ = ["QuantumCircuit", "QuantumState"]
