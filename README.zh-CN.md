# Kalaser

一个开源的终端原生 AI 编程助手，基于 TypeScript/Node.js 从零构建。

## 快速开始

### 一键安装

```bash
# 克隆项目
git clone https://github.com/anthropics/kalaser.git
cd kalaser

# 安装依赖
npm install

# 构建
npm run build

# 全局链接（可选，之后可以直接使用 kalaser 命令）
npm link
```

### 配置 API

Kalaser 支持多种模型提供者。创建配置文件 `~/.kalaser/settings.json`：

```json
{
  "models": {
    "my-api": {
      "protocol": "openai-chat",
      "model": "your-model-name",
      "baseURL": "https://your-api.com/v1",
      "apiKey": "your-api-key"
    }
  },
  "defaultModel": "my-api"
}
```

支持的协议：
- `anthropic` — Anthropic Claude API
- `openai-chat` — OpenAI Chat Completions API
- `openai-responses` — OpenAI Responses API
- `gemini` — Google Gemini API

### 运行

```bash
# 交互式模式
kalaser

# 无头模式
echo "hello" | kalaser --print

# 指定模型
kalaser --model my-api
```

## 功能特性

- **多轮对话** — 完整的上下文管理和会话持久化
- **工具调用** — 文件读写、代码编辑、Shell 命令、Web 搜索
- **权限控制** — 三级模式（default/plan/auto），安全沙箱
- **子代理** — 并行任务执行，Agent Teams 协作
- **MCP 协议** — 支持 Model Context Protocol 扩展
- **技能系统** — 可扩展的技能定义和条件激活
- **上下文压缩** — 智能 token 管理，自动/手动压缩
- **多模态** — 支持图片输入和理解
- **Extended Thinking** — 可配置的推理深度

## 命令行参数

```bash
kalaser --help

Options:
  -v, --version               查看版本
  -h, --help                  查看帮助
  --model <handle>            选择模型
  -p, --print [prompt]        无头模式（单次查询）
  --output-format <fmt>       输出格式：text | json | stream-json
  --resume [session-id]       恢复会话
  --plan                      计划模式（只读工具）
  --auto                      自动模式（AI 分类器决策）
  --permission-mode <mode>    权限模式
```

## REPL 命令

在交互式模式下可用的命令：

| 命令 | 说明 |
|------|------|
| `/help` | 显示帮助 |
| `/clear` | 清空对话历史 |
| `/config` | 查看/修改配置 |
| `/mode` | 切换权限模式 |
| `/model` | 切换模型 |
| `/compact` | 压缩上下文 |
| `/skills` | 列出技能 |
| `/agents` | 列出代理 |
| `/history` | 查看历史 |
| `/exit` | 退出 |

## 项目结构

```
kalaser/
├── src/
│   ├── entrypoint/      # CLI 入口
│   ├── ui/              # React/Ink 终端界面
│   ├── core/            # 代理循环和查询引擎
│   ├── agents/          # 子代理定义和运行器
│   ├── tools/           # 本地工具和工具注册表
│   ├── services/        # API、MCP、技能服务
│   ├── permissions/     # 权限和安全控制
│   ├── context/         # 系统提示和上下文管理
│   ├── sandbox/         # Bash 沙箱
│   ├── session/         # 会话持久化
│   ├── state/           # UI/运行时状态
│   ├── types/           # 共享类型
│   └── utils/           # 工具函数
├── package.json
├── tsconfig.json
└── README.md
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `KALASER_DEBUG` | 启用调试日志 |
| `KALASER_DEBUG_STREAM` | 启用流式调试 |
| `KALASER_TEAMS` | 启用 Agent Teams |
| `KALASER_DISABLE_HOOKS` | 禁用所有 hooks |
| `KALASER_MAX_RETRIES` | 设置最大重试次数 |
| `KALASER_DISABLE_CHECKPOINTING` | 禁用文件历史 |

## 配置文件位置

```
~/.kalaser/settings.json          # 用户级配置
<项目>/.kalaser/settings.json     # 项目级配置
<项目>/.kalaser/settings.local.json  # 项目本地配置
```

## 开发

```bash
# 开发模式（热重载）
npm run dev

# 构建
npm run build

# 运行测试
npm run test:stage30
```

## 许可证

MIT License

## 致谢

基于 [Easy Agent](https://github.com/anthropics/easy-agent) 项目重构。
