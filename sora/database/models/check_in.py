import datetime

from tortoise import fields
from tortoise.models import Model


class UserCheckInfo(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    user_id = fields.CharField(max_length=8)
    """指用户注册后 Sora 为其分配的ID"""
    total_days: int = fields.IntField()
    """累计签到天数"""
    continuous_days: int = fields.IntField()
    """连续签到天数"""
    last_day: datetime.datetime = fields.DatetimeField(null=True)
    """上次签到日期"""

    class Meta:
        table = "user_check_info"
