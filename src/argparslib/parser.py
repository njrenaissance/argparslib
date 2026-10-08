"""Boolean flag parser."""

from dataclasses import dataclass

from argparslib.errors import UnknownFlagError

LONG_PREFIX = "--"
SHORT_PREFIX = "-"


@dataclass(frozen=True)
class Flag:
    """A registered boolean flag."""

    name: str
    short: str | None
    default: bool


class Parser:
    """Parses boolean flags of the form ``--name``, ``-n`` or combined ``-nm``."""

    def __init__(self) -> None:
        self._flags: list[Flag] = []
        self._flags_by_token: dict[str, Flag] = {}

    def register_flag(self, name: str, short: str | None = None, default: bool = False) -> None:
        """Register a flag by long name, with an optional single-letter alias."""
        flag = Flag(name=name, short=short, default=default)
        self._flags.append(flag)
        self._flags_by_token[LONG_PREFIX + name] = flag
        if short is not None:
            self._flags_by_token[SHORT_PREFIX + short] = flag

    def parse(self, args: list[str]) -> dict[str, bool]:
        """Return every registered flag's value: ``True`` if present in ``args``, else its default.

        Raises:
            UnknownFlagError: if an argument matches no registered flag.
        """
        result = {flag.name: flag.default for flag in self._flags}
        for token in args:
            for flag_token in self._split_combined_short_flags(token):
                flag = self._flags_by_token.get(flag_token)
                if flag is None:
                    raise UnknownFlagError(f"unknown flag '{flag_token}'")
                result[flag.name] = True
        return result

    def _split_combined_short_flags(self, token: str) -> list[str]:
        """Expand a group such as ``-vd`` into ``["-v", "-d"]``; any other token is returned unchanged."""
        is_short_group = token.startswith(SHORT_PREFIX) and not token.startswith(LONG_PREFIX) and len(token) > 1
        if token in self._flags_by_token or not is_short_group:
            return [token]
        return [SHORT_PREFIX + letter for letter in token[len(SHORT_PREFIX) :]]
