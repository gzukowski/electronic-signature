import enum


class RsaGenState(enum.IntEnum):
    """
    Enum representing the state of RSA key generation.

    Attributes:
        FINISHED (int): Indicates that the RSA key generation has finished successfully.
        ERRORED (int): Indicates that an error occurred during RSA key generation.

    """

    FINISHED = 0
    ERRORED = -1
