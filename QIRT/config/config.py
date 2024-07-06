import configparser
import importlib.resources as pkg_resources


def get_config_parser() -> configparser.ConfigParser:
    """Get the configuration parser for the QIRT project.

    This function reads the configuration from the config.ini file located
    in the QIRT/config directory and returns a ConfigParser object.

    Returns:
        configparser.ConfigParser: The configuration parser with the settings read from config.ini.
    """
    config_parser = configparser.ConfigParser()
    config_path = pkg_resources.files("QIRT.config").joinpath("config.ini")
    with config_path.open("r") as file:
        config_parser.read_file(file)
    return config_parser
