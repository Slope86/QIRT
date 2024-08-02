"""Utils module for QIRT package.

This module provides various utility functions and classes used throughout the Quantum Information
Research Toolkit (QIRT). These utilities include string manipulation, mathematical operations,
quantum state notations, and extended numpy operations for quantum computations.

Modules:
    find_nth_substring: Contains a function to find the nth occurrence of a substring in a string.
    float_gcd: Contains a function to compute the greatest common divisor (GCD) for floating-point numbers.
    ket: Contains the Ket class to manage and validate custom ket notations for quantum states.
    np_extension: Contains extended numpy functions for quantum computations, such as inverse tensor and tensor product.
"""

from .find_nth_substring import find_nth_substring
from .float_gcd import float_gcd
from .ket import Ket
from .np_extension import inverse_tensor, tensor_product

__all__ = ["find_nth_substring", "float_gcd", "Ket", "inverse_tensor", "tensor_product"]
