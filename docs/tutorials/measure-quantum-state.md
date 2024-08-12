# Measuring Quantum States

After creating and manipulating quantum states, the next crucial step in quantum computing is measurement. In this tutorial, we'll learn how to measure quantum states using QIRT's `draw_measurement` function.

## Introduction to Quantum Measurement

In quantum mechanics, measurement plays a fundamental role. When we measure a quantum state, we force it to collapse into one of its basis states. The probability of each outcome is determined by the amplitudes of the quantum state.

## Using `draw_measurement` in QIRT

QIRT provides a powerful `draw_measurement` method that allows you to visualize the measurement results of a quantum state. Let's explore how to use this function.

```python
from QIRT import QuantumState

# Create a quantum state
state = QuantumState.from_label("01","10")  # Creates the state (|01> + |10>) / sqrt(2)

# Measure the state and show the results
state.draw_measurement(measure_bit=[0], target_basis=['z'])
```

\>> Output:

$|\texttt{0}\rangle_{0} : |\texttt{1}\rangle_{1} \\|\texttt{1}\rangle_{0} : |\texttt{0}\rangle_{1} \\$

This code creates a quantum state where the first qubit is in a superposition of |0> and |1>, and the second qubit is in the |0> state. We then perform measurement on the first qubit and visualize the measurement results.

## Understanding the Parameters

Let's break down the parameters of `draw_measurement`:

1. `measure_bit`: Specifies which qubits to measure. For example, [0, 2] would measure the first and third qubits.
1. `show_qubit_index`: Boolean. If True, shows qubit indices in the visualization.
1. `output_length`: Controls how many terms are shown per line in the output.
1. `source`: Boolean. If True, returns the LaTeX source code instead of rendering the output.
1. `target_basis`: Determines the measurement basis for measured qubits and the display basis for unmeasured qubits. This parameter is a list or string where each element corresponds to a qubit in the state.

    - For measured qubits: The corresponding element in `target_basis` determines the measurement basis.
    - For unmeasured qubits: The corresponding element in `target_basis` determines the basis for displaying that qubit's state.

### Examples of `target_basis` Usage

1. Two-qubit state:

    ```python
    state = QuantumState.from_label("00")
    state.draw_measurement(measure_bit=[1], target_basis="zx")
    ```

    In this case:

    - Qubit 1 (second qubit) is measured in the X basis.
    - Qubit 0 (first qubit) is displayed in the Z basis.

1. Four-qubit state:

    ```python
    state = QuantumState.from_label("0000")
    state.draw_measurement(measure_bit=[0, 2], target_basis="xzzx")
    ```

    Here:

    - Qubit 0 is measured in the X basis.
    - Qubit 2 is measured in the Z basis.
    - Qubit 1 is displayed in the Z basis.
    - Qubit 3 is displayed in the X basis.

These examples demonstrate how `target_basis` allows for flexible control over both measurement and display bases for each qubit in the system.

## Interpreting the Results

The `draw_measurement` function provides a visual representation of the measurement outcomes. You'll see:

- The measured states and their probabilities.
- The post-measurement states of the system.

This visualization helps in understanding the probabilistic nature of quantum measurements and how measurement affects the quantum state.

## Next Steps

Now that you've learned how to measure quantum states, you're ready to explore more complex quantum algorithms and protocols. Try creating different quantum states and measuring them in various bases to deepen your understanding of quantum measurement.

For more advanced usage of QIRT's measurement capabilities, check out our [How-To guides](../how-to-guides/index.md).
