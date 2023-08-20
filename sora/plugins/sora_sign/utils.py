from sora.utils.user import (
    calculate_exp_threshold,
    calculate_next_exp_threshold,
)


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
