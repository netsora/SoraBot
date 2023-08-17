from sora.utils.user import (
    calculate_exp_threshold,
    calculate_next_exp_threshold,
)
from sora.database import UserInfo


async def get_rank(type: str, limit: int = 10):
    """
    说明：
        排行榜
    参数：
        * type: 排行榜类型
        * limit: 排行数量（默认10）

    返回：
        * QuerySet: 用户信息列表
    """

    query = UserInfo.all().order_by(f"-{type}").limit(limit)
    results = await query.values_list("user_id", "user_name", type)

    ranks: dict[int, dict[str, str | int]] = {}

    for rank, (user_id, user_name, count) in enumerate(results, start=1):
        ranks[rank] = {
            "user_id": user_id,
            "user_name": user_name,
            "count": count,
        }

    return ranks


async def get_user_rank(user_id: str, type: str) -> int:
    user = await UserInfo.get(user_id=user_id)
    if type == "coin":
        rank = await UserInfo.filter(coin__gt=user.coin).count()
    elif type == "exp":
        rank = await UserInfo.filter(exp__gt=user.exp).count()
    else:
        rank = await UserInfo.filter(favor__gt=user.favor).count()

    return rank + 1


def generate_progress_bar(user_level: int, user_exp: int, bar_length: int = 20):
    current_max_exp = calculate_exp_threshold(user_level)
    next_max_exp = calculate_next_exp_threshold(user_level)

    progress_bar = ""

    for i in range(int(float(current_max_exp / next_max_exp) * bar_length)):
        progress_bar = progress_bar + "|"
    for i in range(bar_length - len(progress_bar)):
        progress_bar = progress_bar + " "
    progress_bar = "[" + progress_bar + "]"
    progress_text = f"Lv.{user_level + 1}: {user_exp} / {next_max_exp}"
    return progress_bar, progress_text
