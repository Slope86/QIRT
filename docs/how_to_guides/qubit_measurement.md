# Qubit Measurement

This guide covers advanced usage of QIRT's `draw_measurement` function for quantum state measurement. We'll explore the function's parameters in depth and look at complex examples.

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

In this case:

- Qubit 1 (second qubit) is measured in the X basis.
- Qubit 0 (first qubit) is displayed in the Z basis.

### Example 2: Four-qubit state

```python
state = QuantumState.from_label("+-+0")
state.draw_measurement(measure_bit=[0, 2], target_basis="xzzx")
```

Here:

- Qubit 0 is measured in the X basis.
- Qubit 2 is measured in the Z basis.
- Qubit 1 is displayed in the Z basis.
- Qubit 3 is displayed in the X basis.

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

$|\texttt{0}\rangle_{0} : |\texttt{00}\rangle_{12} (50\%) \\
|\texttt{1}\rangle_{0} : |\texttt{11}\rangle_{12} (50\%)$

This tells us:

- There's a 50% chance of measuring |0⟩ in the first qubit, leaving the other qubits in state |00⟩.
- There's a 50% chance of measuring |1⟩ in the first qubit, leaving the other qubits in state |11⟩.

## Advanced Measurement Scenarios

### Partial Measurement of Entangled States

Consider the GHZ state:

```python
ghz = QuantumState.from_label("000", "111")
ghz.draw_measurement(measure_bit=[0, 1], target_basis="zx")
```

This measures the first qubit in the Z basis and the second in the X basis, demonstrating how entanglement affects measurement outcomes.

### Measuring in Different Bases

```python
state = QuantumState.from_label("+", "-")
state.draw_measurement(measure_bit=[0, 1], target_basis="xy")
```

This measures a two-qubit state where the first qubit is in the X basis and the second in the Y basis, showcasing how measurement basis affects outcomes.

## Conclusion

Mastering `draw_measurement` allows for deep exploration of quantum measurement phenomena. Experiment with different states, measurement configurations, and bases to gain intuition about quantum behavior.

Remember, quantum measurement is probabilistic and can dramatically alter the state of a system. Use these tools to visualize and understand these complex quantum effects.
