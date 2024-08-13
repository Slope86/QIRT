# Customizing Ket Notation with Configuration File

QIRT allows you to customize the ket notation using a configuration file. This feature enables you to adapt the notation to your preferences or to match specific conventions in your work.

## Configuration File Location

The configuration file is located at:

```txt
~/.QIRT/config.ini
```

in your home directory.

## Default Configuration

Here's an example of the default configuration:

```ini
[ket]
z0 = 0
z1 = 1
x0 = +
x1 = -
y0 = i
y1 = j
```

This configuration defines how different basis states are represented:

- `z0` and `z1` represent the computational basis states
- `x0` and `x1` represent the X-basis states
- `y0` and `y1` represent the Y-basis states

## Customizing the Notation

To customize the ket notation:

1. Open the `config.ini` file in a text editor.
2. Modify the values for each basis state as desired.
3. Save the file.

For example, if you prefer to use "r" and "l" for the Y-basis states, you could modify the configuration like this:

```ini
[ket]
z0 = 0
z1 = 1
x0 = +
x1 = -
y0 = r
y1 = l
```

## Applying Changes

After making changes to the configuration file, you must restart your Jupyter kernel or Python interpreter for the changes to take effect. This ensures that QIRT loads the updated configuration properly.

## Usage Example

After customizing the notation, your quantum states will be represented using the new notation:

```python
from QIRT import QuantumState

state = QuantumState.from_label("r", "l")
state.draw(target_basis="y")
```

With the custom configuration above, this would output:

$ \frac{\sqrt{2}}{2}|\texttt{r}\rangle_{0} +\frac{\sqrt{2}}{2}|\texttt{l}\rangle_{0} $
