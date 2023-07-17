from pathlib import Path

# 配置路径
SORA_CONFIG = Path() / "config.yaml"

# 图片路径
IMAGE_PATH = Path() / "resources" / "image"
# 语音路径
RECORD_PATH = Path() / "resources" / "record"
# 文本路径
TEXT_PATH = Path() / "resources" / "text"
# 字体路径
FONT_PATH = Path() / "resources" / "font"
# 网页模板路径
TEMPLATE_PATH = Path() / "resources" / "template"


# 插件数据路径
PLUGIN_PATH = Path() / "data" / "plugin"

# 数据库路径
DATABASE_PATH = Path().cwd() / "data" / "database"
# 用户数据路径
USER_INFO_DB_PATH = DATABASE_PATH / "user.db"
# 用户绑定数据路径
USER_BIND_DB_PATH = DATABASE_PATH / "bind.db"
# 用户签到数据路径
USER_SIGN_DB_PATH = DATABASE_PATH / "sign.db"


def load_path():
    IMAGE_PATH.mkdir(parents=True, exist_ok=True)
    RECORD_PATH.mkdir(parents=True, exist_ok=True)
    TEXT_PATH.mkdir(parents=True, exist_ok=True)
    FONT_PATH.mkdir(parents=True, exist_ok=True)
    TEMPLATE_PATH.mkdir(parents=True, exist_ok=True)
    DATABASE_PATH.mkdir(parents=True, exist_ok=True)


load_path()
