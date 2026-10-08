"""Project exception hierarchy."""


class ArgparslibError(Exception):
    """Base class for all argparslib errors."""


class UnknownFlagError(ArgparslibError, ValueError):
    """Raised when an argument does not match any registered flag."""
