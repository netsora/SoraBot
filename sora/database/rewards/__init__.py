from typing import Any
from pydantic import Field, BaseModel


class Coin(BaseModel):
    """硬币奖励"""

    amount: Any = Field(0)
    """数量。可选，既可以是整数列表 [int, int]，又可以是整数且必须大于0"""

    def __str__(self):
        return str(self.amount)

    def __getitem__(self, index):
        if self.amount is None:
            raise TypeError("无法对 None 执行索引")
        elif isinstance(self.amount, int):
            if index != 0:
                raise IndexError("索引超出范围")
            return self.amount
        elif isinstance(self.amount, list):
            return self.amount[index]
        else:
            raise TypeError("不支持的索引类型")


class Exp(BaseModel):
    """经验值奖励"""

    amount: Any = Field(0)
    """数量。可选，如果存在则必须大于0"""

    def __str__(self):
        return str(self.amount)

    def __getitem__(self, index):
        if self.amount is None:
            raise TypeError("无法对 None 执行索引")
        elif isinstance(self.amount, int):
            if index != 0:
                raise IndexError("索引超出范围")
            return self.amount
        elif isinstance(self.amount, list):
            return self.amount[index]
        else:
            raise TypeError("不支持的索引类型")


class Favor(BaseModel):
    """好感度奖励"""

    amount: Any = Field(0)
    """数量。可选，如果存在则必须大于0"""

    def __str__(self):
        return str(self.amount)

    def __getitem__(self, index):
        if self.amount is None:
            raise TypeError("无法对 None 执行索引")
        elif isinstance(self.amount, int):
            if index != 0:
                raise IndexError("索引超出范围")
            return self.amount
        elif isinstance(self.amount, list):
            return self.amount[index]
        else:
            raise TypeError("不支持的索引类型")


class EventReward(BaseModel):
    """事件模型"""

    name: str
    """事件名称"""
    description: str
    """事件描述"""
    coin_reward: Coin = Field(Coin(amount=0), description="硬币奖励")
    """硬币奖励"""
    exp_reward: Exp = Field(Exp(amount=0), description="经验值奖励")
    """经验值奖励"""
    favor_reward: Favor = Field(Favor(amount=0), description="好感度奖励")
    """好感度奖励"""


class AchieveReward(BaseModel):
    """成就模型"""

    name: str
    """成就名称"""
    description: str
    """成就描述"""
    coin_reward: Coin = Field(Coin(amount=0), description="硬币奖励")
    """硬币奖励"""
    exp_reward: Exp = Field(Exp(amount=0), description="经验值奖励")
    """经验值奖励"""
    favor_reward: Favor = Field(Favor(amount=0), description="好感度奖励")
    """好感度奖励"""
