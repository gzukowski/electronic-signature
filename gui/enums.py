import enum


class RsaGenState(enum.IntEnum):
    FINISHED = 0
    ERRORED = -1

class SignState(enum.IntEnum):
    FINISHED = 0
    ERRORED = -1

class DriveSelectorMode(enum.IntEnum):
    STANDARD = 0
    WITH_KEYS = 1
