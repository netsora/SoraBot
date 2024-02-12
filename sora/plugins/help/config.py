from pydantic import Field

from sora.config import BaseConfig


class Config(BaseConfig):
    index: bool = False
    """是否展示索引"""

    max_length: int = -1
    """单个页面展示的最大长度"""

    message_count: int = Field(10, ge=1, le=120)
    """统计命令显示的消息数量"""
