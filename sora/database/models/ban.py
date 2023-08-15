import time
from tortoise import fields
from tortoise.models import Model

from sora.log import logger


class BanUser(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    user_id = fields.CharField(max_length=10, unique=True)
    """用户ID"""
    ban_time = fields.BigIntField()
    """ban开始的时间"""
    duration = fields.BigIntField()
    """ban时长"""

    class Meta:
        table = "banUser"
        table_description = "封禁人员数据表"

    @classmethod
    async def check_ban_time(cls, user_id: int | str) -> int | str:
        """
        说明:
            检测用户被ban时长
        参数:
            * user_id: 用户id
        """
        if user := await cls.filter(user_id=str(user_id)).first():
            if (
                time.time() - (user.ban_time + user.duration) > 0
                and user.duration != -1
            ):
                return ""
            if user.duration == -1:
                return "∞"
            return int(time.time() - user.ban_time - user.duration)
        return ""

    @classmethod
    async def is_ban(cls, user_id: int | str) -> bool:
        """
        说明:
            判断用户是否被ban
        参数:
            * user_id: 用户id
        """
        if await cls.check_ban_time(str(user_id)):
            return True
        else:
            await cls.unban(user_id)
        return False

    @classmethod
    async def ban(cls, user_id: int | str, duration: int):
        """
        说明:
            ban掉目标用户
        参数:
            * user_id: 目标用户id
            * duration:  ban时长（秒），-1 表示永久封禁
        """
        logger.debug("封禁", f"封禁用户，ID: {str(user_id)}，时长: {duration}")
        if await cls.filter(user_id=str(user_id)).first():
            await cls.unban(user_id)
        await cls.create(
            user_id=str(user_id),
            ban_time=time.time(),
            duration=duration,
        )

    @classmethod
    async def unban(cls, user_id: int | str) -> bool:
        """
        说明:
            unban用户
        参数:
            * user_id: 用户id
        """
        if user := await cls.filter(user_id=user_id).first():
            logger.debug("封禁", f"解除封禁：{str(user_id)}")
            await user.delete()
            return True
        return False
