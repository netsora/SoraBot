from datetime import date
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

    @classmethod
    async def get_today_rank(cls, limit: int = 10):
        """
        说明：
            获取当日签到排名前十的用户
        参数：
            * limit: 排名限制（默认排名 top10）
        """
        today = date.today()
        return (
            await UserSign.filter(last_day=today).order_by("-total_days").limit(limit)
        )

    @classmethod
    async def get_total_rank(cls, limit: int = 10):
        """
        说明：
            获取签到总排名
        参数：
            * user_id
            * limit: 排名限制（默认排名 top10）
        """
        return (
            await UserSign.filter(last_day__isnull=False)
            .order_by("-total_days")
            .limit(limit)
        )

    @classmethod
    async def get_user_sign_info(cls, user_id: str):
        """
        说明：
            获取用户签到信息
        参数：
            * user_id
        """
        user_sign = await cls.filter(user_id=user_id).first()

        total_days = user_sign.total_days if user_sign else 0
        continuous_days = user_sign.continuous_days if user_sign else 0

        return total_days, continuous_days
