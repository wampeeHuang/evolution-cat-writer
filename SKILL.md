---
name: evolution-cat-writer
description: |
  进化猫的公众号长文写作技能（已归档）。触发后路由到 persona-article。
  触发词：写文章、写稿子、帮我写、续写、扩写、公众号文章、长文、出稿、按我的风格写。
---

# 进化猫公众号长文写作

> **本 Skill 已归档。** 所有写作逻辑已迁移到 `evolution-cat-article` 6 阶段管线。

## 路由

当用户触发本 Skill 时，直接调用 `evolution-cat-article` skill，参数 `--light`。

```
触发 evolution-cat-article --light
```

不再在本 Skill 内独立执行写作流程。所有风格规则、质检体系、杀稿门禁由 evolution-cat-article 统一管理。

## 迁移说明

| v6.x（旧） | v7.0（新） |
|-----------|-----------|
| 独立 writer skill | 路由到 evolution-cat-article --light |
| 自有写作流程 | 6 阶段管线（判→搜→构→写→审→发） |
| 独立人设定义 | 进化猫单人设，血肉/骨架双层 |
