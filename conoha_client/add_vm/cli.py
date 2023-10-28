"""add VM CLI."""
from __future__ import annotations

import os
from operator import attrgetter
from typing import TYPE_CHECKING

import click

from conoha_client.add_vm.repo import DistQuery
from conoha_client.features._shared.view.domain import view_options
from conoha_client.features.image.domain import (
    Application,
    Distribution,
    DistVersion,
)
from conoha_client.features.plan.domain import Memory

if TYPE_CHECKING:
    from conoha_client.features.vm.domain import VM

    pass


@click.group("add", invoke_without_command=True)
@click.option(
    "--memory",
    "-m",
    type=click.Choice(Memory),
    required=True,
)
@click.option(
    "--dist",
    "-d",
    type=click.Choice(Distribution),
    default=Distribution.UBUNTU,
    show_default=True,
)
@click.option(
    "--version",
    "-v",
    default="latest",
    help="latestの場合最新バージョンが指定される",
    show_default=True,
    type=DistVersion.parse,
)
@click.option(
    "--app",
    "-a",
    default="null",
    help="アプリ名.NONEは指定なし",
    show_default=True,
    type=Application.parse,
)
@click.option(
    "--admin-password",
    "-pw",
    default=lambda: os.getenv("OS_ADMIN_PASSWORD", None),
    help="VMのrootユーザーのパスワード:OS_ADMIN_PASSWORD環境変数の値が設定される",
    show_default=True,
)
@click.option(
    "--keypair-name",
    "-k",
    default=lambda: os.getenv("OS_SSHKEY_NAME", None),
    help="sshkeyのペア名:OS_SSHKEY_NAME環境変数の値が設定される",
    show_default=True,
)
@view_options
@click.pass_context
def add_vm_cli(  # noqa: PLR0913
    ctx: click.Context,
    memory: Memory,
    dist: Distribution,
    version: str,
    app: str,
    admin_password: str | None,
    keypair_name: str | None,
) -> list[VM]:
    """Add VM CLI."""
    ctx.ensure_object(dict)
    query = DistQuery(memory=memory, dist=dist)
    # a = Application.parse(app)
    ctx.obj["q"] = query
    ctx.obj["version"] = version
    ctx.obj["app"] = app
    if ctx.invoked_subcommand is None:
        click.echo(admin_password)
        click.echo(keypair_name)
        # cmd = add_vm_command(
        #     memory=memory,
        #     dist=dist,
        #     ver=version,
        #     app=app,
        #     admin_pass=admin_password,
        # )
        # click.echo(cmd)
    #     click.echo(":以下のVMが新規追加されました")
    #     return [added]
    return []


@add_vm_cli.command(name="dist-vers")
@view_options
@click.pass_obj
def list_os_versions(obj: object) -> list[DistVersion]:
    """利用可能なOSバージョンを検索する."""
    vers = obj["q"].available_vers()
    return sorted(vers, key=attrgetter("value"))


@add_vm_cli.command(name="apps")
@view_options
@click.pass_obj
def find_apps(obj: object) -> list[Application]:
    """利用可能なアプリケーションを検索する."""
    v = obj["version"]
    apps = obj["q"].apps(v)
    return sorted(apps, key=attrgetter("value"))
