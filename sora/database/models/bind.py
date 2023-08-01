from tortoise import fields
from tortoise.models import Model


class UserBind(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    user_id = fields.CharField(max_length=10)
    """用户ID"""
    qq_id = fields.CharField(max_length=20, null=True, unique=True)
    """用户QQ ID"""
    qqguild_id = fields.CharField(max_length=50, null=True, unique=True)
    """用户QQ频道 ID"""
    discord_id = fields.CharField(max_length=20, null=True, unique=True)
    """Discord ID"""
    telegram_id = fields.CharField(max_length=20, null=True, unique=True)
    """Telegram ID"""
    bilibili_id = fields.CharField(max_length=20, null=True, unique=True)
    """Bilibili ID"""
    arcaea_id = fields.CharField(max_length=20, null=True, unique=True)
    """Arcaea ID"""
    phigros_id = fields.CharField(max_length=20, null=True, unique=True)
    """Phigros ID"""

    class Meta:
        table = "userBind"
