from .config import GameConfig

level_config = (GameConfig.load_config("game")).level


def calc_exp_threshold(level: int) -> int:
    """
    计算经验阈値
    :param level:用户当前的等级
    :return: threshold
    """
    base_exp = level_config.base_exp
    cardinality = level_config.cardinality
    threshold = round(int(base_exp * (cardinality**level)) / 10) * 10
    return threshold


def calc_next_exp_threshold(level: int) -> int:
    """计算下一等级的经验阈值"""
    threshold = calc_exp_threshold(level + 1)
    return threshold


def generate_progress_bar(user_level: int, user_exp: int, bar_length: int = 20):
    current_max_exp = calc_exp_threshold(user_level)
    next_max_exp = calc_next_exp_threshold(user_level)

    progress_bar = ""

    for i in range(int(float(current_max_exp / next_max_exp) * bar_length)):
        progress_bar = progress_bar + "|"
    for i in range(bar_length - len(progress_bar)):
        progress_bar = progress_bar + " "
    progress_bar = "[" + progress_bar + "]"
    progress_text = f"Lv.{user_level + 1}: {user_exp} / {next_max_exp}"
    return progress_bar, progress_text
