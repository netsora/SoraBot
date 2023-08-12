from sora.config import Config


base_exp = Config.add_config(
    "Level",
    "base_exp",
    150,
    name="初始经验阈值",
    help="指用户从 Lv.1 升入 Lv.2 一共需要的经验点",
)
max_level = Config.add_config(
    "Level",
    "max_level",
    60,
    name="最大等级",
    help="指等级上限。若等级达到该上限，溢出的经验会转换为硬币",
)
cardinality = Config.add_config(
    "Level",
    "cardinality",
    1.2,
    name="经验系数",
    help="经验系数用于控制经验阈值的增长速度。较大的经验增长系数将导致经验阈值快速增加，而较小的系数将导致经验阈值增长较慢",
)
