from pydantic import BaseModel


class GoCQHTTPAccountList(BaseModel):
    uin: int
    password: str
    protocol: int


class WithGoCQHTTP(BaseModel):
    enabled: bool
    accounts: list[GoCQHTTPAccountList] | None
    download_domain: str
    download_version: str
    gocqhttp_webui_username: str
    gocqhttp_webui_password: str


class Coin(BaseModel):
    login: int
    sign: list[int]


class Jrrp(BaseModel):
    login: int
    sign: int


class Exp(BaseModel):
    login: int
    sign: int


class Award(BaseModel):
    Coin: Coin
    Jrrp: Jrrp
    Exp: Exp


class ConfigModel(BaseModel):
    ConfigVersion: str
    WithGoCQHTTP: WithGoCQHTTP
    Award: Award


class RuntimeConfig(BaseModel):
    gocqhttp_accounts: list | None
    gocqhttp_download_domain: str
    gocqhttp_version: str
    gocqhttp_webui_username: str
    gocqhttp_webui_password: str
