"""add VM domain test."""
from __future__ import annotations

import pytest

from conoha_client.add_vm.domain.errors import (
    ApplicationWithoutVersionError,
    OSVersionExtractError,
)

from .domain import OS, Application, Version


def test_os_is_match() -> None:
    """OS名がむくまれているか."""
    assert OS.UBUNTU.is_match("xxx-ubuntu-yyy")
    assert not OS.UBUNTU.is_match("xxx-not_ubuntu-yyy")


def test_get_os_version() -> None:
    """OS Versionを取得できるか."""
    assert OS.UBUNTU.version("xxx-ubuntu-vvv-zzzz") == Version(value="vvv")


def test_get_win_version() -> None:
    """Windowsの場合は後ろ2要素を結合したものがバージョンとなる."""
    assert OS.WINDOWS.version("vmi-win2019dce-rds") == Version(value="win2019dce-rds")
    assert OS.WINDOWS.version("vmi-win-2019dce-amd64") == Version(value="win-2019dce")


def test_invalid_get_os_version() -> None:
    """OS Versionが取得できないときに適切なエラーが出るか."""
    with pytest.raises(OSVersionExtractError):
        OS.UBUNTU.version("xxx-ubun-22.0")
    with pytest.raises(OSVersionExtractError):
        OS.UBUNTU.version("xxx-ubuntu")


def test_get_app_with_version() -> None:
    """OSに紐づいたアプリ名とバージョンを取得する."""
    av1 = OS.UBUNTU.app_with_version("vmi-rust-latest-ubuntu-20.04-amd64-100gb")
    assert av1 == Application(name="rust", version=Version(value="latest"))
    av3 = OS.DEBIAN.app_with_version("vmi-debian-12.0-amd64-100gb")
    assert av3 == Application.none()
    av4 = OS.CENTOS.app_with_version(
        "vmi-cacti-nagios-1.2.17.4.4.6-centos-7.9-amd64-30gb",
    )

    assert av4 == Application(
        name="cacti-nagios",
        version=Version(value="1.2.17.4.4.6"),
    )


def test_invalid_get_app_with_version() -> None:
    """OSに紐づいたアプリ名とバージョンを取得に失敗する."""
    with pytest.raises(OSVersionExtractError):
        OS.UBUNTU.app_with_version("dev")

    with pytest.raises(ApplicationWithoutVersionError):
        OS.UBUNTU.app_with_version(
            "vmi-appname_without_version-ubuntu-20.02-amd64-100gb",
        )