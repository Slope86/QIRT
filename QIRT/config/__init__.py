"""Configuration for QIRT package.

This module provides the configuration settings for the Quantum Information Research Toolkit (QIRT).
It includes functionalities to read and parse configuration settings from the `config.ini` file located
in the `QIRT/config` directory. The configuration settings include custom notations for quantum state
vectors and visualization parameters for LaTeX outputs.

Modules:
    config: Contains the `get_config_parser` function to read and parse the configuration settings.
"""

from .config import CONFIG_PARSER

__all__ = ["CONFIG_PARSER"]
