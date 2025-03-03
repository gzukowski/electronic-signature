import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget

from common.drive_manager.drive_manager import DriveManager
from common.gui.enums import DriveSelectorMode
from common.utils.utils import load_stylesheet

logger = logging.getLogger("global_logger")

DRIVES_REFRESH = 300

class DriveSelectionWidget(QWidget):
    def __init__(self, mode=DriveSelectorMode.STANDARD):
        """
        DriveSelectionWidget constructor.

        Args:
            mode (str): 'STANDARD' - lists all drives, 'WITH_KEYS' - only drives with keys.

        """
        super().__init__()
        logger.info("Drive Selection Widget created")
        self.mode = mode
        self.drive_manager = DriveManager()
        self.is_drive_selected = False
        self.init_ui()

    def init_ui(self):
        load_stylesheet(self, "common/gui/css/driver_selection.css")
        layout = QVBoxLayout()

        self.selected_drive_label = QLabel("No drive selected.")

        self.drive_list = QListWidget()
        self.drive_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        button_layout = QHBoxLayout()
        self.select_btn = QPushButton("Select Drive")
        self.select_btn.clicked.connect(self.select_drive)
        button_layout.addWidget(self.select_btn)

        layout.addWidget(self.drive_list)
        layout.addWidget(self.selected_drive_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_drives)
        self.timer.start(DRIVES_REFRESH)

        self.refresh_drives()

    def refresh_drives(self):
        connected_drives = self.get_connected_drives()

        current_items = {item.text() for item in self.drive_list.findItems("*", Qt.MatchFlag.MatchWildcard)}

        for drive in connected_drives:
            if drive not in current_items:
                self.drive_list.addItem(drive)

        for item in self.drive_list.findItems("*", Qt.MatchFlag.MatchWildcard):
            if item.text() not in connected_drives:
                self.drive_list.takeItem(self.drive_list.row(item))

        if self.drive_list.count() == 1 and not self.is_drive_selected:
            self.drive_list.setCurrentRow(0)
            self.select_drive()
            self.is_drive_selected = True

        logger.info("Drive list refreshed")

    def get_connected_drives(self):
        drives = []

        if self.mode == DriveSelectorMode.WITH_KEYS:
            drives = self.drive_manager.list_drives_with_keys()
        else:
            self.drive_manager.refresh()
            drives = self.drive_manager.drive_list

        return drives

    def select_drive(self):
        selected_item = self.drive_list.selectedItems()
        if selected_item:
            self.drive_manager.selected_drive = selected_item[0].text()
            logger.info("Selected drive: %s", self.drive_manager.selected_drive)
            self.selected_drive_label.setText(f"Selected drive: {self.drive_manager.selected_drive}")
        else:
            logger.info("No drive selected")
            self.selected_drive_label.setText("No drive selected.")
