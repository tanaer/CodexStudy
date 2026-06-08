---
description: "AGENTS.md 项目规则指南，说明如何写入项目命令、代码风格、禁用事项、验证方式、团队约定和本地私有规则，让 Codex 更懂仓库。"
redirectFrom:
  - /guide/14-agents-md.html
---

# AGENTS.md 项目规则

对于 Codex 而言，我们每开启一个新的对话窗口，它都会进入一个全新的上下文。它不记得之前发生了什么，对于整个项目的记忆都是空白的。

所以 Codex 提供了记忆系统来解决这样的问题

`AGENTS.md` 是给 Codex 这类编码代理看的项目说明文件。它可以描述项目结构、开发命令、测试要求、代码风格和协作边界。

::: tip 最后核对
`AGENTS.md` 机制请以 [Codex AGENTS.md 官方文档](https://developers.openai.com/codex/guides/agents-md) 和 [openai/codex GitHub repository](https://github.com/openai/codex) 为准。最后核对日期：2026-05-27。
:::

## 为什么需要 AGENTS.md

没有项目规则时，Codex 需要从仓库里推断很多事情：

- 用哪个包管理器。
- 如何运行测试。
- 哪些目录是生成物。
- 哪些文件不能改。
- 提交前要跑哪些检查。

`AGENTS.md` 能把这些规则显式写下来，减少反复解释。

## 建议放在仓库哪里

针对于我们打开的项目，我们可以在项目根目录下创建一个 agents.md 的文件。

它是 Codex 的记忆文件，Codex 在开始工作之前会先读取 agents.md 的内容。我们可以测试一下：
1. 在 agents.md 文件里面写入一些内容。

![image-20260513125413867](../images/image-20260513125413867.png)

1. 回到 Codex 对话窗口问它：“这是一个什么样的系统？”

![image-20260513125430444](../images/image-20260513125430444.png)

从这里可以看出，Codex 会读取 agents.md 文件，把里面的内容自动带入到新的对话，作为它们的上下文。

当然，在当前目录根目录下创建 agents.md 只对当前文件夹生效，并不是全局生效的。

如果想要全局生效，有以下两种方式：
1. 在系统的全局 Codex 文件夹里面找到 agents.md。
2. 在 Codex 桌面 App 里面打开设置，找到“个性化”，在其中填写“自定义指令”。这里面设置的就是全局的 agents.md 文件。

设置全局文件后，对于所有的项目都会生效。所以它们的作用域和作用范围是不一样的，这一点大家需要了解一下。

![image-20260513125644728](../images/image-20260513125644728.png)

## 团队共享规则和本地私有规则

多人协作时，`AGENTS.md` 适合保存团队共同认可的项目规则；个人路径、本机工具习惯、临时约束和私有工作流偏好，则更适合留在本地。这样团队规则保持稳定，个人习惯也不会被提交到仓库。

### 使用场景

下面这些内容适合放在本地私有规则里：

- 本机缓存、SDK、脚本或临时目录路径。
- 个人常用命令、别名、编辑器习惯。
- 只对自己有效的语言风格、回复格式、验证偏好。
- 不方便进入团队文档的临时限制，例如“今天先只做只读分析”。

### 文件分工

| 文件 | 作用 | 是否提交到 Git |
| --- | --- | --- |
| `AGENTS.md` | 团队共享的项目规则、命令、边界和交付要求 | 可以提交 |
| `AGENTS.local.md` | 个人本地偏好、私有路径和临时规则 | 应加入 ignore |
| `AGENTS.override.md` | 本地工具生成的合并结果 | 应加入 ignore |

### 推荐安装方式

社区工具 [codex-agents-local](https://github.com/samzong/codex-agents-local) 提供了 `AGENTS.local.md` 的本地覆盖方案。它通过 Codex hooks 在会话开始或提交提示词时同步本地规则，默认会把工具安装到 `~/.local/bin`，并更新 `~/.codex/hooks.json`。

安装前建议先让 Codex 审查安装提示词，再决定是否执行：

```text
Read https://github.com/samzong/codex-agents-local/blob/main/INSTALL_PROMPT.md

Follow that prompt in Codex to install codex-agents-local.
```

::: warning 社区工具提示
`codex-agents-local` 不是 Codex 官方功能。安装前请检查脚本会改哪些文件、会启用哪些 hooks、是否符合你的团队安全要求。
:::

### 安全边界

使用本地私有规则时，建议遵守这些边界：

- 不把 token、密钥、账号密码写进 `AGENTS.local.md`。
- 把 `AGENTS.local.md` 和 `AGENTS.override.md` 加入全局 gitignore 或项目 `.gitignore`。
- 不在本地规则里绕过团队的测试、审批和安全要求。
- 每次引入 hooks 工具前，先确认它是否会替换命令、执行仓库文件、访问网络或写入敏感目录。

### 验证命令

安装或修改本地规则后，可以用这些命令检查状态：

```bash
codex-agents-local doctor
codex-agents-local sync --cwd . --check
codex-agents-local sync --cwd . --json
```

如果还没有安装社区工具，可以先检查 ignore 状态：

```bash
git check-ignore -v AGENTS.local.md AGENTS.override.md
```

### 适合和谨慎使用的情况

适合使用：

- 团队已经有稳定的 `AGENTS.md`，个人还需要补充本机规则。
- 多个项目都需要同一套个人偏好，但这些偏好不适合进入仓库。
- 本地规则经常变化，希望减少对团队规则文件的干扰。

谨慎使用：

- 团队对 hooks、自动化脚本或本地生成文件有严格限制。
- 项目处理生产数据、客户数据、财务或医疗等高敏感信息。
- 你还没有确认工具安装脚本和生成文件的具体行为。

## 推荐模板

```markdown
# AGENTS.md

## 项目概览

- 项目类型：
- 主要语言：
- 关键目录：

## 常用命令

- 安装依赖：`...`
- 本地开发：`...`
- 运行测试：`...`
- 类型检查：`...`
- 格式化：`...`

## 代码规范

- 遵循现有代码风格。
- 不做无关重构。
- 新增功能必须补充或更新测试。

## 安全边界

- 不读取或提交 `.env`、密钥和私有凭据。
- 不执行删除生产数据的命令。
- 修改数据库迁移前先说明影响。

## 交付要求

- 说明改动文件。
- 说明验证命令和结果。
- 说明未验证项和剩余风险。
```

## 写作建议

- 越具体越好。`运行测试：pnpm test` 比“记得测试”有用。
- 把生成目录、构建产物、锁文件策略写清楚。
- 如果是 monorepo，请说明每个包的边界。
- 如果有特殊 lint、格式化或代码生成流程，写在命令区。
- 对安全敏感项目，单独写“禁止事项”。

## 最小可用版本

```markdown
# AGENTS.md

## 项目命令

- 安装依赖：`pnpm install`
- 本地开发：`pnpm dev`
- 构建：`pnpm build`

## 改动规则

- 修改前先阅读相关文件。
- 保持现有代码风格。
- 不提交构建产物和环境变量文件。

## 验证要求

- 文档改动运行：`pnpm build`
- 代码改动运行相关测试。

## 安全边界

- 不读取 `.env` 或任何私有凭据。
- 不执行发布、部署、数据库迁移和删除数据命令。
```
