# Obtaining Post-Measurement Quantum States

This guide covers the usage of QIRT's `state_after_measurement` function for obtaining post-measurement quantum states.

## Using `state_after_measurement` Function

The `state_after_measurement` function allows you to simulate quantum measurements and obtain the resulting post-measurement states. This is particularly useful when you need to work with or analyze the quantum states after a measurement has been performed.

### Function Signature

```python
def state_after_measurement(
    self, measure_bit: list[int] | str, target_basis: list[str] | str = [], shot=100
) -> list[QuantumState]:
```

### Parameters

1. `measure_bit`: List of integers or string specifying which qubits to measure. For example, [0, 2] or "02" would measure the first and third qubits.

2. `target_basis`: List or string determining the measurement basis for measured qubits. Each element corresponds to a measured qubit. Default is Z-basis for all measured qubits.

3. `shot`: Number of measurement simulations to perform. Higher values give more accurate probability distributions. Defaults to 100.

### Return Value

The function returns a list of `QuantumState` objects, each representing a possible post-measurement state.

### Examples

Let's explore some examples to understand how to use `state_after_measurement`:

#### Example 1: Single Qubit Measurement in Different Bases

```python
state = QuantumState.from_label("000", "111")  # (|000> + |111>)/√2

# Z-basis measurement of qubit 0
z_states = state.state_after_measurement(measure_bit=[0], target_basis="z--")
z_states[0].draw()  # |000>
z_states[1].draw()  # |111>

# X-basis measurement of qubit 0
x_states = state.state_after_measurement(measure_bit=[0], target_basis="x--")
x_states[0].draw()  # 1/√2(|+++> + |+-->)
x_states[1].draw()  # 1/√2(|-+-> - |--+>)

# Y-basis measurement of qubit 0
y_states = state.state_after_measurement(measure_bit=[0], target_basis="y--")
y_states[0].draw()  # 1/√2(|i00> - i|i11>)
y_states[1].draw()  # 1/√2(|j00> + i|j11>)
```

#### Example 2: Multi-Qubit Measurement

```python
# Measure qubits 1 and 2 in X-basis
x_states = state.state_after_measurement(measure_bit=[1, 2], target_basis="-xx")
x_states[0b00].draw()  # |+++>
x_states[0b01].draw()  # |-+->
x_states[0b10].draw()  # |--+>
x_states[0b11].draw()  # |+-->
```

### Understanding the Results

1. The returned list contains `QuantumState` objects, each representing a possible post-measurement state.

2. For a single qubit measurement:
    - `states[0]`: State corresponding to the measurement result '0'
    - `states[1]`: State corresponding to the measurement result '1'

3. For multi-qubit measurements, the index corresponds to the binary representation of the measurement outcome. For example, in a two-qubit measurement:
    - `states[0b00]`: Outcome '00'
    - `states[0b01]`: Outcome '01'
    - `states[0b10]`: Outcome '10'
    - `states[0b11]`: Outcome '11'

4. The basis-specific interpretations are:
    - Z-basis: '0' represents |0>, '1' represents |1>
    - X-basis: '0' represents |+>, '1' represents |->
    - Y-basis: '0' represents |+i>, '1' represents |-i>

## Conclusion

The `state_after_measurement` function provides a powerful tool for exploring post-measurement quantum states. It allows for a comprehensive analysis of quantum measurement phenomena, enabling deeper insights into quantum behavior and facilitating the development and testing of quantum algorithms.
