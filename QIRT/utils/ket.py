r"""Module to store and check the ket notation for the state vector.

This module provides functionality to store and validate ket notations used for
representing quantum state vectors. The ket notations can be customized through a
configuration file (config.ini). The module ensures that the notations conform to
expected single-character representations and provides methods to validate and convert
ket notations to the standard Qiskit format.

The functionalities added in this module are:
- Storage of custom ket notations.
- Validation of ket notation strings.
- Conversion of custom ket notations to Qiskit-compatible notations.

Configurable Ket Notations:
- z0: Default is "0"
- z1: Default is "1"
- x0: Default is "+"
- x1: Default is "-"
- y0: Default is "i"
- y1: Default is "j"

The configurable notations are read from the `config.ini` file located in the project's `QIRT/config` directory.
"""

import re

from QIRT.config import CONFIG_PARSER


class _ConfigMeta(type):
    """Metaclass to load and store ket notations from the config file."""

    __z0: str = "0"
    __z1: str = "1"
    __x0: str = "+"
    __x1: str = "-"
    __y0: str = "i"
    __y1: str = "j"

    def __new__(cls, name, bases, namespace):
        """Create a new instance of the metaclass and load the config settings."""
        for ket in CONFIG_PARSER["ket"]:
            if ket not in ["z0", "z1", "x0", "x1", "y0", "y1"]:
                print(f"Unknown basis [{ket}]. Basis should be z0, z1, x0, x1, y0, y1.")
                print("Please check the config.ini file, invalid user setting will be ignored and use default setting.")
                continue
            if len(CONFIG_PARSER["ket"][ket]) != 1:
                print(f"The ket notation should be a single character but [{CONFIG_PARSER['ket'][ket]}] is given.")
                print("Please check the config.ini file, invalid user setting will be ignored and use default setting.")
                continue
            match ket:
                case "z0":
                    cls.__z0 = CONFIG_PARSER["ket"][ket]
                case "z1":
                    cls.__z1 = CONFIG_PARSER["ket"][ket]
                case "x0":
                    cls.__x0 = CONFIG_PARSER["ket"][ket]
                case "x1":
                    cls.__x1 = CONFIG_PARSER["ket"][ket]
                case "y0":
                    cls.__y0 = CONFIG_PARSER["ket"][ket]
                case "y1":
                    cls.__y1 = CONFIG_PARSER["ket"][ket]

        return super().__new__(cls, name, bases, namespace)

    @property
    def z0(cls) -> str:
        return cls.__z0

    @property
    def z1(cls) -> str:
        return cls.__z1

    @property
    def x0(cls) -> str:
        return cls.__x0

    @property
    def x1(cls) -> str:
        return cls.__x1

    @property
    def y0(cls) -> str:
        return cls.__y0

    @property
    def y1(cls) -> str:
        return cls.__y1


class Ket(metaclass=_ConfigMeta):
    """Class to store and check the ket notation for the state vector."""

    @classmethod
    def check_valid(cls, label: str) -> bool:
        """Check if the input label is valid.

        Args:
            label (str): The ket notation label to validate.

        Returns:
            bool: True if the label is valid, False otherwise.

        """
        # Create a regex pattern based on the configured ket notations
        ket_regex = "^[" + cls.z0 + cls.z1 + cls.x0 + cls.x1 + cls.y0 + cls.y1 + "]+$"
        # Escape the minus sign in the regex
        ket_regex = ket_regex.replace("-", R"\-")

        # Validate the label against the regex pattern
        if re.match(ket_regex, label) is None:
            return False
        return True

    @classmethod
    def to_qiskit_notation(cls, label: str) -> str:
        """Convert the custom ket notation to Qiskit-compatible notation.

        Args:
            label (str): The ket notation label to convert.

        Returns:
            str: The converted Qiskit-compatible notation.

        """
        # Replace custom ket notations with Qiskit standard notations
        label = label.replace(Ket.z0, "0")
        label = label.replace(Ket.z1, "1")
        label = label.replace(Ket.x0, "+")
        label = label.replace(Ket.x1, "-")
        label = label.replace(Ket.y0, "r")
        label = label.replace(Ket.y1, "l")
        return label
