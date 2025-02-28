from PyQt6.QtCore import QFile, QTextStream


def load_stylesheet(widget, filename):
    file = QFile(filename)
    if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(file)
        stylesheet = stream.readAll()
        widget.setStyleSheet(stylesheet)
        file.close()
