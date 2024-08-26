# Creating a Basic Quantum Circuit

After creating a basic quantum state $|\texttt{00}\rangle$, the next step is to build a basic quantum circuit.

## Basic Circuit Creation

Let's start by creating a basic quantum circuit with two qubits:

```python
from QIRT import QuantumCircuit

# Create a two-qubit quantum circuit
circuit = QuantumCircuit(2)

# Visualize the empty circuit
circuit.draw()
```

This creates an empty quantum circuit with two qubits.

## Adding Quantum Gates

Now, let's add some gates to our circuit. We'll create a circuit that prepares a Bell state, which is a maximally entangled state of two qubits.

```python
# Add a Hadamard gate on the circuit to qubit 0
circuit.h(0)

# Add a CNOT gate on the circuit with control qubit 0 and target qubit 1
circuit.cx(0, 1)

# Visualize the circuit
circuit.draw()
```

\>> Output:

![bell_state_circ](./imgs/bell_state_circ.png)

This circuit shows:

- A Hadamard gate (H) applied to qubit 0
- A CNOT gate with qubit 0 as the control and qubit 1 as the target

## Understanding the Circuit

1. The Hadamard gate (H) puts the first qubit into a superposition state.
2. The CNOT gate entangles the two qubits.

This particular circuit creates a Bell state, which is a fundamental resource in many quantum information protocols.

## Next Steps

Now that you know how to create basic quantum circuits, you're ready to learn how to apply these circuits to quantum states.

In the next tutorial, [Applying the Quantum Circuit to the Quantum State](apply_circuit.md), you'll see how quantum circuits transform quantum states, bringing together everything you've learned so far.

For more advanced circuit creation techniques, including method chaining and adding custom unitary operators, check out our [How-To Guide on Creating Quantum Circuits](../how_to_guides/create_circuits.md).
