"""VM Domain."""

from datetime import datetime
from enum import Enum
from ipaddress import IPv4Address
from uuid import UUID

from pydantic import AliasPath, BaseModel, Field, field_validator

from conoha_client.features._shared.util import TOKYO_TZ


class VMStatus(Enum):
    """契約中Serverの状態."""

    ACTIVE = "ACTIVE"
    SHUTOFF = "SHUTOFF"
    REBOOT = "REBOOT"
    BUILD = "BUILD"

    def is_shutoff(self) -> bool:
        """シャットダウン済みか否か."""
        return self == VMStatus.SHUTOFF


class VM(BaseModel, frozen=True):
    """契約中のサーバー."""

    name: str = Field(alias="name")
    vm_id: UUID = Field(alias="id", description="このIDに請求が紐づいている")
    status: VMStatus = Field(alias="status")
    created: datetime = Field(alias="created")
    updated: datetime = Field(alias="updated")
    image_id: UUID = Field(alias=AliasPath("image", "id"))
    flavor_id: UUID = Field(alias=AliasPath("flavor", "id"))

    # def elapsed_from_created(self) -> timedelta:
    #     """作成時からの経過時間を秒以下を省いて計算する."""
    #     return now_jst() - self.created_at
    @property
    def ipv4(self) -> IPv4Address:
        """ipv4 from name."""
        return IPv4Address(self.name.replace("-", "."))

    @field_validator("created")
    def validate_created(cls, v: datetime) -> datetime:  # noqa: N805
        """Validate created datetime."""
        return v.astimezone(TOKYO_TZ)

    @field_validator("updated")
    def validate_updated(cls, v: datetime) -> datetime:  # noqa: N805
        """Validate created datetime."""
        return v.astimezone(TOKYO_TZ)


class AddedVM(BaseModel, frozen=True):
    """新規追加されたVM."""

    vm_id: UUID = Field(alias="id")
