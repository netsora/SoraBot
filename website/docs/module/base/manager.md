---
title: 管理
date: 2023-05-03
categories:
 - 模块
tags:
 - 使用说明
---

# 管理
管理 林汐 的各项服务

## 封禁
<ClientOnly><p><span class="span-bot-admin">Bot 管理员</span> <span class="span-bot-helper">Bot 协助者</span></p></ClientOnly>

::: warning 警告 
被封禁的用户（或群聊）无法使用 林汐 提供的所有服务
:::

### 用户

**封禁**
```
/封禁用户
```
**解封**
```
/解封用户
```

### 群聊

**封禁**
```
/封禁群聊
```
**解封**
```
/解封群聊
```


## 服务

### 群聊
<ClientOnly><p><span class="span-admin">群管理员</span>  <span class="span-group">群主</span>  <span class="span-bot-admin">Bot 管理员</span>  <span class="span-bot-helper">Bot 协助者</span></p></ClientOnly>

::: tip 提示
服务名可通过发送 `/服务列表` 或 `/帮助列表` 获取。
:::

**禁用**
```
/禁用[服务名]
```

**启用**
```
/启用[服务名]
```

### 个人
<ClientOnly><p><span class="span-bot-admin">Bot 管理员</span>  <span class="span-bot-helper">Bot 协助者</span></p></ClientOnly>
针对某一用户禁用（或启用）某服务

**禁用**
```
对用户<QQ号>禁用<服务名>
```

**启用**
```
对用户<QQ号>启用<服务名>
```

### 全局
<ClientOnly><p><span class="span-bot-admin">Bot 管理员</span>  <span class="span-bot-helper">Bot 协助者</span></p></ClientOnly>
全局禁用（或启用）某服务

**禁用**
```
/全局禁用[服务名]
```

**启用**
```
/全局启用[服务名]
```

## 申请
<ClientOnly><p><span class="span-bot-admin">Bot 管理员</span>  <span class="span-bot-helper">Bot 协助者</span></p></ClientOnly>

### 好友申请

#### 获取
获取好友申请列表

```
/好友申请列表
```

#### 同意
同意好友申请

```
/同意好友
```

#### 拒绝
拒绝好友申请

```
/拒绝好友
```

### 入群邀请

#### 获取
获取群邀请列表

```
/群邀请列表
```

#### 同意
同意他人群聊邀请

```
/同意邀请
```

#### 拒绝
拒绝他人群聊邀请

```
/拒绝邀请
```

## 追踪
获取报错信息

:::: code-group
::: code-group-item 中文
```
/追踪
```
:::
::: code-group-item 英文
```
/track
```
:::
::::
