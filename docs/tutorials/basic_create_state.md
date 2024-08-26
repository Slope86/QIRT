# Creating a Basic Quantum State

Let's start with the basics of QIRT: creating a simple quantum state. We'll focus on creating the state $|\texttt{00}\rangle$ using bra-ket notation.

## Using Bra-Ket Notation

QIRT provides a convenient method to create quantum states using bra-ket notation through the `from_label` method.

```python
from QIRT import QuantumState

# Create a quantum state |00> from bra-ket notation
state = QuantumState.from_label("00")

# Visualize the state
state.draw()
```

\>> Output: $|\texttt{00}\rangle_{01}$

This creates the quantum state $|\texttt{00}\rangle$, where both qubits are in the $|0\rangle$ state.

You can also create other simple states:

```python
# Create |01> state
state_01 = QuantumState.from_label("01")

# Create |1> state (single qubit)
state_1 = QuantumState.from_label("1")
```

## Visualizing Quantum States

As you've seen, we used the `draw()` method to visualize our quantum states. This method provides a basic representation of the state. For more advanced visualization options, including different output formats and customization, please refer to our [How-To Guide on Visualizing Quantum States](../how_to_guides/visualize_states.md).

## Next Steps

Now that you've learned how to create and visualize basic quantum states, you're ready to move on to more advanced operations.

The next tutorial will show you how to [Create a Quantum Circuit](basic_create_circuit.md), where you'll learn how to apply quantum gates to manipulate these states.

For more advanced state creation techniques, including creating states from matrices and using coefficients, check out our [How-To Guide on Creating Quantum States](../how_to_guides/create_states.md).
