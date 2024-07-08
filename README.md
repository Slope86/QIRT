# QIRT - Quantum Information Research Toolkit (WIP)

A quantum information research toolkit based on Qiskit. **This project is currently a Work in Progress (WIP) and is not yet complete. Features and documentation may be incomplete.**

## Introduction

The Quantum Information Research Toolkit (QIRT) is designed to facilitate research and development in quantum information science using the Qiskit framework. This toolkit provides essential classes and functions to create and manipulate quantum states and operations effectively.

## Quick start

QIRT can be installed using pip:

```bash
pip install QIRT
```

## Usage

### Importing the Toolkit

To start using the Quantum Information Research Toolkit, import the necessary modules as shown below:

```python
from QIRT import QuantumState, QuantumOperation
```

- **QuantumState**: This class allows you to create and manage quantum states. It provides various methods to initialize, transform, and measure quantum states.
- **QuantumOperatio**: This class provides a set of operations that can be applied to quantum states. It includes methods for unitary operations, measurements, and other quantum operations.

### Creating a Quantum State

To create a quantum state, you can use the `from_label` method provided by the `QuantumState` class. Below is an example of how to create a quantum state labeled '00':

```python
# Create a quantum state labeled '00'
init_state = QuantumState.from_label('00')
```

### Visualizing the Quantum State

Once you have created a quantum state, you can visualize it using the `draw` method. Here is how you can visualize the quantum state `init_state`:

```python
# Draw the quantum state
init_state.draw()
```

## Creating a Quantum Operation

## Configuration

The configuration file for QIRT is located in the user's home directory under `~/.QIRT/config.ini`. This file allows you to customize various settings for the toolkit.

The default configuration file is as follows:

```ini
; This section sets up the notation for the StateVector (affects the visualization result and the constructor function from_label()).
; The default notation uses |j> to represent |-i>. 
; You can change the notation to another character if necessary. (only accepts single characters.)
[ket]
z0 = 0
z1 = 1
x0 = +
x1 = -
y0 = i
y1 = j
```

## Requirement

Python >= 3.10  
qiskit[visualization] == 1.1.0  

## License

This QIRT project is open source under the MIT license.
However, the extensions that are installed separately are not part of the QIRT project.
They all have their own licenses!
