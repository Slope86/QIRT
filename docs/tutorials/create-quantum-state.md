# Create a Quantum State

First, let's start with the basics of QIRT: creating a quantum state $|\texttt{00}\rangle$. In QIRT, there are multiple ways to create a quantum state. We'll explore two common methods: creating from a matrix and using bra-ket notation.

## From Matrix

QIRT allows you to create a quantum state by directly providing the state vector as a list or numpy array.

```python
from QIRT import QuantumState

# Create a quantum state |00> from matrix
state = QuantumState([1, 0, 0, 0])

# Visualize the state
state.draw()
```

\>> Output: $|\texttt{00}\rangle_{01}$

This creates a quantum state $|\texttt{00}\rangle$ where both qubits are in the $|0\rangle$ state.

## From Bra-Ket Notation

QIRT also provides a convenient method to create quantum states using bra-ket notation through the `from_label` method.

```python
from QIRT import QuantumState

# Create a quantum state |00> from bra-ket notation
state = QuantumState.from_label("00")

# Visualize the state
state.draw()
```

\>> Output: $|\texttt{00}\rangle_{01}$

This also creates the quantum state $|\texttt{00}\rangle$, but using a more intuitive notation.

The `from_label` method is versatile and can create various states:

```python
# Create |01> state
state_01 = QuantumState.from_label("01")

# Create |+> state (superposition of |0> and |1>)
state_plus = QuantumState.from_label("+")

# Create |-i> state (Y-basis state)
state_minus_i = QuantumState.from_label("j")  # Note: 'j' represents -i in QIRT notation
```

## Next Steps

Now that you've learned how to create quantum states, you're ready to move on to more advanced operations. The next tutorial will show you how to [Create a Quantum Circuit](creating-quantum-circuit.md), where you'll learn how to apply quantum gates to manipulate these states.
