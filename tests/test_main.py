import pytest

from main import build_parser, greet, main


def test_greet():
    assert greet("world") == "Hello, world!"


@pytest.mark.unit
def test_build_parser_parses_name() -> None:
    args = build_parser().parse_args(["--name", "Alice"])

    assert args.name == "Alice"


@pytest.mark.unit
def test_build_parser_name_defaults_to_world() -> None:
    args = build_parser().parse_args([])

    assert args.name == "world"


@pytest.mark.unit
def test_build_parser_rejects_unknown_flag() -> None:
    with pytest.raises(SystemExit) as exit_info:
        build_parser().parse_args(["--bogus"])

    assert exit_info.value.code != 0


@pytest.mark.unit
@pytest.mark.parametrize(
    ("argv", "expected_output"),
    [
        pytest.param(["--name", "Alice"], "Hello, Alice!\n", id="name_passed"),
        pytest.param([], "Hello, world!\n", id="no_arguments"),
    ],
)
def test_main_prints_greeting(argv: list[str], expected_output: str, capsys: pytest.CaptureFixture[str]) -> None:
    main(argv)

    assert capsys.readouterr().out == expected_output


@pytest.mark.unit
def test_main_exits_nonzero_on_unknown_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--bogus"])

    assert exit_info.value.code != 0
    assert "unrecognized arguments" in capsys.readouterr().err


@pytest.mark.unit
def test_main_help_shows_name_option(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--help"])

    assert exit_info.value.code == 0
    assert "--name" in capsys.readouterr().out
