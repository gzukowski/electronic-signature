"""
common.utils

This module provides utility functions for the electronic signature project. It includes functions for loading stylesheets and other common utilities.

Modules:

- utils.py
    - load_stylesheet(widget, relative_path): Loads a stylesheet from a given relative path and applies it to the specified widget.
        - Args:
            - widget (QWidget): The widget to which the stylesheet will be applied.
            - relative_path (str): The relative path to the stylesheet file.
        - Raises:
            - FileNotFoundError: If the stylesheet file does not exist.
            - IOError: If there is an error reading the stylesheet file.
"""
