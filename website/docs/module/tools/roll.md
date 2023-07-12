---
title: Roll
date: 2023-05-13
categories:
 - 模块
tags:
 - 使用说明
---

## Roll
<ClientOnly><p><span class="span-friend">私聊</span> <span class="span-group">群聊</span></p></ClientOnly>
让 林汐 帮你做选择！


---

### 随机数字
从 0~数字 之间随机roll一个数字
```
/roll [数字](默认100)
```

### 随机事件
从所给事件中随机一个并返回
:::: code-group
::: code-group-item 指令
```
/roll [事件1] [事件2] [···]
```
:::
::: code-group-item 🌰栗子
```
/roll 吃饭 睡觉 打豆豆
```
:::
::::

### 犹豫不决
林汐为你做决定！
:::: code-group
::: code-group-item 指令
```bash
（只可意会，建议看例子
```
:::
::: code-group-item 🌰栗子
```bash
# bot会在 你是耳聋 和 你不是耳聋 之间随机一个并返回。
/roll 我是不是耳聋

# 相同道理还有：有没有、去不去、上不上等这种 x不x 的规则
```
:::
::::