# Setup

To get started with QIRT, you'll need to install it on your system. This tutorial will guide you through the installation process.

## Prerequisites

QIRT requires Python 3.10 or later. Make sure you have a compatible version of Python installed on your system.

## Installing QIRT

You can install QIRT using pip, Python's package installer. Open your terminal or command prompt and run the following command:

```bash
pip install QIRT
```

This command will download and install QIRT along with its dependencies.

## Verifying the Installation

To verify that QIRT has been installed correctly, you can import it in a Python environment:

```python
import QIRT

print(QIRT.__version__)
```

If this runs without any errors and prints the version number, you've successfully installed QIRT!

## **Setting up jupyter notebook**

We recommend using Jupyter Notebook for the best experience with QIRT. Here's how to set it up:

1. Install Jupyter:

    ```bash
    pip install jupyter
    ```

2. Launch Jupyter Notebook:

    ```bash
    jupyter notebook
    ```

3. Create a new notebook and you're ready to start!

## Next Steps

Now that you have QIRT installed and Jupyter Notebook set up, you're ready to dive into quantum computing with QIRT! Here are the next tutorials to guide you through the basics:

1. [Create a Quantum State](create-quantum-state.md): Learn how to create and visualize quantum states using QIRT.

2. [Create a Quantum Circuit](create-quantum-circuit.md): Explore how to build quantum circuits with gates like Hadamard and CNOT.

3. [Apply a Quantum Circuit to a Quantum State](apply-circuit-to-state.md): Discover how to apply quantum circuits to quantum states and observe the results.