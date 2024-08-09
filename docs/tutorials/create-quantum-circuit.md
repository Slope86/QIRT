# Create a Quantum Circuit

After learning how to create quantum states, the next step is to understand how to build quantum circuits. Quantum circuits are sequences of quantum gates that manipulate quantum states. In this tutorial, we'll create a simple quantum circuit using QIRT.

## Basic Circuit Creation

Let's start by creating a quantum circuit with two qubits:

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

![bell_state_circ](./bell_state_circ.png)

This circuit shows:

- A Hadamard gate (H) applied to qubit 0
- A CNOT gate with qubit 0 as the control and qubit 1 as the target

## Understanding the Circuit

1. The Hadamard gate (H) puts the first qubit into a superposition state.
2. The CNOT gate entangles the two qubits.

This particular circuit creates a Bell state, which is a fundamental resource in many quantum information protocols.

## Method Chaining

QIRT's `QuantumCircuit` class supports method chaining, which allows you to build circuits more concisely. Here is how you can create the same Bell state circuit using method chaining:

```python
# Create a two-qubit quantum circuit and add gates using method chaining
circuit = QuantumCircuit(2).h(0).cx(0, 1)

# Visualize the circuit
circuit.draw()
```

\>> Output:

![bell_state_circ](./bell_state_circ.png)

Method chaining can make your code cleaner and more readable, especially for constructing more complex circuits.

## Finding More Quantum Gates

QIRT provides support for many different quantum gates. To explore all available gates and their usage, you can refer to the [Qiskit Circuit Library](https://docs.quantum.ibm.com/api/qiskit/circuit_library). QIRT is built on top of Qiskit, which is a comprehensive and widely-used framework for quantum computing. The Qiskit Circuit Library includes detailed documentation on various quantum gates, their parameters, and usage examples, making it an excellent resource for understanding how to use these gates in your circuits.

## Next Steps

Now that you know how to create quantum circuits, you're ready to learn how to apply these circuits to quantum states. In the next tutorial, [Applying a Quantum Circuit to a Quantum State](applying-circuit-to-state.md), you'll see how quantum circuits transform quantum states, bringing together everything you've learned so far.
