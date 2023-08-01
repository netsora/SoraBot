from tortoise import fields
from tortoise.models import Model


class UserSign(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    user_id = fields.CharField(max_length=10)
    """指用户注册后 Sora 为其分配的ID"""
    total_days = fields.IntField(default=0)
    """累计签到天数"""
    continuous_days = fields.IntField(default=0)
    """连续签到天数"""
    last_day = fields.DateField(auto_now=True, null=True, format="%Y-%m-%d")
    """上次签到日期"""

    class Meta:
        table = "signInfo"
