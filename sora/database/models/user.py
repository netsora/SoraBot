import random
from datetime import date
from typing import TYPE_CHECKING, Any

from tortoise import fields
from tortoise.models import Model
from nonebot.internal.adapter import Event
from nonebot.internal.permission import Permission as Permission

if TYPE_CHECKING:
    from .bind import Bind


class User(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    uid = fields.CharField(max_length=10, unique=True)
    """指用户注册后 Sora 为其分配的ID"""
    user_name = fields.CharField(max_length=15, unique=True)
    """用户昵称"""
    level = fields.IntField(default=0)
    """等级"""
    exp = fields.IntField(default=0)
    """经验值"""
    coin = fields.IntField(default=0)
    """硬币数"""
    favor = fields.IntField(default=0)
    """好感度"""
    birthday = fields.DateField(null=True)
    """生日"""
    register_time = fields.DatetimeField(auto_now_add=True)
    """注册日期"""
    permission = fields.CharField(max_length=10)

    bind: fields.ReverseRelation["Bind"]

    class Meta:
        table = "User"

    @classmethod
    async def create_user(
        cls,
        uid: str,
        user_name: str,
        level: int = 1,
        exp: int = 0,
        coin: int = 50,
        favor: int = 0,
        birthday: date | None = None,
        permission: str = "NORMAL",
    ):
        """
        说明：
            创建用户账号
        参数：
            * uid: 用户ID
            * user_name: 用户名
            * level: 等级
            * exp: 经验值
            * coin: 硬币
            * favor: 好感度
            * birthday: 出生日期，默认为 None
            * permission: 权限
        """
        return await cls.create(
            uid=uid,
            user_name=user_name,
            level=level,
            exp=exp,
            coin=coin,
            favor=favor,
            birthday=birthday,
            permission=permission,
        )

    @classmethod
    async def delete_user(cls, uid: str) -> None:
        """
        说明：
            删除用户账号及数据
        参数：
            * uid: 用户ID
        """
        user = await cls.get(uid=uid)
        await user.delete()

    @classmethod
    async def reward(
        cls, uid: str, *, reward: dict[str, Any]
    ) -> dict[str, int | float]:
        """
        说明：
            奖励用户
        参数：
            * reward: 奖励
        返回：
            奖励的数量
        """
        user = await cls.get(uid=uid)
        reward_amount = {}
        for key, value in reward.items():
            match key:
                case "coin":
                    if isinstance(value, list):
                        amount = random.randint(value[0], value[1])
                    elif isinstance(value, int):
                        amount = value
                    else:
                        raise TypeError(f"Invalid reward type: {type(value)}")
                    user.coin += amount
                    reward_amount[key] = amount
                case "exp":
                    if isinstance(value, list):
                        amount = random.randint(value[0], value[1])
                    elif isinstance(value, int):
                        amount = value
                    else:
                        raise TypeError(f"Invalid reward type: {type(value)}")
                    user.exp += amount
                    reward_amount[key] = amount
                case "favor":
                    if isinstance(value, list):
                        amount = random.randint(value[0], value[1])
                    elif isinstance(value, float | int):
                        amount = float(value)
                    else:
                        raise TypeError(f"Invalid reward type: {type(value)}")
                    user.favor += amount
                    reward_amount[key] = amount
                case _:
                    raise ValueError(f"Invalid reward key: {key}")
        await user.save()
        return reward_amount

    @classmethod
    async def check_username(cls, user_name: str) -> bool:
        """
        说明：
            判断数据表中是否有相同的 user_name
        参数：
            *user_name: 用户名
        """
        return await cls.exists(user_name=user_name)

    @classmethod
    async def check_exists(cls, platform: str, pid: str):
        """
        判断用户是否存在
        """
        return await cls.filter(bind__platform=platform, bind__pid=pid).exists()

    @classmethod
    async def get_user_by_uid(cls, uid: str):
        return await User.get(uid=uid)

    @classmethod
    async def get_user_by_pid(cls, pid: str):
        return await User.get(bind__pid=pid)

    @classmethod
    async def get_user_by_event(cls, event: Event):
        return await User.get(bind__pid=event.get_user_id())
