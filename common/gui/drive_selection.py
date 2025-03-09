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
    """
        DriveSelectionWidget is a QWidget that allows users to select a drive from a list of connected drives.

    Attributes:
        mode (DriveSelectorMode): Mode of the drive selector, either 'STANDARD' or 'WITH_KEYS'.
        drive_manager (DriveManager): Manages the drives.
        is_drive_selected (bool): Indicates if a drive has been selected.
        selected_drive_label (QLabel): Label displaying the selected drive.
        drive_list (QListWidget): List widget displaying the available drives.
        select_btn (QPushButton): Button to select a drive.
        timer (QTimer): Timer to refresh the list of drives.

    Methods:
        __init__(mode=DriveSelectorMode.STANDARD): Initializes the DriveSelectionWidget.
        init_ui(): Initializes the user interface.
        refresh_drives(): Refreshes the list of connected drives.
        get_connected_drives(): Retrieves the list of connected drives based on the mode.
        select_drive(): Selects the currently highlighted drive in the list.

    """

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
        """
        Initializes the user interface for drive selection.
        This method sets up the layout and widgets for the drive selection UI, including:
        - Loading the stylesheet for the UI.
        - Creating and configuring a vertical layout.
        - Adding a label to display the selected drive.
        - Adding a list widget to display available drives.
        - Adding a button to confirm drive selection.
        - Setting up a timer to periodically refresh the list of available drives.
        Widgets:
            selected_drive_label (QLabel): Displays the currently selected drive.
            drive_list (QListWidget): Lists available drives for selection.
            select_btn (QPushButton): Button to confirm the selected drive.
            timer (QTimer): Timer to refresh the list of available drives.
        Layouts:
            layout (QVBoxLayout): Main vertical layout for the UI.
            button_layout (QHBoxLayout): Horizontal layout for the select button.
        Connections:
            select_btn.clicked: Connects to the select_drive method.
            timer.timeout: Connects to the refresh_drives method.
        """
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
        """
        Refresh the list of connected drives in the GUI.
        This method updates the drive list by performing the following steps:
        1. Retrieves the currently connected drives.
        2. Adds any new drives to the drive list.
        3. Removes any drives from the drive list that are no longer connected.
        4. If there is only one drive in the list and no drive is currently selected,
           it selects the first drive and marks it as selected.
        5. Logs the refresh action.

        Returns:
            None

        """
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

    def get_connected_drives(self):
        """
        Retrieves a list of connected drives based on the current mode.
        If the mode is `DriveSelectorMode.WITH_KEYS`, it lists drives that have keys.
        Otherwise, it refreshes the drive manager and retrieves the full list of drives.

        Returns:
            list: A list of connected drives.

        """
        drives = []

        if self.mode == DriveSelectorMode.WITH_KEYS:
            drives = self.drive_manager.list_drives_with_keys()
        else:
            self.drive_manager.refresh()
            drives = self.drive_manager.drive_list

        return drives

    def select_drive(self):
        """
        Handles the selection of a drive from the drive list.

        This method retrieves the selected item from the drive list. If an item is selected,
        it updates the `selected_drive` attribute of the `drive_manager` with the text of the selected item,
        logs the selected drive, and updates the `selected_drive_label` to display the selected drive.
        If no item is selected, it logs that no drive was selected and updates the `selected_drive_label`
        to indicate that no drive was selected.
        """
        selected_item = self.drive_list.selectedItems()
        if selected_item:
            self.drive_manager.selected_drive = selected_item[0].text()
            logger.info("Selected drive: %s", self.drive_manager.selected_drive)
            self.selected_drive_label.setText(f"Selected drive: {self.drive_manager.selected_drive}")
        else:
            logger.info("No drive selected")
            self.selected_drive_label.setText("No drive selected.")
