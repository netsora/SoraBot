from tortoise import fields
from tortoise.models import Model


class Item(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """物品 ID"""
    name = fields.CharField(max_length=20)
    """物品名称"""
    description = fields.TextField(null=True, default="神秘")
    """物品介绍"""
    amount = fields.BigIntField()
    """物品数量"""

    class Meta:
        table = "Item"
