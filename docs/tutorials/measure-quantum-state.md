# Measuring Quantum States

After creating and manipulating quantum states, the next crucial step in quantum computing is measurement. In this tutorial, we'll learn how to measure quantum states using QIRT's `draw_measurement` function.

## Introduction to Quantum Measurement

In quantum mechanics, measurement plays a fundamental role. When we measure a quantum state, we force it to collapse into one of its basis states. The probability of each outcome is determined by the amplitudes of the quantum state.

## Using `draw_measurement` in QIRT

QIRT provides a powerful `draw_measurement` method that allows you to visualize the measurement results of a quantum state. Let's explore how to use this function.

```python
from QIRT import QuantumState

# Create a quantum state
state = QuantumState.from_label('+0')  # Creates the state (|00> + |10>) / sqrt(2)

# Measure the state and show the results
state.draw_measurement(measure_bit=[0], shot=1000)
```

\>> Output

This code creates a quantum state where the first qubit is in a superposition of |0> and |1>, and the second qubit is in the |0> state. We then perform measurement on the first qubit and visualize the measurement results.

## Understanding the Parameters

Let's break down the parameters of `draw_measurement`:

- `measure_bit`: Specifies which qubits to measure. In our example, we measured the first qubit ([0]).
- `state_basis`: The basis in which to perform the measurement. Default is the computational (Z) basis.
- `show_qubit_index`: Whether to show qubit indices in the visualization.
- `output_length`: Controls how many terms are shown per line in the output.
- `source`: If True, returns the LaTeX source code instead of rendering the output.

## Measuring in Different Bases

QIRT allows you to measure in different bases. Let's try measuring in the X basis:

```python
x_basis_result = state.draw_measurement(measure_bit=[0], state_basis=['x'], shot=1000)
display(x_basis_result)
```

This will show the measurement results if we measure the first qubit in the X basis.

## Interpreting the Results

The `draw_measurement` function provides a visual representation of the measurement outcomes. You'll see:

- The measured states and their probabilities.
- The post-measurement states of the system.

This visualization helps in understanding the probabilistic nature of quantum measurements and how measurement affects the quantum state.

## Next Steps

Now that you've learned how to measure quantum states, you're ready to explore more complex quantum algorithms and protocols. Try creating different quantum states and measuring them in various bases to deepen your understanding of quantum measurement.

For more advanced usage of QIRT's measurement capabilities, check out our [How-To guides](../how-to-guides/index.md).