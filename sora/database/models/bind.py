from tortoise import fields
from tortoise.models import Model


class UserBind(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    user_id = fields.CharField(max_length=10)
    """用户ID"""
    user_origin_id = fields.CharField(max_length=10, null=True)
    """用户原始ID"""
    platform = fields.CharField(max_length=50)
    """绑定平台"""
    account = fields.CharField(max_length=50)
    """平台ID"""

    class Meta:
        table = "userBind"

    @classmethod
    async def check_account_exists(cls, platform: str, account: str) -> bool:
        """
        说明：
            判断 platform 账号 是否存在于 UserBind 表中

        参数：
            * platform: 平台
            * account: 平台ID

        返回：
            如果存在则返回 `true`,
            反之则返回 `false`
        """
        exists = await cls.filter(platform=platform, account=account).exists()
        return exists

    @classmethod
    async def bind(cls, bind_id: str, platform: str, account: str):
        """
        说明：
            绑定账号
        参数：
            * bind_id: 绑定 ID
            * platform: 平台
            * account: 平台ID
        """
        obj = await cls.filter(platform=platform, account=account).first()
        if obj:
            obj.user_origin_id = obj.user_id
            obj.user_id = bind_id
            await obj.save()

    @classmethod
    async def rebind(cls, user_id: str, platform: str):
        """
        说明：
            取消绑定
        参数：
            * user_id: 用户 ID
            * platform: 平台
        """
        obj = await cls.filter(user_id=user_id, platform=platform).first()
        if obj:
            obj.user_id = obj.user_origin_id
            await obj.save()

    @classmethod
    async def get_bind_info(cls, account):
        """
        说明：
            获取用户绑定信息
        参数：
            *account: 平台ID
        """
        user_data = await cls.filter(account=account).values(
            "user_id", "platform", "account"
        )
        user_id = user_data[0]["user_id"]
        data = await cls.filter(user_id=user_id).values(
            "user_id", "platform", "account"
        )
        return data
