import pytest

from argparslib.errors import ArgparslibError, UnknownFlagError
from argparslib.parser import Parser


@pytest.fixture
def parser() -> Parser:
    flag_parser = Parser()
    flag_parser.register_flag("verbose", short="v")
    flag_parser.register_flag("debug", short="d")
    return flag_parser


@pytest.mark.unit
def test_parse_single_long_flag(parser: Parser) -> None:
    assert parser.parse(["--verbose"])["verbose"] is True


@pytest.mark.unit
def test_parse_multiple_long_flags(parser: Parser) -> None:
    result = parser.parse(["--verbose", "--debug"])

    assert result["verbose"] is True
    assert result["debug"] is True


@pytest.mark.unit
def test_parse_multiple_short_flags(parser: Parser) -> None:
    result = parser.parse(["-v", "-d"])

    assert result["verbose"] is True
    assert result["debug"] is True


@pytest.mark.unit
@pytest.mark.parametrize(
    "token",
    [
        pytest.param("--verbose", id="long"),
        pytest.param("-v", id="short"),
    ],
)
def test_short_alias_sets_long_name(parser: Parser, token: str) -> None:
    assert parser.parse([token]) == {"verbose": True, "debug": False}


@pytest.mark.unit
@pytest.mark.parametrize(
    ("token", "message"),
    [
        pytest.param("--unknown", "unknown flag '--unknown'", id="long"),
        pytest.param("-x", "unknown flag '-x'", id="short"),
        pytest.param("positional", "unknown flag 'positional'", id="non_flag_token"),
    ],
)
def test_unknown_flag_raises(parser: Parser, token: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        parser.parse([token])


@pytest.mark.unit
def test_unknown_flag_error_belongs_to_project_hierarchy(parser: Parser) -> None:
    with pytest.raises(ArgparslibError):
        parser.parse(["--unknown"])
    assert issubclass(UnknownFlagError, ValueError)


@pytest.mark.unit
def test_absent_flags_are_false(parser: Parser) -> None:
    assert parser.parse([]) == {"verbose": False, "debug": False}


@pytest.mark.unit
def test_default_value_used_when_absent() -> None:
    flag_parser = Parser()
    flag_parser.register_flag("color", default=True)
    flag_parser.register_flag("quiet")

    assert flag_parser.parse([]) == {"color": True, "quiet": False}


@pytest.mark.unit
def test_flag_without_short_form_rejects_short_token() -> None:
    flag_parser = Parser()
    flag_parser.register_flag("verbose")

    with pytest.raises(UnknownFlagError, match="unknown flag '-v'"):
        flag_parser.parse(["-v"])
