"""
common.logger

This module provides logging functionality for the electronic signature project. It includes functions for initializing the logger and compressing old log files into a ZIP archive.

Modules:

- logger.py
    - compress_old_log(log_file): Compresses the existing log file into a single ZIP archive before starting a new session.
        - Args:
            - log_file (Path): The path to the log file to be compressed.
    - initialize(log_file): Initializes the new global logger instance.
        - Args:
            - log_file (Path): The path to the log file to be initialized.
"""
