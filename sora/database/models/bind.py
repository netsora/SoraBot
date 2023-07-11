from tortoise import fields
from tortoise.models import Model


class UserBind(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    user_id: str = fields.CharField(max_length=10)
    """用户ID"""
    user_qq_id: str = fields.CharField(max_length=20, null=True)
    """用户QQ ID"""
    user_qqguild_id: str = fields.CharField(max_length=50, null=True)
    """用户QQ频道 ID"""
    discord_id: str = fields.CharField(max_length=20, null=True)
    """Discord ID"""
    bilibili_id: str = fields.CharField(max_length=20, null=True)
    """Bilibili ID"""
    arcaea_id: str = fields.CharField(max_length=20, null=True)
    """Arcaea ID"""
    phigros_id: str = fields.CharField(max_length=20, null=True)
    """Phigros ID"""

    class Meta:
        table = "user_bind"
