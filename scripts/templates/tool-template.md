# 工具类项目Skill模板

## 模板说明
此模板适用于工具类GitHub项目，如命令行工具、库、SDK等。

## 核心结构

### 1. SKILL.md 结构
```markdown
---
name: "{skill_name}"
description: "{description} Use when user needs to {use_case}."
---

# {project_name}

{project_description}

## 快速开始

### 安装
```bash
{installation_command}
```

### 基本使用
```bash
{basic_usage}
```

## 功能特性

{features_list}

## 命令行参考

### 主要命令
```bash
{main_command} --help
```

### 常用选项
- `--help`: 显示帮助信息
- `--version`: 显示版本信息
- `--verbose`: 详细输出模式
- `--config`: 指定配置文件

## 配置说明

### 配置文件位置
- `~/.{tool_name}/config.json`
- `./.{tool_name}.json`
- 环境变量

### 配置示例
```json
{config_example}
```

## 示例

### 示例1: 基本功能
```bash
{example_1}
```

### 示例2: 高级功能
```bash
{example_2}
```

## 故障排除

### 常见问题
1. **安装失败**: 检查系统依赖
2. **权限错误**: 确保有执行权限
3. **配置错误**: 验证配置文件格式

### 获取帮助
1. 运行 `{main_command} --help`
2. 查看项目文档
3. 提交GitHub Issue
```

### 2. 脚本目录结构
```
scripts/
├── run-tool.py              # 主执行脚本
├── setup.py                 # 安装脚本
├── test-tool.py             # 测试脚本
└── utils/                   # 工具函数
    ├── config.py
    ├── logger.py
    └── validator.py
```

### 3. 配置目录结构
```
config/
├── default-config.json      # 默认配置
├── production-config.json   # 生产环境配置
└── development-config.json  # 开发环境配置
```

### 4. 示例目录结构
```
examples/
├── basic-usage.md           # 基本使用示例
├── advanced-features.md     # 高级功能示例
└── integration/             # 集成示例
    ├── with-python.md
    ├── with-nodejs.md
    └── with-docker.md
```

## 填充指南

### 1. 元数据填充
- `{skill_name}`: 使用小写字母和连字符，如 `markdown-formatter`
- `{description}`: 简洁描述工具功能
- `{use_case}`: 具体使用场景，如 "format markdown documents" 或 "analyze code quality"

### 2. 命令填充
- `{installation_command}`: 安装命令，如 `pip install tool-name` 或 `npm install tool-name`
- `{basic_usage}`: 基本使用命令，如 `tool-name --help` 或 `tool-name process input.txt`
- `{main_command}`: 主命令名称

### 3. 内容填充
- `{project_name}`: 项目名称
- `{project_description}`: 项目描述
- `{features_list}`: 功能列表（使用Markdown列表格式）
- `{config_example}`: 配置示例（JSON格式）
- `{example_1}`, `{example_2}`: 具体使用示例

## 最佳实践

### 1. 触发条件设计
- 明确描述何时使用此Skill
- 包含具体的关键词和场景
- 避免过于宽泛的描述

### 2. 接口设计
- 提供清晰的命令行接口
- 支持标准输入输出
- 包含详细的帮助信息

### 3. 错误处理
- 提供有意义的错误信息
- 包含故障排除指南
- 支持调试模式

### 4. 文档质量
- 包含实际可运行的示例
- 提供配置说明
- 列出常见问题和解决方案

## 自动填充规则

### 从GitHub项目提取
1. **名称**: 从仓库名提取
2. **描述**: 从仓库描述或README第一段提取
3. **安装命令**: 根据项目类型推断（npm, pip, cargo等）
4. **使用示例**: 从README的Usage部分提取
5. **功能列表**: 从README的Features部分提取

### 智能推断
1. **项目类型**: 根据文件结构和技术栈推断
2. **主要命令**: 根据常见模式推断（如cli, tool, cmd等）
3. **配置格式**: 根据技术栈推断（JSON, YAML, TOML等）
4. **依赖关系**: 从package.json, requirements.txt等文件提取

## 验证标准

### 必须包含
- [ ] 清晰的触发条件描述
- [ ] 完整的安装说明
- [ ] 实际可运行的示例
- [ ] 故障排除指南

### 推荐包含
- [ ] 配置模板
- [ ] 测试脚本
- [ ] 集成示例
- [ ] 性能优化建议

### 可选包含
- [ ] 高级功能文档
- [ ] API参考
- [ ] 插件系统说明
- [ ] 贡献指南

## 示例填充

### 输入项目
- 名称: `markdown-formatter`
- 描述: `A tool for formatting and beautifying Markdown documents`
- 语言: `Python`
- README: 包含Usage和Examples部分

### 生成Skill
- Skill名称: `markdown-formatter`
- 触发条件: `Use when user needs to format and beautify Markdown documents`
- 安装命令: `pip install markdown-formatter`
- 使用示例: `markdown-formatter input.md --output formatted.md`
- 功能列表: 从README提取的功能点

## 注意事项

1. **保持简洁**: Skill文档应简洁明了，避免冗余
2. **关注核心**: 突出核心功能，次要功能可放在参考文件中
3. **测试验证**: 确保所有示例都能实际运行
4. **持续更新**: Skill应与原项目保持同步更新