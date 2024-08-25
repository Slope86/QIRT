# Applying the Quantum Circuit to the Quantum State

After created a basic quantum circuit, the next step is to apply the circuit to the quantum state we created in step 1. This process is fundamental to quantum computing, as it allows you to manipulate and transform quantum states using the gates defined in your circuit. In this tutorial, we'll apply a quantum circuit to a quantum state to create a Bell state.

## Preparing the Initial State and Circuit

Let's start by creating our initial quantum state and the quantum circuit we'll apply to it:

```python
from QIRT import QuantumState, QuantumCircuit

# Initialize the quantum state |00>
init_state = QuantumState.from_label('00')

# Create a two-qubit quantum circuit and add gates using method chaining
circuit = QuantumCircuit(2).h(0).cx(0, 1)
```

Here's what we've done:

1. Created an initial state $|\texttt{00}\rangle$ using the `from_label` method.
1. Created a quantum circuit with two qubits.
1. Added a Hadamard gate (H) to the first qubit (index 0).
1. Added a CNOT gate with the first qubit as control and the second as target.

## Applying the Quantum Circuit to the Quantum State

Now, let's apply the quantum circuit to the initial quantum state $|\texttt{00}\rangle$, creating a Bell state:

```python
# Apply the quantum circuit to the quantum state
Bell_state = init_state.apply(circuit)

# Visualize the Bell state
Bell_state.draw()
```

\>> Output: $\frac{\sqrt{2}}{2}|\texttt{00}\rangle_{01} + \frac{\sqrt{2}}{2}|\texttt{11}\rangle_{01} $

Now you have transformed the quantum state $|\texttt{00}\rangle$ into a Bell state $\frac{1}{\sqrt{2}}(|\texttt{00}\rangle + |\texttt{11}\rangle)$ using the quantum circuit.

## Understanding the Result

The resulting state is a Bell state, which is one of the four maximally entangled two-qubit states. This state is crucial in many quantum information protocols, such as quantum teleportation and superdense coding.

1. The Hadamard gate (H) puts the first qubit into a superposition state.
2. The CNOT gate entangles the two qubits, resulting in the Bell state.

## Next Steps

Congratulations! You have now learned how to apply a quantum circuit to a quantum state.

To learn about measuring quantum states, proceed to our next tutorial: [Measuring Quantum States](basic_measurement.md). This tutorial will teach you how to perform measurements on your quantum states and interpret the results.

For more advanced usage, check out our [How-To guides](../how_to_guides/index.md). These guides provide step-by-step instructions for specific tasks and use cases.
