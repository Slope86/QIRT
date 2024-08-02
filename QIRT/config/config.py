"""The configuration parser for the QIRT project."""

import configparser
import importlib.resources as pkg_resources
import os
import shutil


def _ensure_user_config():
    """Ensure the user configuration file exists."""
    user_config_path = os.path.expanduser("~/.QIRT/config.ini")
    if not os.path.exists(user_config_path):
        os.makedirs(os.path.dirname(user_config_path), exist_ok=True)
        default_config_path = pkg_resources.files("QIRT.config").joinpath("default_config.ini")
        shutil.copy(str(default_config_path), user_config_path)
    return user_config_path


def _get_config_parser() -> configparser.ConfigParser:
    """Get the configuration parser for the QIRT project.

    This function reads the configuration from the user's config.ini file
    located in the user's home directory and returns a ConfigParser object.

    Returns
    -------
        configparser.ConfigParser: The configuration parser with the settings read from config.ini.

    """
    config_parser = configparser.ConfigParser()
    user_config_path = _ensure_user_config()
    with open(user_config_path) as file:
        config_parser.read_file(file)
    return config_parser


CONFIG_PARSER = _get_config_parser()
