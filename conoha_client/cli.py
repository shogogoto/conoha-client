"""CLI definition."""

import click
from click_shell import shell

from conoha_client._shared.renforced_vm import (
    list_vm_cli,
    reinforced_vm_cli,
    shortcut_vm_cli,
)
from conoha_client.features import (
    sshkey_cli,
    vm_actions_cli,
    vm_image_cli,
    vm_plan_cli,
)
from conoha_client.features.billing.cli import invoice_cli, order_cli, paid_cli
from conoha_client.graceful_remove import graceful_rm_cli
from conoha_client.vm import vm_add_cli, vm_resize_cli
from conoha_client.vm.rebuild import vm_rebuild_cli

from .snapshot import snapshot_cli

__version__ = "0.0.0"


# @click.group()
@shell(prompt="(conoha-client) ")
def cli() -> None:
    """root."""


@cli.command()
def version() -> None:
    """Show self version."""
    click.echo(f"conoha-client {__version__}")


@click.group()
def vm_cli() -> None:
    """VM関連."""


def main() -> None:
    """CLI設定用."""
    vm_cli.add_command(list_vm_cli)
    vm_cli.add_command(vm_add_cli)
    vm_cli.add_command(graceful_rm_cli)
    vm_cli.add_command(vm_rebuild_cli)
    vm_merged = click.CommandCollection(
        name="vm",
        sources=[
            vm_cli,
            vm_actions_cli,
            vm_resize_cli,
        ],
        help="VM操作関連",
    )
    cli.add_command(vm_merged)
    cli.add_command(vm_plan_cli)
    cli.add_command(vm_image_cli)
    cli.add_command(sshkey_cli)

    cli.add_command(order_cli)
    cli.add_command(paid_cli)
    cli.add_command(invoice_cli)

    cli.add_command(snapshot_cli)
    cli.add_command(reinforced_vm_cli)
    cli.add_command(shortcut_vm_cli)
    cli()
