# **Tutorials**

Welcome to the Quantum Information Research Toolkit (QIRT) tutorials. This guide will help you get started with QIRT and explore its features.

## **Installation**

To install QIRT, you need Python 3.10 or later. Use pip to install the package:

```bash
pip install QIRT
```

## **Setting up your environment**

We recommend using Jupyter Notebooks for the best experience with QIRT. Here's how to set it up:

1. Install Jupyter:

    ```bash
    pip install jupyter
    ```

2. Launch Jupyter Notebook:

    ```bash
    jupyter notebook
    ```

3. Create a new notebook and you're ready to start!

## **Basic usage**

Let's start with the basics of QIRT:

```python
from QIRT import QuantumState, QuantumCircuit

# Create a quantum state
state = QuantumState.from_label('00')

# Visualize the state
state.draw()
```

Output:
$|\texttt{00}\rangle_{01}$

## **Working with quantum states**

QIRT provides various methods to manipulate quantum states:

```python
# Create a superposition state
superposition = QuantumState.from_label('+0')

# Measure the state
measurement_result = superposition.measure()
print(f"Measurement result: {measurement_result}")

# Apply a transformation
transformed_state = superposition.apply_gate('H', target_qubit=1)
print(f"Transformed state: {transformed_state}")
```

## **Quantum circuit**

Use the `QuantumCircuit` class to apply quantum operations to your quantum states:

```python
# Create a quantum circuit
op = QuantumCircuit()

# Apply a Hadamard gate
op.h(0)

# Apply a CNOT gate
op.cx(0, 1)

# Apply the operation to a state
initial_state = QuantumState.from_label('00')
final_state = op.apply_to(initial_state)
print(f"Final state after operations: {final_state}")
```

## **Visualization**

QIRT provides powerful visualization tools:

```python
# Visualize a quantum state
state = QuantumState.from_label('++')
state.draw()

# Visualize a quantum operation
op = QuantumCircuit()
op.h(0)
op.cx(0, 1)
op.draw()
```

Certainly! Here's a polished version of the Configuration section:

## **Configuration**

QIRT utilizes a configuration file to customize the ket notation. This file is located at `~/.QIRT/config.ini` in your home directory. You can modify the ket notation by editing the `config.ini` file. Here's an example of the default configuration:

```ini
[ket]
z0 = 0
z1 = 1
x0 = +
x1 = -
y0 = i
y1 = j
```

This configuration defines how different basis states are represented:

- `z0` and `z1` represent the computational basis states
- `x0` and `x1` represent the X-basis states
- `y0` and `y1` represent the Y-basis states

Feel free to adjust these values to match your preferred notation or to align with specific conventions in your work.

**Note:** After making changes to the configuration file, you must restart your Jupyter kernel or Python interpreter for the changes to take effect. This ensures that QIRT loads the updated configuration properly.

## **Custom quantum gates**

You can define custom quantum gates:

```python
import numpy as np
from QIRT import QuantumCircuit

# Define a custom gate matrix
custom_matrix = np.array([[0, 1], [1, 0]])  # X gate

# Create a quantum operation with the custom gate
op = QuantumCircuit()
op.unitary(custom_matrix, [0], label='CustomX')

# Visualize
op.draw()
```

For more advanced usage and detailed API documentation, please refer to our [API Reference](./reference.md).

Happy quantum computing with QIRT!
