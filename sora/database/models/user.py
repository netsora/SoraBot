import datetime

from tortoise import fields
from tortoise.models import Model
from nonebot.internal.permission import Permission as Permission


class UserInfo(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    user_id = fields.CharField(max_length=10, unique=True)
    """指用户注册后 Sora 为其分配的ID"""
    user_name = fields.CharField(max_length=10, unique=True)
    """用户昵称"""
    password = fields.CharField(max_length=20)
    """用户密码"""
    level: int = fields.IntField()
    """等级"""
    exp: int = fields.IntField()
    """经验值"""
    coin: int = fields.IntField()
    """硬币数"""
    jrrp: int = fields.IntField()
    """好感度"""
    birthday: datetime.datetime = fields.DatetimeField(null=True)
    """生日"""
    register_time: datetime.datetime = fields.DatetimeField(auto_now_add=True)
    """注册日期"""
    permission = fields.CharField(max_length=10)

    class Meta:
        table = "user_info"
