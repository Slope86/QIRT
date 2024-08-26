# Visualizing Quantum Measurement Results

This guide covers advanced usage of QIRT's `draw_measurement` function for visualizing quantum state measurements.

## Detailed Parameters of `draw_measurement`

The `draw_measurement` function in QIRT is highly customizable. Here's a breakdown of its parameters:

1. `measure_bit`: List of integers specifying which qubits to measure. For example, [0, 2] would measure the first and third qubits.

2. `show_qubit_index`: Boolean. When True, qubit indices are shown in the visualization.

3. `output_length`: Integer controlling how many terms are shown per line in the output.

4. `source`: Boolean. When True, returns the LaTeX source code instead of rendering the output.

5. `target_basis`: List or string determining the measurement basis for measured qubits and the display basis for unmeasured qubits. Each element corresponds to a qubit in the state.

## Advanced Usage of `target_basis`

The `target_basis` parameter is particularly powerful. Let's explore its usage with examples:

### Example 1: Two-qubit state

```python
state = QuantumState.from_label("+-")
state.draw_measurement(measure_bit=[1], target_basis="zx")
```

\>> Output: $|\texttt{-}\rangle_{1} : \frac{\sqrt{2}}{2}|\texttt{0}\rangle_{0} +\frac{\sqrt{2}}{2}|\texttt{1}\rangle_{0} \\$

Here:

- Qubit 1 (second qubit) is measured in the X basis.
- Qubit 0 (first qubit) is displayed in the Z basis.

### Example 2: Four-qubit state

```python
state = QuantumState.from_label("+-+0")
state.draw_measurement(measure_bit=[0, 2], target_basis="xzzy")
```

\>> Output:

$|\texttt{+0}\rangle_{02} : \frac{\sqrt{2}}{2}|\texttt{0i}\rangle_{13} +\frac{\sqrt{2}}{2}|\texttt{0j}\rangle_{13} \\|\texttt{-0}\rangle_{02} : \frac{\sqrt{2}}{2}|\texttt{0i}\rangle_{13} +\frac{\sqrt{2}}{2}|\texttt{0j}\rangle_{13} \\$

Here:

- Qubit 0 is measured in the X basis.
- Qubit 2 is measured in the Z basis.
- Qubit 1 is displayed in the Z basis.
- Qubit 3 is displayed in the Y basis. (Note: In the Y basis, the default ket notation uses |i⟩ and |j⟩ to represent |+i⟩ and |-i⟩ respectively.)

## Interpreting Complex Measurement Results

The output of `draw_measurement` provides a wealth of information:

1. Measurement outcomes: The possible states after measurement.
2. Probabilities: The likelihood of each outcome.
3. Post-measurement states: The state of unmeasured qubits after measurement.

For example, in a three-qubit system where we measure the first qubit:

```python
state = QuantumState.from_label("000", "111")
state.draw_measurement(measure_bit=[0])
```

The output might look like:

$|\texttt{0}\rangle_{0} : |\texttt{00}\rangle_{12}\\
|\texttt{1}\rangle_{0} : |\texttt{11}\rangle_{12}$

This tells us:

- There's a 50% chance of measuring |0⟩ in the first qubit, leaving the other qubits in state |00⟩.
- There's a 50% chance of measuring |1⟩ in the first qubit, leaving the other qubits in state |11⟩.

## Conclusion

Mastering `draw_measurement` allows for deep exploration of quantum measurement phenomena. Experiment with different states, measurement configurations, and bases to gain intuition about quantum behavior.

Remember, quantum measurement is probabilistic and can dramatically alter the state of a system. Use these tools to visualize and understand these complex quantum effects.
