# QIRT - Quantum Information Research Toolkit

A quantum information research toolkit based on Qiskit, designed to facilitate research and development in quantum information science.

## Quick Start

1. Install QIRT using pip:

    ```bash
    pip install QIRT
    ```

2. Set up Jupyter Notebook (if not already installed):

    ```bash
    pip install jupyter
    jupyter notebook
    ```

## Basic Usage in Jupyter Notebook

Create a new notebook and run the following:

```python
from QIRT import QuantumState, QuantumCircuit

# Create a quantum state
state = QuantumState.from_label('00')

# Visualize the state
state.draw()

# Create a quantum circuit
circuit = QuantumCircuit(2)
circuit.h(0)  # Apply Hadamard gate to the first qubit
circuit.cx(0, 1)  # Apply CNOT gate

# Apply circuit to state
final_state = state.apply(circuit)
final_state.draw()
```

## Documentation

For detailed documentation, tutorials, and how-to guides, visit our [documentation website](https://slope86.github.io/QIRT/).

- [Tutorials](https://slope86.github.io/QIRT/tutorials): Learn the basics of QIRT with hands-on examples.
- [How-To Guides](https://slope86.github.io/QIRT/how_to_guides): Detailed instructions for specific tasks.
- [API Reference](https://slope86.github.io/QIRT/reference): Detailed descriptions of QIRT functions, classes, and modules.

## Requirements

- Python >= 3.10
- qiskit[visualization] >= 1.1.0
- IPython >= 8.24.0
- Jupyter Notebook (for visualization)

## Configuration

QIRT can be configured using `~/.QIRT/config.ini`. See the [documentation](https://slope86.github.io/QIRT/how_to_guides/customize_ket_notation/) for more details.

## License

This project is open source under the MIT license. Note that separately installed extensions are not part of the QIRT project and have their own licenses.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/slope86/QIRT/issues) on our GitHub repository.
