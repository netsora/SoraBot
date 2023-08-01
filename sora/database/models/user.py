from tortoise import fields
from tortoise.models import Model
from nonebot.internal.permission import Permission as Permission


class UserInfo(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    user_id = fields.CharField(max_length=10, unique=True)
    """指用户注册后 Sora 为其分配的ID"""
    user_name = fields.CharField(max_length=10, unique=True)
    """用户昵称"""
    password = fields.CharField(max_length=20)
    """用户密码"""
    level = fields.IntField(default=0)
    """等级"""
    exp = fields.IntField(default=0)
    """经验值"""
    coin = fields.IntField(default=0)
    """硬币数"""
    jrrp = fields.IntField(default=0)
    """好感度"""
    birthday = fields.DatetimeField(null=True)
    """生日"""
    register_time = fields.DatetimeField(auto_now_add=True)
    """注册日期"""
    permission = fields.CharField(max_length=10)

    class Meta:
        table = "userInfo"
