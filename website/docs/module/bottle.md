---
title: 漂流瓶
date: 2023-03-04
categories:
 - 模块
tags:
 - 使用说明

---

# 漂流瓶
<ClientOnly><p><span class="span-group">群聊</span></p></ClientOnly>


::: danger 警告
禁止使用此功能传播任何违反 [使用条款](/docs/clause.md) 的内容。
:::

## 投掷
:::: code-group
::: code-group-item 中文
```
.扔漂流瓶 <文本|图片>
```
:::
::: code-group-item 英文
```
/bottle throw <text | picture>
```
:::
::::

## 捡取
若捡到的漂流瓶存在回复，则会显示最近三条，使用`.查看漂流瓶`查看所有回复
:::: code-group
::: code-group-item 中文
```
.捡漂流瓶
```
:::

::: code-group-item 英文
```
/bottle pick
```
:::
::::

## 评论
:::: code-group
::: code-group-item 中文
```
.评论漂流瓶 <编号> <文本>
```
:::

::: code-group-item 英文
```
/bottle comment <Bottle ID> <text>
```
:::
::::

## 举报
当举报次数大于5次时自动删除
```
.举报漂流瓶 <编号>
```

## 查看
为保证随机性，无评论时不展示漂流瓶内容
```
.查看漂流瓶 <编号>
```
---
<ClientOnly><p><span class="span-bot-admin">Bot 管理员</span> <span class="span-bot-helper">Bot 协助者</span></p></ClientOnly>

```
.漂流瓶详情 <编号>
```


## 删除
可以删除自己扔出的漂流瓶
```
.删除漂流瓶 <编号>
```

## 设置

### 功能开关
<ClientOnly><p><span class="span-admin">群管理员</span>  <span class="span-group">群主</span>  <span class="span-bot-admin">Bot 管理员</span>  <span class="span-bot-helper">Bot 协助者</span></p></ClientOnly>

```
/plugin block bottle
```
```
/plugin unblock bottle
```

### 删除
<ClientOnly><p><span class="span-bot-admin">Bot 管理员</span>  <span class="span-bot-helper">Bot 协助者</span></p></ClientOnly>

```
.删除漂流瓶 <编号>
```
```
.删除漂流瓶评论 <编号> <QQ号>
```

### 恢复
<ClientOnly><p><span class="span-bot-admin">Bot 管理员</span>  <span class="span-bot-helper">Bot 协助者</span></p></ClientOnly>

恢复被删除的漂流瓶
```
.恢复漂流瓶 <编号>
```

### 清空
<ClientOnly><p><span class="span-bot-admin">Bot 管理员</span>  <span class="span-bot-helper">Bot 协助者</span></p></ClientOnly>

```
.清空漂流瓶
```
