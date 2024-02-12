from typing import Literal

from sora.database import User


async def check_permission(
    uid: str, permission: Literal["ADMIN", "HELPER", "NORMAL", "BANNED"]
) -> bool:
    user = await User.get_user_by_uid(uid)
    return user.permission == permission
