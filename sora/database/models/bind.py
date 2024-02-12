from typing import Any

from tortoise import fields
from tortoise.models import Model

from .user import User


class Bind(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    uid = fields.CharField(max_length=10)
    """用户ID"""
    origin_uid = fields.CharField(max_length=10, null=True)
    """用户原始ID"""
    platform = fields.CharField(max_length=50)
    """绑定平台"""
    pid = fields.CharField(max_length=50)
    """平台ID"""

    info: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="bind", to_field="uid"
    )

    class Meta:
        table = "Bind"

    @classmethod
    async def check_pid_exists(cls, platform: str, pid: str) -> bool:
        """
        说明：
            判断 platform 账号 是否存在于 Bind 表中

        参数：
            * platform: 平台
            * pid: 平台ID

        返回：
            如果存在则返回 `true`,
            反之则返回 `false`
        """
        exists = await cls.filter(platform=platform, pid=pid).exists()
        return exists

    @classmethod
    async def bind(cls, origin_uid: str, bind_uid: str) -> None:
        """
        说明：
            绑定账号
        参数：
            * origin_uid: 原 uid
            * bind_uid: 预绑定后的 uid
        """
        bind = await Bind.get(uid=origin_uid)
        user = await User.get(uid=bind_uid)
        bind.origin_uid = origin_uid
        bind.uid = bind_uid
        bind.info = user
        await bind.save()

    @classmethod
    async def cancel(cls, origin_uid: str, rebind_uid: str, platform: str) -> None:
        """
        说明：
            取消绑定
        参数：
            * origin_uid: 原uid
            * rebind_uid: 预取消绑定的 uid
        """
        bind = await Bind.get(uid=rebind_uid, platform=platform)
        user = await User.get(uid=origin_uid)
        bind.origin_uid = None
        bind.uid = origin_uid
        bind.info = user
        await bind.save()

    @classmethod
    async def get_user_bind(cls, pid: str) -> list[dict[str, Any]]:
        """
        说明：
            获取用户绑定信息
        参数：
            * pid: 平台ID
        """
        user_data = await cls.filter(pid=pid).values("uid", "platform", "pid")
        uid = user_data[0]["uid"]
        data = await cls.filter(uid=uid).values("uid", "platform", "pid")
        return data
