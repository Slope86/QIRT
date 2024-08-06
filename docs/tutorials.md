# **Tutorials**

Welcome to the Quantum Information Research Toolkit (QIRT) tutorials. This guide will help you get started with QIRT and explore its features.

## **Installation**

To install QIRT, you need Python 3.10 or later. Use pip to install the package:

```bash
pip install QIRT
```

## **Setting up jupyter notebook**

We recommend using Jupyter Notebook for the best experience with QIRT. Here's how to set it up:

1. Install Jupyter:

    ```bash
    pip install jupyter
    ```

2. Launch Jupyter Notebook:

    ```bash
    jupyter notebook
    ```

3. Create a new notebook and you're ready to start!

## **Creating a quantum state**

First let's start with the basics of QIRT,  creating a quantum state $|\texttt{00}\rangle$:

```python
from QIRT import QuantumState, QuantumCircuit

# Create a quantum state |00>
init_state = QuantumState.from_label('00')

# Visualize the state
init_state.draw()
```

The output will be:

$|\texttt{00}\rangle_{01}$

Showing the quantum state $|\texttt{00}\rangle$ with qubit number labels 0 and 1.

## **Creating a quantum circuit**

Next, let's create a quantum circuit with a Hadamard gate and a CNOT gate:

```python
# Create a two bit quantum circuit
circuit = QuantumCircuit(2)

# Add a Hadamard gate on the circuit to qubit 0
circuit.h(0)

# Add a CNOT gate on the circuit with control qubit 0 and target qubit 1
circuit.cx(0, 1)

# Visualize the circuit
circuit.draw()
```

The output will be:

![bell_state_circ](.\imgs\bell_state_circ.png)

Showing the quantum circuit with a Hadamard gate on qubit 0 and a CNOT gate with control qubit 0 and target qubit 1.

## **Applying the quantum circuit to the quantum state**

Now, let's apply the quantum circuit to the quantum state $|\texttt{00}\rangle$, creating a Bell state:

```python
# Apply the quantum circuit to the quantum state
Bell_state = init_state.apply(circuit)

# Visualize the Bell state
Bell_state.draw()
```

The output will be:

$\frac{\sqrt{2}}{2}|\texttt{00}\rangle_{01} + \frac{\sqrt{2}}{2}|\texttt{11}\rangle_{01} $

Now you have turned the quantum state $|\texttt{00}\rangle$ into a Bell state $\frac{1}{\sqrt{2}}(|\texttt{00}\rangle + |\texttt{11}\rangle)$ using the quantum circuit.

For more advanced usage, check out our [How-To guides](./how-to-guides.md), and for the detailed API documentation, please refer to our [API Reference](./reference.md).

Happy quantum computing with QIRT!
