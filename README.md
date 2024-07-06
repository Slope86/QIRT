# Quantum Information Research Toolkit

A quantum information research toolkit based on Qiskit.

## Introduction

The Quantum Information Research Toolkit (QIRT) is designed to facilitate research and development in quantum information science using the Qiskit framework. This toolkit provides essential classes and functions to create and manipulate quantum states and operations effectively.

## Installation

### Option 1: Install from PyPI

To install QIRT from PyPI, use the following command:

```bash
pip install QIRT
```

### Option 2: Install from Source

To install QIRT from the source, follow these steps:

```bash
git clone --depth 1 https://github.com/Slope86/QIRT
cd QIRT
pip install .
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
state00 = QuantumState.from_label('00')
```

### Visualizing the Quantum State

Once you have created a quantum state, you can visualize it using the `draw` method. Here is how you can visualize the quantum state `state00`:

```python
# Draw the quantum state
state00.draw()
```

## Configuration

The configuration file for QIRT is located at `~/QIRT/config/config.ini`. This file allows you to customize various settings for the toolkit.

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

This configuration file allows you to customize the notation for quantum states and the border width of LaTeX output images. Adjust these settings according to your preferences.

## Requirement

Python >= 3.10  
qiskit[visualization] == 1.1.0  

## License

This QiskitExtension project is open source under the MIT license.
However, the extensions that are installed separately are not part of the QiskitExtension project.
They all have their own licenses!
