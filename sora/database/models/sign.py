from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class Sign(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    uid = fields.CharField(max_length=10)
    """用户 ID"""
    total_days = fields.IntField(default=0)
    """累计签到天数"""
    continuous_days = fields.IntField(default=0)
    """连续签到天数"""
    last_sign = fields.DatetimeField(null=True, alias="last_day")
    """上次签到日期"""

    class Meta:
        table = "Sign"

    @classmethod
    async def get_today_rank(cls, limit: int = 10) -> list:
        """
        说明：
            获取当日签到排名前十的用户
        参数：
            * limit: 排名限制（默认排名 top10）
        """
        today = datetime.today()
        return await cls.filter(last_sign=today).order_by("-total_days").limit(limit)

    @classmethod
    async def get_total_rank(cls, limit: int = 10) -> list:
        """
        说明：
            获取签到总排名
        参数：
            * user_id
            * limit: 排名限制（默认排名 top10）
        """
        return (
            await cls.filter(last_sign__isnull=False)
            .order_by("-total_days")
            .limit(limit)
        )

    @classmethod
    async def get_sign_info(cls, uid: str):
        """
        说明：
            获取用户签到信息
        参数：
            * uid
        """
        return await cls.get_or_none(uid=uid)
