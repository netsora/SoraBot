# SoraBot 贡献指南
首先，感谢大家为 SoraBot 贡献代码
本张旨在引导你更规范地向 SoraBot 提交贡献，请务必认真阅读。

## 提交 Issue

在提交 Issue 前，我们建议你先查看 [FAQ](https://github.com/orgs/netsora/discussions) 与 [已有的 Issues](https://github.com/netsora/SoraBot/issues)，以防重复提交。

### 报告问题、故障与漏洞

SoraBot 仍然是一个不够稳定的开发中项目，如果你在使用过程中发现问题并确信是由 SoraBot 引起的，欢迎提交 Issue。

### 建议功能

SoraBot 还未进入正式版，欢迎在 Issue 中提议要加入哪些新功能。

为了让开发者更好地理解你的意图，请认真描述你所需要的特性，可能的话可以提出你认为可行的解决方案。

## Pull Request

SoraBot 使用 poetry 管理项目依赖，由于 pre-commit 也经其管理，所以在此一并说明。

下面的命令能在已安装 poetry 和 yarn 的情况下帮你快速配置开发环境。

```cmd
# 安装 python 依赖
poetry install
# 安装 pre-commit git hook
pre-commit install
```

### 使用 GitHub Codespaces（Dev Container）

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=master&repo=645755460)

### 使用 GitPod

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#/https://github.com/netsora/SoraBot)

### Commit 规范

请确保你的每一个 commit 都能清晰地描述其意图，一个 commit 尽量只有一个意图。

SoraBot 的 commit message 格式遵循 gitmoji 规范，在创建 commit 时请牢记这一点。


### 工作流概述

`master` 分支为 SoraBot 的开发分支，在任何情况下都请不要直接修改 `master` 分支，而是创建一个目标分支为 `sorabot:master` 的 Pull Request 来提交修改。Pull Request 标题请尽量更改成中文，以便阅读。

如果你不是 netsora 团队的成员，可在 fork 本仓库后，向本仓库的 master 分支发起 Pull Request，注意遵循先前提到的 commit message 规范创建 commit。我们将在 code review 通过后通过 squash merge 方式将您的贡献合并到主分支。

### 撰写文档

SoraBot 的文档使用 [vuepress-reco](http://v2.vuepress-reco.recoluan.com/)，它有一些 [Markdown 特性](http://v2.vuepress-reco.recoluan.com/docs/theme/custom-container.html) 可能会帮助到你。

如果你需要在本地预览修改后的文档，可以使用 yarn 安装文档依赖后启动 dev server，如下所示：

```cmd
yarn install
yarn start
```

SoraBot 文档并没有具体的行文风格规范，但我们建议你尽量写得简单易懂。

以下是比较重要的编写与排版规范。目前 SoraBot 文档中仍有部分文档不完全遵守此规范，如果在阅读时发现欢迎提交 PR。

1. 中文与英文、数字、半角符号之间需要有空格。例：`SoraBot 是基于 Nonebot2 开发的多平台机器人。`
2. 若非英文整句，使用全角标点符号。例：`现在你可以看到机器人回复你：“Hello, World !”。`
3. 直引号 `「」` 和弯引号 `“”` 都可接受，但同一份文件里应使用同种引号。
4. **不要使用斜体**，你不需要一种与粗体不同的强调。除此之外，你也可以考虑使用 vuepress 提供的[扩展](https://vuepress-theme-reco.recoluan.com/docs/theme/custom-container.htm)。
5. 文档中应以“我们”指代林汐开发者（即管理员与协助者），以“您”指代机器人的使用者。

以上由[社区创始人 richardchien 的中文排版规范](https://stdrc.cc/style-guides/chinese)补充修改得到。

如果你需要编辑器检查 Markdown 规范，可以在 VSCode 中安装 markdownlint 扩展。

### 文件夹规范

实际上，若无开发需求，您暂时不用了解每一个文件的作用

```cmd
📦 SoraBot
├── 📂 go-cqhttp
│   └── ......
├── 📂 SoraBot
│   └── 📂 sora
│       └── 📂 configs          // 配置
│       └── 📂 database         // 数据库
│       └── 📂 plugins          // 插件
│       └── 📂 utils            // 工具
│       └── 📜 ...           
│   └── 📂 website
│       └── 📂 .vuepress
│           └── 📂 styles       // 文档样式
│           └── 📂 public       // 静态资源
│           └── 📜 README.md    // 配置文件
│       └── 📂 blogs            // 博客文章（开发文档
│       └── 📂 docs             // 使用文档
│       └── 📜 package.json
│       └── 📜 README.md
│   └── 📜 .env                 // 配置文件
│   └── 📜 .env.prod            // 配置文件
│   └── 📜 bot.py               // 启动文件
│   └── 📜 matcher_patch.py
│   └── 📜 poetry.lock          // 依赖管理
│   └── 📜 pyproject.toml       
|   └── 📜 README.md       
|   └── 📜 requirements.txt     // 依赖列表   
```

### 参与开发

SoraBot 的代码风格遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 与 [PEP 484](https://www.python.org/dev/peps/pep-0484/) 规范，请确保你的代码风格和项目已有的代码保持一致，变量命名清晰，有适当的注释与测试代码。
