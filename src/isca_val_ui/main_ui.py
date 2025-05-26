#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTHOR

    Sebastien Le Maguer <lemaguer@surface.home>

DESCRIPTION

LICENSE
    This script is in the public domain, free from copyrights or restrictions.
    Created: 25 May 2025
"""

# Python

from typing import Any
import pathlib
import argparse
import sys
import importlib_resources

# Messaging/logging
import logging
from logging.config import dictConfig

# PyQt / Data
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

# IO
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

# Current
from .model.papers import PaperModel

###############################################################################
# global constants
###############################################################################
LEVEL = [logging.WARNING, logging.INFO, logging.DEBUG]


###############################################################################
# Functions
###############################################################################
def configure_logger(args) -> logging.Logger:
    """Setup the global logging configurations and instanciate a specific logger for the current script

    Parameters
    ----------
    args : dict
        The arguments given to the script

    Returns
    --------
    the logger: logger.Logger
    """
    # create logger and formatter
    logger = logging.getLogger()

    # Verbose level => logging level
    log_level = args.verbosity
    if args.verbosity >= len(LEVEL):
        log_level = len(LEVEL) - 1
        # logging.warning("verbosity level is too high, I'm gonna assume you're taking the highest (%d)" % log_level)

    # Define the default logger configuration
    logging_config = dict(
        version=1,
        disable_existing_logger=True,
        formatters={
            "f": {
                "format": "[%(asctime)s] [%(levelname)s] — [%(name)s — %(funcName)s:%(lineno)d] %(message)s",
                "datefmt": "%d/%b/%Y: %H:%M:%S ",
            }
        },
        handlers={
            "h": {
                "class": "logging.StreamHandler",
                "formatter": "f",
                "level": LEVEL[log_level],
            }
        },
        root={"handlers": ["h"], "level": LEVEL[log_level]},
    )

    # Add file handler if file logging required
    if args.log_file is not None:
        logging_config["handlers"]["f"] = {
            "class": "logging.FileHandler",
            "formatter": "f",
            "level": LEVEL[log_level],
            "filename": args.log_file,
        }
        logging_config["root"]["handlers"] = ["h", "f"]

    # Setup logging configuration
    dictConfig(logging_config)

    # Retrieve and return the logger dedicated to the script
    logger = logging.getLogger(__name__)
    return logger


def define_argument_parser() -> argparse.ArgumentParser:
    """Defines the argument parser

    Returns
    --------
    The argument parser: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description="")

    # Add logging options
    parser.add_argument("-l", "--log_file", default=None, help="Logger file")
    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=0,
        help="increase output verbosity",
    )

    # Add arguments
    parser.add_argument("-d", "--checker-description-file", default="./desc.yaml", type=str, help="The checker printer name")
    parser.add_argument("-r", "--report-file", default="./report.yaml", type=str, help="The ISCA checker report file")

    # Return parser
    return parser


###############################################################################
# I/O
###############################################################################
def commentedmap_to_dict(cm: CommentedMap | list | Any, config_dir: pathlib.Path) -> dict | list | Any:
    """Convert the ruamel.yaml format to python objects

    Parameters
    ----------
    cm : CommentedMap | list | Any
        The ruamel.yaml object
    config_dir: pathlib.Path
        The directory containing the configuration file and used a the origin of any relative path

    Returns
    -------
    dict | list | Any
        the python object
    """

    if isinstance(cm, CommentedMap):
        to_return = {}
        for k, v in cm.items():
            if k.endswith("_file"):
                to_return[k] = str((config_dir/v).resolve())
            else:
                to_return[k] = commentedmap_to_dict(v, config_dir)
        return to_return
    elif isinstance(cm, list):
        return [commentedmap_to_dict(i, config_dir) for i in cm]
    else:
        return cm


def load_report_yaml(yaml_input_file: pathlib.Path) -> dict:
    """Helper to load the yaml report into a dictionary of papers

    Parameters
    ----------
    yaml_input_file : pathlib.Path
        The path to the file to load

    Returns
    -------
    dict
        The dictionnary of papers (paper_id -> paper_info)
    """

    yaml_io = YAML(typ="rt", pure=True)
    yaml_io.preserve_quotes = True
    yaml_io.indent(mapping=2, sequence=4, offset=2)

    # Load file list from YAML
    with open(yaml_input_file, "r") as f:
        content_yaml = commentedmap_to_dict(yaml_io.load(f), yaml_input_file.resolve().parent)

    return content_yaml["papers"]


def load_desc_yaml(yaml_input_file: pathlib.Path) -> dict:
    """Helper to load the yaml report into a dictionary of papers

    Parameters
    ----------
    yaml_input_file : pathlib.Path
        The path to the file to load

    Returns
    -------
    dict
        The dictionnary of papers (paper_id -> paper_info)
    """

    yaml_io = YAML(typ="rt", pure=True)
    yaml_io.preserve_quotes = True
    yaml_io.indent(mapping=2, sequence=4, offset=2)

    # Load file list from YAML
    with open(yaml_input_file, "r") as f:
        content_yaml = commentedmap_to_dict(yaml_io.load(f), yaml_input_file.resolve().parent)

    return content_yaml



###############################################################################
# Entry point
###############################################################################
def main():
    # Initialization of the argument parser and the logger
    arg_parser = define_argument_parser()
    args = arg_parser.parse_args()
    logger = configure_logger(args)

    QQuickStyle.setStyle("Material")
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Load the data
    papers = load_report_yaml(pathlib.Path(args.report_file))
    description = None
    if pathlib.Path(args.checker_description_file).exists():
        description = load_desc_yaml(pathlib.Path(args.checker_description_file))

    # Register the data provider class with QML
    data_provider = PaperModel(papers, description)
    engine.rootContext().setContextProperty("paperModel", data_provider)

    # Ready, now go!
    qml_file = importlib_resources.files("isca_val_ui") / "resources/qml/main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())


###############################################################################
# Wrapping for directly calling the scripts
###############################################################################
if __name__ == "__main__":
    main()
