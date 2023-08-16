from typing import Annotated

from nonebot.params import Depends

from sora.utils.user import get_bind_info
from sora.utils.user import get_user_info
from sora.database import UserBind as _UserBind
from sora.database import UserInfo as _UserInfo


BindInfo = Annotated[_UserBind, Depends(get_bind_info)]
UserInfo = Annotated[_UserInfo, Depends(get_user_info)]
