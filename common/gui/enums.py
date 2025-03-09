import enum


class DriveSelectorMode(enum.IntEnum):
    """
    Enumeration for drive selector modes.

    Attributes:
        STANDARD (int): Standard drive selection mode.
        WITH_KEYS (int): Drive selection mode with keys.

    """

    STANDARD = 0
    WITH_KEYS = 1
