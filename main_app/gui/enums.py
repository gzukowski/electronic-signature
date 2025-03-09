import enum


class SignState(enum.IntEnum):
    """
    SignState is an enumeration representing the state of a signing process.

    Attributes:
        FINISHED (int): Indicates that the signing process has completed successfully.
        ERRORED (int): Indicates that an error occurred during the signing process.

    """

    FINISHED = 0
    ERRORED = -1

class VerifyState(enum.IntEnum):
    """
    Enum class representing the state of a verification process.

    Attributes:
        FINISHED (int): Indicates that the verification process has finished successfully.
        ERRORED (int): Indicates that an error occurred during the verification process.

    """

    FINISHED = 0
    ERRORED = -1

