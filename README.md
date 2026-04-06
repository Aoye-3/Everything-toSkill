# EverythingSkill

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/Aoye-3/Everything-toSkill)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange)](https://github.com/Aoye-3/Everything-toSkill/releases)

**Transform GitHub projects and local folders into AI-accessible Skills**

## 项目概述

EverythingSkill是一个创新的工具，能够将GitHub项目或本地文档文件夹转换为AI可用的Skills。它基于对OpenAI SKILL创建指南和实际项目（如colleague-skill）的深入分析，实现了智能的项目分析和Skill生成功能。

**GitHub仓库**: [https://github.com/Aoye-3/Everything-toSkill](https://github.com/Aoye-3/Everything-toSkill)

## 设计理念

### 核心理念：增强而非替代（Augment, Not Replace）

EverythingSkill的设计基于一个核心信念：AI应该增强人类的能力，而不是替代人类。我们创建的Skills不是为了取代开发者、文档作者或知识工作者，而是为了：

1. **增强工作效率**：将重复性、模式化的任务交给AI，让人专注于创造性工作
2. **扩展个人能力**：将个人知识和经验转化为可复用的AI能力
3. **保存团队智慧**：防止知识流失，确保团队连续性
4. **加速学习过程**：为新成员提供即时可用的知识和指导

### 自主转换：自己掌控自己的知识

"与其被人做成Skill，不如自己来转换一些可以帮助自己的内容被自己使用" - 这一理念体现在：

1. **自主性**：开发者可以自主决定将哪些项目转化为Skills
2. **控制权**：完全控制转换过程、内容和质量
3. **个性化**：根据个人或团队需求定制Skills
4. **迭代优化**：持续改进和优化自己的Skills库

### OpenAI指南的实践应用

遵循OpenAI SKILL创建指南不仅是为了技术合规性，更是为了：

1. **高效协作**：确保Skills能够被AI代理高效理解和使用
2. **资源优化**：合理使用上下文窗口这一宝贵资源
3. **质量保证**：遵循行业最佳实践，创建高质量的Skills
4. **可维护性**：创建易于维护和更新的Skills结构

## 核心功能

### 1. 智能项目分析

- **GitHub项目分析**: 自动提取仓库元数据、README内容、文件结构和关键功能
- **本地文件夹分析**: 扫描目录结构、文件类型和文档内容
- **项目类型检测**: 自动识别项目类型（工具、资源、应用、框架、同事技能等）
- **关键功能提取**: 从文档中识别和提取核心功能

### 2. 智能Skill生成

- **模板化生成**: 根据项目类型使用适当的模板
- **OpenAI兼容**: 遵循OpenAI SKILL创建指南的最佳实践
- **渐进式披露**: 实现三层加载系统（元数据 → SKILL.md正文 → 捆绑资源）
- **上下文优化**: 保持SKILL.md简洁，将详细信息移到references/目录

### 3. 多项目类型支持

- **工具项目**: 命令行工具、库、SDK
- **资源项目**: 文档集合、代码示例、设计资源
- **应用项目**: Web应用、桌面应用、服务
- **框架项目**: 开发框架、样板代码
- **同事技能项目**: 将同事知识转化为AI技能
- **OpenAI兼容项目**: 遵循OpenAI指南的高质量Skills

## 技术架构

### 目录结构

```
everything-skill/
├── SKILL.md                    # 主Skill文档
├── scripts/                    # 核心脚本
│   ├── everything-skill.py     # 主执行脚本
│   ├── analyze-github.py       # GitHub项目分析
│   ├── analyze-folder.py       # 本地文件夹分析
│   ├── generate-skill.py       # 标准Skill生成
│   ├── generate-skill-v2.py    # 改进版Skill生成（OpenAI兼容）
│   └── templates/              # 模板目录
│       ├── tool-template.md
│       ├── resource-template.md
│       ├── openai-compliant-template.md
│       └── colleague-skill-template.md
├── config/                     # 配置文件
│   └── skill-config.json
├── examples/                   # 使用示例
│   └── example-usage.md
└── README.md                   # 项目总结文档
```

### 核心脚本说明

1. **everything-skill.py**: 主执行脚本，支持GitHub和本地文件夹转换
2. **analyze-github.py**: GitHub项目分析器，提取项目信息和结构
3. **analyze-folder.py**: 本地文件夹分析器，扫描和分析文件夹内容
4. **generate-skill.py**: 标准Skill生成器，创建基本Skill结构
5. **generate-skill-v2.py**: 改进版Skill生成器，支持OpenAI兼容和同事技能

## 从OpenAI指南学到的关键原则

### 1. 简洁是关键

- 上下文窗口是共享资源
- 只添加AI不知道的信息
- 挑战每个信息："AI真的需要这个解释吗？"
- 偏好简洁的示例而非冗长的解释

### 2. 适当的自由度

- **高自由度**: 基于文本的指令，适用于灵活任务
- **中自由度**: 伪代码或带参数的脚本
- **低自由度**: 特定脚本，参数少，适用于脆弱操作

### 3. 渐进式披露

- **层级1**: 元数据（名称+描述）- 始终在上下文中
- **层级2**: SKILL.md正文 - 技能触发时加载
- **层级3**: 捆绑资源 - AI需要时加载

### 4. 技能结构

- **必需**: SKILL.md（包含YAML frontmatter）
- **推荐**: agents/openai.yaml（UI元数据）
- **可选**: scripts/, references/, assets/
- **避免**: README.md等额外文档文件

## 从colleague-skill项目学到的洞察

### 1. 创新的技能概念

- 将同事的知识和经验转化为AI技能
- 解决知识传承和团队连续性问题

### 2. 结构化数据设计

- **meta.json**: 同事元数据（角色、专长等）
- **persona.md**: 人物设定和沟通风格
- **work.md**: 工作文档和知识
- **examples/**: 工作示例

### 3. 多语言支持

- 多种语言的README文件
- 国际化考虑
- 跨文化适应性

### 4. 实际应用场景

- 知识保存和传承
- 工作连续性保障
- 培训加速
- 质量保证

## 使用示例

### 示例1: 转换GitHub项目

```bash
# 转换GitHub项目
python scripts/everything-skill.py https://github.com/example/project --output ./skills

# 使用改进版生成器
python scripts/generate-skill-v2.py project-analysis.json --output ./skills --template openai-compliant
```

### 示例2: 转换本地文件夹

```bash
# 转换本地文件夹
python scripts/everything-skill.py ./my-docs --output ./skills --type folder

# 分析文件夹
python scripts/analyze-folder.py ./my-docs --output analysis.json
```

### 示例3: 创建同事技能

```bash
# 分析colleague-skill项目
python scripts/analyze-github.py https://github.com/titanwings/colleague-skill --output analysis.json

# 生成同事技能
python scripts/generate-skill-v2.py analysis.json --output ./skills --template colleague-skill
```

## 生成的Skill结构

### 标准Skill结构

```
generated-skill/
├── SKILL.md                    # 主文档
├── scripts/                    # 执行脚本
├── config/                     # 配置文件
├── assets/                     # 资源文件
└── examples/                   # 使用示例
```

### OpenAI兼容Skill结构

```
openai-skill/
├── SKILL.md                    # 简洁主文档
├── agents/                     # AI代理元数据
│   └── openai.yaml            # UI元数据
├── scripts/                    # 可执行代码
├── references/                 # 参考文档（渐进式披露）
└── assets/                     # 输出资源
```

### 同事技能结构

```
colleague-skill/
├── SKILL.md                    # 同事技能文档
├── agents/                     # AI代理元数据
├── colleagues/                 # 同事数据
│   ├── {name}/                # 单个同事
│   │   ├── meta.json          # 元数据
│   │   ├── persona.md         # 人物设定
│   │   └── work.md            # 工作文档
│   └── index.json             # 同事索引
├── scripts/                    # 处理脚本
├── references/                 # 参考文档
└── assets/                     # 模板和资源
```

## 最佳实践实现

### 1. 内容提取策略

- 从README提取核心功能，而非所有功能
- 识别主要使用场景和命令
- 提取实际可运行的示例
- 确定适当的自由度级别

### 2. 模板填充指南

- **名称**: 使用项目名称，小写，连字符分隔
- **描述**: 项目功能 + 明确的触发条件
- **示例**: 实际可运行的命令，非伪代码
- **功能**: 核心功能列表，限制数量

### 3. 结构优化

- 创建标准目录结构
- 将详细内容放入引用文件
- 将可执行代码放入脚本
- 将模板文件放入资源

### 4. 质量保证

- 验证SKILL.md格式和内容
- 检查文件大小和结构
- 测试生成脚本的可运行性
- 验证渐进式披露模式

## 技术挑战与解决方案

### 挑战1: 项目类型识别

**问题**: 如何准确识别项目类型
**解决方案**: 多因素分析（文件结构、README内容、技术栈线索）

### 挑战2: 内容提取准确性

**问题**: 如何从复杂文档中提取关键信息
**解决方案**: 模式匹配 + 启发式规则 + 关键词提取

### 挑战3: OpenAI兼容性

**问题**: 如何确保生成的Skill符合OpenAI指南
**解决方案**: 专用模板 + 验证规则 + 渐进式披露实现

### 挑战4: 同事技能建模

**问题**: 如何将人的知识转化为结构化数据
**解决方案**: 标准化数据结构（meta.json, persona.md, work.md）

## 性能优化

### 1. 分析优化

- 限制递归深度
- 排除无关文件类型
- 缓存分析结果
- 并行处理

### 2. 生成优化

- 模板预编译
- 批量处理
- 增量生成
- 压缩输出

### 3. 存储优化

- 智能文件组织
- 避免重复内容
- 使用引用而非复制
- 压缩资源文件

## 扩展性设计

### 1. 插件系统

- 可扩展的分析器
- 自定义模板支持
- 第三方集成插件
- 输出格式插件

### 2. API接口

- RESTful API服务
- 批量处理接口
- 实时分析接口
- 技能验证接口

### 3. 集成能力

- CI/CD管道集成
- 版本控制系统集成
- 项目管理工具集成
- 知识库系统集成

## 伦理和安全考虑

### 1. 隐私保护

- 数据匿名化处理
- 访问权限控制
- 数据保留政策
- 加密存储

### 2. 透明性

- 明确AI生成内容标识
- 技能能力说明
- 知识来源标注
- 使用限制说明

### 3. 责任归属

- 内容责任明确
- 错误报告机制
- 影响评估流程
- 持续监督机制

## 未来发展方向

### 短期目标

1. 更多项目类型支持
2. 更好的模板系统
3. 交互式转换模式
4. 批量处理功能

### 中期目标

1. 技能验证和测试
2. 社区模板共享
3. 分析插件系统
4. 集成插件开发

### 长期目标

1. 实时学习能力
2. 多技能协作
3. 情感模拟功能
4. 跨平台支持

## 总结

EverythingSkill成功实现了将GitHub项目和本地文件夹转换为AI可用Skills的核心功能，并基于OpenAI指南和实际项目洞察进行了深度优化。主要成就包括：

### 技术成就

1. **智能分析系统**: 能够准确分析项目结构和内容
2. **模板化生成**: 支持多种项目类型的智能生成
3. **OpenAI兼容**: 遵循行业最佳实践和指南
4. **渐进式披露**: 实现高效的内容加载策略

### 创新亮点

1. **同事技能支持**: 创新的知识传承解决方案
2. **多语言考虑**: 国际化设计思维
3. **实际场景聚焦**: 解决真实工作问题
4. **伦理框架**: 全面的伦理和安全考虑

### 实用价值

1. **知识保存**: 防止知识流失
2. **效率提升**: 加速技能创建过程
3. **质量保证**: 生成高质量、可用的Skills
4. **标准化**: 推动Skill创建标准化

EverythingSkill为AI技能创建提供了一个强大、灵活、智能的工具，有助于推动AI代理能力的扩展和应用场景的丰富化。

## 开源协议与引用声明

### 开源协议
EverythingSkill 采用 **MIT 许可证** 发布。这是一个宽松的开源协议，允许：

1. **商业使用**: 可以用于商业项目
2. **修改和分发**: 可以修改代码并分发
3. **私人使用**: 可以用于私人项目
4. **专利使用**: 许可证包含明确的专利授权

**限制条件**：
- 必须保留原始版权声明
- 必须包含许可证文本
- 不提供任何担保

完整许可证文本请查看 [LICENSE](../LICENSE) 文件。

### 引用声明
使用或参考EverythingSkill时，请适当引用：

**学术引用**：
```
EverythingSkill: Transform GitHub projects and local folders into AI-accessible Skills.
Version 1.0. Available at: https://github.com/example/everything-skill
```

**代码引用**：
```python
# Based on EverythingSkill (https://github.com/example/everything-skill)
# MIT License - Copyright (c) 2026 EverythingSkill Contributors
```

### 第三方引用
EverythingSkill 参考和借鉴了以下项目：

1. **OpenAI SKILL 创建指南**: 遵循OpenAI的Skill创建最佳实践
2. **colleague-skill 项目**: 灵感来源于将同事知识转化为AI技能的概念
3. **GitHub API**: 用于分析GitHub项目结构和内容
4. **OpenAI 模型**: 遵循AI代理交互的最佳实践

### 免责声明
1. **非官方工具**: EverythingSkill 不是OpenAI官方工具
2. **无担保**: 软件按"原样"提供，不提供任何明示或暗示的担保
3. **责任限制**: 在任何情况下，作者或版权持有人均不对因使用本软件而产生的任何索赔、损害或其他责任负责
4. **合规性**: 用户需确保使用符合相关法律法规和平台政策

### 贡献者协议
贡献代码即表示您同意：
1. 您的贡献将根据MIT许可证授权
2. 您拥有提交代码的必要权利
3. 您同意遵守项目行为准则

### 知识产权
1. **代码版权**: 代码版权归贡献者所有
2. **内容责任**: 用户对转换的内容负责
3. **引用要求**: 使用第三方内容需遵守原始许可证
4. **归属要求**: 适当引用和归属原始项目

### GitHub贡献指南
欢迎通过GitHub贡献代码！请遵循以下步骤：

1. **Fork仓库**: 点击GitHub页面右上角的"Fork"按钮
2. **克隆仓库**: `git clone https://github.com/YOUR-USERNAME/Everything-toSkill.git`
3. **创建分支**: `git checkout -b feature/your-feature-name`
4. **提交更改**: `git commit -m "Add your feature description"`
5. **推送到GitHub**: `git push origin feature/your-feature-name`
6. **创建Pull Request**: 在GitHub仓库页面创建PR

### 问题报告和功能请求
- **问题报告**: 在GitHub Issues中报告问题
- **功能请求**: 提交功能请求或改进建议
- **文档贡献**: 帮助改进文档和示例

### 快速链接
- **GitHub仓库**: [https://github.com/Aoye-3/Everything-toSkill](https://github.com/Aoye-3/Everything-toSkill)
- **问题跟踪**: [GitHub Issues](https://github.com/Aoye-3/Everything-toSkill/issues)
- **讨论区**: [GitHub Discussions](https://github.com/Aoye-3/Everything-toSkill/discussions)

---

*EverythingSkill - 让每个项目都能成为AI的技能*

**增强而非替代，自主掌控知识**

**GitHub**: [Aoye-3/Everything-toSkill](https://github.com/Aoye-3/Everything-toSkill)  
**许可证**: MIT  
**版权**: © 2026 EverythingSkill Contributors  
**版本**: 1.0.0  
**最后更新**: 2026-04-06
