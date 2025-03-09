import enum


class SignState(enum.IntEnum):
    FINISHED = 0
    ERRORED = -1

class VerifyState(enum.IntEnum):
    FINISHED = 0
    ERRORED = -1

