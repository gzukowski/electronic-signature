import logging
from pathlib import Path

from PyQt6.QtCore import QFile, QTextStream

logger = logging.getLogger("global_logger")

def load_stylesheet(widget, relative_path):
    css_path = Path(__file__).resolve().parents[2] / relative_path

    file = QFile(str(css_path))
    if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(file)
        widget.setStyleSheet(stream.readAll())
        file.close()
