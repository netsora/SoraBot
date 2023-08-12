import shutil

from datetime import date
from tortoise import fields
from tortoise.models import Model
from nonebot.internal.permission import Permission as Permission

from sora.config.path import DATABASE_PATH


class UserInfo(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    user_id = fields.CharField(max_length=10, unique=True)
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

    class Meta:
        table = "userInfo"

    @classmethod
    async def create_user(
        cls,
        user_id: str,
        user_name: str,
        level: int = 1,
        exp: int = 0,
        coin: int = 50,
        favor: int = 0,
        birthday: date | None = None,
        permission: str = "USER",
    ):
        """
        说明：
            创建用户账号
        参数：
            * user_id: 用户ID
            * user_name: 用户名
            * level: 等级
            * exp: 经验值
            * coin: 硬币
            * favor: 好感度
            * birthday: 出生日期，默认为 None
            * permission: 权限
        """
        await cls.update_or_create(
            user_id=user_id,
            user_name=user_name,
            level=level,
            exp=exp,
            coin=coin,
            favor=favor,
            birthday=birthday,
            permission=permission,
        )
        path = DATABASE_PATH / "user" / f"{user_id}"
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

    @classmethod
    async def delete_user(cls, user_id):
        """
        说明：
            删除用户账号及数据
        参数：
            * user_id: 用户ID
        """
        user = await cls.filter(user_id=user_id).first()
        if user:
            await user.delete()
            shutil.rmtree(DATABASE_PATH / "user" / f"{user_id}")

    @classmethod
    async def check_username(cls, user_name: str):
        """
        说明：
            判断数据表中是否有相同的 user_name
        参数：
            *user_name: 用户名
        """
        user_exist = await cls.exists(user_name=user_name)
        return user_exist

    @classmethod
    async def check_user_exist(cls, user_id: str) -> bool:
        user = await UserInfo.get_or_none(user_id=user_id)
        if user is None:
            return False
        return True
