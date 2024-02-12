import random
import string
import hashlib
import datetime


def md5(text: str) -> str:
    """
    md5加密

    :param text: 文本
    :return: md5加密后的文本
    """
    md5_ = hashlib.md5()
    md5_.update(text.encode())
    return md5_.hexdigest()


def generate_id():
    """
    说明：
        生成九位数用户ID
    结构：
        日期+随机数
    """
    current_time = datetime.datetime.now().strftime("%Y%m%d")  # 获取当前日期
    random_number = random.randint(10, 99)  # 生成一个随机数
    if random_number < 10:
        random_number = "0" + str(random_number)
    user_id: str = f"{current_time}{random_number}"  # 结合日期和随机数生成ID
    return user_id


def random_hex(length: int, prefix: str | None = None) -> str:
    """
    说明：
        生成指定长度的随机字符串
    参数：
        * length: 长度
        * prefix: 增加前缀（可选）
    """
    result = hex(random.randint(0, 16**length)).replace("0x", "").upper()
    if len(result) < length:
        result = "0" * (length - len(result)) + result
    if prefix is not None:
        result = prefix + result[5:]
    return result


def random_text(length: int, prefix: str | None = None) -> str:
    """
    说明：
        生成指定长度的随机字符串
    参数：
        * length: 长度
        * prefix: 前缀（可选）
    """
    result = "".join(random.sample(string.ascii_lowercase + string.digits, length))
    if prefix is not None:
        result = prefix + result[5:]
    return result
