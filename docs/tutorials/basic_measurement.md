# Measuring Quantum States

After creating quantum states, the next step is often to measure them. In this tutorial, we'll learn the basics of measuring quantum states using QIRT.

## Introduction to Quantum Measurement

In quantum mechanics, measurement causes a quantum state to collapse into one of its basis states. The probability of each outcome depends on the state's amplitudes.

## Using `draw_measurement` in QIRT

QIRT provides a `draw_measurement` method to visualize measurement results. Let's see a simple example:

```python
from QIRT import QuantumState

# Create a quantum state (|+++> + |--->) / sqrt(2)
state = QuantumState.from_label("+++", "---")

# Measure the first qubit in the Z basis and show the result
state.draw_measurement(measure_bit=[0], target_basis="z")
```

\>> Output:

$|\texttt{0}\rangle_{0} : \frac{\sqrt{2}}{2}|\texttt{00}\rangle_{1,2} +\frac{\sqrt{2}}{2}|\texttt{11}\rangle_{1,2} \\|\texttt{1}\rangle_{0} : \frac{\sqrt{2}}{2}|\texttt{01}\rangle_{1,2} +\frac{\sqrt{2}}{2}|\texttt{10}\rangle_{1,2} \\$

This creates a three-qubit state and measures the first qubit.

## Interpreting the Results

The output shows:

- The possible measurement outcomes
- The state of the system after measurement

This helps us understand how measurement affects quantum states.

## Next Steps

Now that you've seen basic measurement, you can explore more advanced topics:

1. For a deeper dive into visualizing quantum measurements, check our [How-To guide on visualizing quantum measurements](../how_to_guides/visualize_measurements.md). This guide will show you how to use the `draw_measurement` function for complex quantum state measurements visualization.

2. To learn how to obtain and work with post-measurement quantum states, see our [How-To guide on obtaining post-measurement states](../how_to_guides/post_measurement_states.md). This guide covers the use of the `state_after_measurement` function to obtain and analyze quantum states after measurement.

These guides will help you master the intricacies of quantum measurement in QIRT and apply these concepts to more complex quantum systems.
