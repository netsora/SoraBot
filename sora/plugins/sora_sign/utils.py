from sora.config import ConfigManager
from sora.utils.user import calculate_exp_threshold, calculate_next_exp_threshold

base_exp = ConfigManager.get_config("Level")["base_exp"]
max_level = ConfigManager.get_config("Level")["max_level"]
cardinality = ConfigManager.get_config("Level")["cardinality"]


def generate_progress_bar(user_level: int, user_exp: int, bar_length: int = 10):
    current_max_exp = calculate_exp_threshold(user_level)
    next_max_exp = calculate_next_exp_threshold(user_level)

    filled_length = int(bar_length * (user_exp - current_max_exp) / (next_max_exp - current_max_exp))
    remaining_length = bar_length - filled_length
    progress_bar = "[" + "|" * filled_length + " " * remaining_length + "]"
    progress_text = f"Lv.{user_level + 1}: {user_exp} / {next_max_exp}"

    return progress_bar, progress_text
