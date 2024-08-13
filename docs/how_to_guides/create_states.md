# Creating Quantum States with Ket Notation and Matrices

QIRT provides multiple powerful methods to create quantum states. This guide covers advanced techniques for state creation, including using coefficients, different bases, and creating states from matrices.

## Creating States from Bra-Ket Notation

### Basic Usage

To create a simple quantum state, you can use string labels:

```python
from QIRT import QuantumState

# Create an equal superposition of |0⟩ and |1⟩
state = QuantumState.from_label("0", "1")
state.draw(target_basis="z")
```

Output: $ \frac{\sqrt{2}}{2}|\texttt{0}\rangle_{0} +\frac{\sqrt{2}}{2}|\texttt{1}\rangle_{0} $

### Multi-Qubit States

You can create multi-qubit states by providing longer string labels:

```python
# Create an equal superposition of all two-qubit states
state = QuantumState.from_label("00", "01", "10", "11")
state.draw(target_basis="zz")
```

Output: $ \frac{1}{2}|\texttt{00}\rangle_{01} +\frac{1}{2}|\texttt{01}\rangle_{01} +\frac{1}{2}|\texttt{10}\rangle_{01} +\frac{1}{2}|\texttt{11}\rangle_{01} $

### Using Different Bases

QIRT supports different bases (X, Y, Z) in state creation:

```python
# Create a state in the X-basis
state = QuantumState.from_label("+", "-")
state.draw(target_basis="x")
```

Output: $ \frac{\sqrt{2}}{2}|\texttt{+}\rangle_{0} + \frac{\sqrt{2}}{2}|\texttt{-}\rangle_{0} $

### States with Coefficients

You can specify complex coefficients for each ket:

```python
# Create a state with specific coefficients
state = QuantumState.from_label("0", (-1, "1"))
state.draw(target_basis="z")
```

Output: $ \frac{\sqrt{2}}{2}|\texttt{0}\rangle_{0} - \frac{\sqrt{2}}{2}|\texttt{1}\rangle_{0} $

```python
# Create a state with complex coefficients
state = QuantumState.from_label("0", (1j, "1"))
state.draw(target_basis="z")
```

Output: $ \frac{\sqrt{2}}{2}|\texttt{0}\rangle_{0} +\frac{\sqrt{2} i}{2}|\texttt{1}\rangle_{0} $

## Creating States from Matrices

QIRT also allows you to create quantum states by directly providing the state vector as a list or numpy array.

```python
import numpy as np
from QIRT import QuantumState

# Create a quantum state |00> from matrix
state_00 = QuantumState([1, 0, 0, 0])

# Create a quantum state |11> from numpy array
state_11 = QuantumState(np.array([0, 0, 0, 1]))

# Create a Bell state (|00> + |11>) / sqrt(2)
bell_state = QuantumState([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])

# Visualize the Bell state
bell_state.draw()
```

Output: $ \frac{\sqrt{2}}{2}|\texttt{00}\rangle_{01} + \frac{\sqrt{2}}{2}|\texttt{11}\rangle_{01} $

## Notes on Usage

- Coefficients can be real or complex numbers.
- The method supports various notations: computational basis (0,1), X-basis (+,-), and Y-basis (i,j).
- For multi-qubit states, use concatenated labels (e.g., "00", "01").
- The resulting state is always normalized.
- When creating states from matrices, ensure the vector is normalized and has the correct dimension (2^n for n qubits).
