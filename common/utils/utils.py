import logging
from pathlib import Path

from PyQt6.QtCore import QFile, QTextStream

logger = logging.getLogger("global_logger")

def load_stylesheet(widget, relative_path):
    """
    Loads a stylesheet from a given relative path and applies it to the specified widget.

    Args:
        widget (QWidget): The widget to which the stylesheet will be applied.
        relative_path (str): The relative path to the stylesheet file.

    Raises:
        FileNotFoundError: If the stylesheet file does not exist.
        IOError: If there is an error reading the stylesheet file.

    """
    css_path = Path(__file__).resolve().parents[2] / relative_path

    file = QFile(str(css_path))
    if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(file)
        widget.setStyleSheet(stream.readAll())
        file.close()
