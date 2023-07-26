import httpx

try:
    import ujson as json
except ImportError:
    import json

from nonebot.internal.adapter import Message

from sora.utils import PROXY


def get_message_at(data: str) -> list:
    """
    获取at列表
    :param data: event.json()
    """
    at_list = []
    data_ = json.loads(data)
    try:
        for msg in data_["message"]:
            if msg["type"] == "at":
                at_list.append(int(msg["data"]["qq"]))
        return at_list
    except Exception:
        return []


async def get_message_img(data: str | Message) -> list[str]:
    """
    获取消息中所有的 图片 的链接

    :param data: event.json()
    """
    img_list = []
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            for msg in message:
                if msg["type"] == "image":
                    img_list.append(msg["data"]["url"])
                elif msg["type"] == "attachments":
                    img_list.append(msg["data"]["url"])
                else:
                    img_list.append(msg["data"]["url"])
    else:
        if data["image"]:
            for seg in data["image"]:
                img_list.append(seg.data["url"])
        elif data["attachment"]:
            for seg in data["attachment"]:
                img_list.append(seg.data["url"])
        else:
            if photo := data["photo"]:
                img_list.append(photo[0].data["file"])

    return img_list


def get_message_face(data: str | Message) -> list[str]:
    """
    获取消息中所有的 face Id

    :param data: event.json()
    """
    face_list = []
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            for msg in message:
                if msg["type"] == "face":
                    face_list.append(msg["data"]["id"])
    else:
        for seg in data["face"]:
            face_list.append(seg.data["id"])
    return face_list


def get_message_img_file(data: str | Message) -> list[str]:
    """
    获取消息中所有的 图片file

    :param data: event.json()
    """
    file_list = []
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            for msg in message:
                if msg["type"] == "image":
                    file_list.append(msg["data"]["file"])
    else:
        for seg in data["image"]:
            file_list.append(seg.data["file"])
    return file_list


def get_message_text(data: str | Message) -> str:
    """
    获取消息中 纯文本 的信息

    :param data: event.json()
    """
    result = ""
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            if isinstance(message, str):
                return message.strip()
            for msg in message:
                if msg["type"] == "text":
                    result += msg["data"]["text"].strip() + " "
        return result.strip()
    else:
        for seg in data["text"]:
            result += seg.data["text"] + " "
    return result.strip()


def get_local_proxy() -> str | None:
    """
    获取 .env* 中设置的代理
    """
    return PROXY or None


async def get_user_avatar(qq: int) -> bytes | None:
    """
    快捷获取用户头像（仅支持 v11）
    :param qq: qq号
    """
    url = f"http://q1.qlogo.cn/g?b=qq&nk={qq}&s=160"
    async with httpx.AsyncClient() as client:
        for _ in range(3):
            try:
                return (await client.get(url)).content
            except TimeoutError:
                pass
    return None
