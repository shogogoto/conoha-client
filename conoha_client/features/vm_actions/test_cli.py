"""VM Actions CLI test."""

from uuid import UUID, uuid4

import click
from click.testing import CliRunner

from conoha_client.features.vm_actions.command_option import (
    uuid_complete_options,
)

ONE = uuid4()


def complete(_: str) -> UUID:
    """Mock."""
    return ONE


@click.command()
@uuid_complete_options(complete)
def cli(uid: UUID) -> None:
    """Testee cli."""
    click.echo(f"{uid} was input")


@click.command()
@click.option("--option", "-o")
@uuid_complete_options(complete)
def cli_with_other_options(uid: UUID, option: str) -> None:
    """Testee cli2."""
    click.echo(f"{uid} and {option}")


def test_uuid_target_option() -> None:
    """uuid_target_optionsデコレータのテスト."""
    runner = CliRunner()
    uid = str(ONE)
    result = runner.invoke(cli, [str(uid)])
    assert uid in result.stdout


def test_with_other_option() -> None:
    """Another case."""
    runner = CliRunner()
    uid = str(ONE)
    result = runner.invoke(
        cli_with_other_options,
        [uid, "-o", "opt"],
    )
    assert uid in result.stdout
    assert "opt" in result.stdout


if __name__ == "__main__":
    cli()
