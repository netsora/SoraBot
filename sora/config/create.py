from pathlib import Path

from .console import C, Console

# from ipaddress import IPv4Address


console = Console(C())


def _init_config(conf_path: Path, default_conf_path: Path):
    raw_conf = default_conf_path.read_text("utf-8")

    console.print("\n[b]是林汐吖！[/b]\n", style="#00bee6")

    console.warn("文档地址: https://sorabot.netlify.app")
    console.info("这是你第一次启动本项目, 请根据提示填写信息")
    console.info("如中途填写出错, 你可以直接退出, 再次启动以重新填写")
    console.info("如需使用默认值, Enter 跳过方可\n")

    console.info("[b]Bot 主体设置[/b]\n", style="white")
    console.warn("由于技术原因，暂无法实现。主体设置请直接修改 .env 文件")
    # host = console.input(
    #     "Bot 监听的主机名 (IP). 建议: [green]0.0.0.0[/green] (默认: [green]127.0.0.1[/green])",
    #     "127.0.0.1",
    #     IPv4Address,
    #     "输入不正确 示例: 127.0.0.1",
    # )
    # port = console.input(
    #     "Bot 对外开放的端口 (Port). 范围建议: [green]10000-60000[/green] (默认: [green]20000[/green])",
    #     "20000",
    #     int,
    #     "输入不正确 示例: 20000",
    # )
    # bot_admin = console.input(
    #     "Bot 管理员, 即 Bot 的[b]主人[/b]. 可填多个, 用英文逗号 (,) 隔开 (默认: [green]2740324073[/green])",
    #     "2740324073",
    #     str,
    #     "输入不正确 示例: 2740324073",
    # )
    # bot_helper = console.input(
    #     "Bot 协助者, 即 [b]协助Bot管理员的人[/b]. 可填多个, 用英文逗号 (,) 隔开",
    #     "2740324073",
    #     str,
    #     "输入不正确 示例: 2740324073"
    # )
    # proxy = console.input(
    #     "是否有代理. 格式参考: http(s)://127.0.0.1:8100 (如无请 Enter 以跳过)",
    #     str(),
    #     str,
    #     "输入不正确 示例: http://127.0.0.1:8100",
    # )
    # console.success("Bot 主体配置完成\n")

    console.info("[b]Bot 进阶设置[/b]\n", style="white")
    is_use_with_gocqhttp = console.input(
        "是否启用内置的 gocqhttp? (y/n) (默认: y)", "y", str, "输入不正确 示例: y"
    )
    if is_use_with_gocqhttp in ["y", "Y", "true", "True", "是"]:
        uin = console.input("Bot 账号", "28717103871", int, "输入不正确 示例: 2871703871")
        password = console.input(
            "Bot 账号密码 (已做隐藏处理, 如不确定是否填写正确, 请查阅填写完毕后所生成的文件: config_manage.yml)",
            str(),
            str,
            password=True,
        )
        protocol = console.input(
            "Bot 登录设备类型. 范围: 0-6, 具体请参考文档 (默认: 6)",
            "6",
            int,
            "输入不正确 范围 0-6",
        )
        download_domain = console.input(
            "gocqhttp 下载源域名设置. 具体请参考文档: 部署项目-设置 (默认: github.com)", "github.com"
        )

        console.success("内置 gocqhttp 配置完成. 支持多账号, 具体请参考文档: 部署项目-设置\n")

        raw_conf = raw_conf.replace("{is_use_with_gocqhttp}", "true")
        raw_conf = raw_conf.replace("{download_domain}", download_domain)  # type: ignore
        raw_conf = raw_conf.replace(
            "{accounts}",
            """
            - uin: {uin}
              password: "{password}"
              protocol: {protocol}""".format(
                uin=str(uin), password=password, protocol=str(protocol)
            ),
        )  # type: ignore

    else:
        console.info("已跳过\n")

        raw_conf = raw_conf.replace("{is_use_with_gocqhttp}", "false")
        raw_conf = raw_conf.replace("{account}", "[]")

    console.success("[white]至此, 所需基本配置已填写完毕[white]")

    with open(conf_path, "w", encoding="utf-8") as w:
        w.write(raw_conf)
