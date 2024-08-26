# Measuring Quantum States

After creating quantum states, the next step is often to measure them. In this tutorial, we'll learn the basics of measuring quantum states using QIRT.

## Introduction to Quantum Measurement

In quantum mechanics, measurement causes a quantum state to collapse into one of its basis states. The probability of each outcome depends on the state's amplitudes.

## Using `draw_measurement` in QIRT

QIRT provides a `draw_measurement` method to visualize measurement results. Let's see a simple example:

```python
from QIRT import QuantumState

# Create a quantum state
state = QuantumState.from_label("01","10")  # Creates the state (|01> + |10>) / sqrt(2)

# Measure the state and show the results
state.draw_measurement(measure_bit=[0])
```

\>> Output:

$|\texttt{0}\rangle_{0} : |\texttt{1}\rangle_{1} \\|\texttt{1}\rangle_{0} : |\texttt{0}\rangle_{1} \\$

This code creates a two-qubit state and measures the first qubit.

## Interpreting the Results

The output shows:

- The possible measurement outcomes
- The state of the system after measurement

This helps us understand how measurement affects quantum states.

## Next Steps

Now that you've seen basic measurement, try creating different states and measuring them. For more advanced usage, check our [How-To guide on quantum measurement](../how_to_guides/qubit_measurement.md).
