# OpenAI兼容Skill模板

## 模板说明
此模板遵循OpenAI SKILL创建指南的最佳实践，适用于创建高质量、高效的Skills。

## 核心原则

### 1. 简洁是关键
- 上下文窗口是共享资源
- 只添加AI不知道的信息
- 挑战每个信息："AI真的需要这个解释吗？"
- 偏好简洁的示例而非冗长的解释

### 2. 适当的自由度
- **高自由度（基于文本的指令）**：当多种方法有效、决策取决于上下文或启发式指导方法时使用
- **中自由度（伪代码或带参数的脚本）**：当存在首选模式、允许一些变化或配置影响行为时使用
- **低自由度（特定脚本，参数少）**：当操作脆弱易错、一致性关键或必须遵循特定序列时使用

## 技能结构

### 标准目录结构
```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter元数据 (必需)
│   │   ├── name: (必需)
│   │   └── description: (必需)
│   └── Markdown指令 (必需)
├── agents/ (推荐)
│   └── openai.yaml - UI元数据
└── 捆绑资源 (可选)
    ├── scripts/          - 可执行代码
    ├── references/       - 按需加载的文档
    └── assets/           - 输出中使用的文件
```

## SKILL.md模板

```markdown
---
name: "{skill_name}"
description: "{clear_description} Use when {trigger_conditions}."
---

# {skill_title}

{brief_overview}

## 快速开始

### 基本使用
```bash
{basic_command}
```

### 最小示例
```bash
{minimal_example}
```

## 核心功能

### 主要用途
{primary_use_cases}

### 输入输出
- **输入**: {input_description}
- **输出**: {output_description}
- **错误**: {error_handling}

## 详细指南

### 配置
{configuration_guide}

### 高级功能
{advanced_features}

## 示例

### 示例1: {example_1_title}
```bash
{example_1_code}
```

### 示例2: {example_2_title}
```bash
{example_2_code}
```

## 故障排除

### 常见问题
{troubleshooting}

### 获取帮助
{help_resources}

---

*遵循OpenAI SKILL创建指南 - 保持简洁，关注核心功能*
```

## 渐进式披露模式

### 模式1: 高级指南与引用
```markdown
# PDF处理

## 快速开始

使用pdfplumber提取文本：
[代码示例]

## 高级功能

- **表单填写**: 参见[FORMS.md](FORMS.md)获取完整指南
- **API参考**: 参见[REFERENCE.md](REFERENCE.md)获取所有方法
- **示例**: 参见[EXAMPLES.md](EXAMPLES.md)获取常见模式
```

### 模式2: 领域特定组织
```
bigquery-skill/
├── SKILL.md (概述和导航)
└── reference/
    ├── finance.md (收入、账单指标)
    ├── sales.md (机会、管道)
    ├── product.md (API使用、功能)
    └── marketing.md (活动、归因)
```

### 模式3: 条件细节
```markdown
# DOCX处理

## 创建文档

使用docx-js创建新文档。参见[DOCX-JS.md](DOCX-JS.md)。
```

## 元数据最佳实践

### Frontmatter要求
```yaml
---
name: "skill-name"  # 必需：小写，连字符分隔
description: "清晰描述技能功能和触发条件"  # 必需：明确说明何时使用
---
```

### 描述编写指南
1. **明确功能**: 技能能做什么
2. **触发条件**: 何时应该使用此技能
3. **使用场景**: 具体的使用场景
4. **避免模糊**: 不要使用"帮助"、"协助"等模糊词汇

**好示例**: "Format and beautify Markdown documents with consistent styling. Use when user needs to clean up Markdown files, enforce formatting rules, or prepare documentation for publication."

**差示例**: "Help with Markdown formatting."

## 脚本目录最佳实践

### 何时包含脚本
- 相同代码被重复重写时
- 需要确定性可靠性时
- 操作脆弱易错时

### 脚本结构
```python
#!/usr/bin/env python3
"""
脚本目的 - 简洁描述
"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='脚本描述')
    parser.add_argument('input', help='输入文件或目录')
    parser.add_argument('--output', '-o', help='输出文件')
    
    args = parser.parse_args()
    
    try:
        # 主逻辑
        result = process(args.input, args.output)
        print(f"成功: {result}")
        return 0
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

## 引用目录最佳实践

### 何时包含引用
- AI在工作时应参考的文档
- 详细参考材料
- 领域特定知识

### 引用文件结构
```
references/
├── api_docs.md      # API规范
├── schemas.md       # 数据模式
├── workflows.md     # 工作流程指南
└── examples.md      # 详细示例
```

## 资源目录最佳实践

### 何时包含资源
- 技能输出中使用的文件
- 模板、图像、图标
- 样板代码、字体

### 资源文件结构
```
assets/
├── templates/       # 模板文件
├── images/          # 图像资源
└── fonts/           # 字体文件
```

## 验证标准

### 必须检查
- [ ] SKILL.md文件存在且格式正确
- [ ] Frontmatter包含name和description
- [ ] 描述清晰说明功能和触发条件
- [ ] 文件大小合理（SKILL.md < 500行）
- [ ] 没有冗余信息

### 推荐检查
- [ ] 包含实际可运行的示例
- [ ] 使用渐进式披露模式
- [ ] 脚本有错误处理
- [ ] 引用文件组织良好

### 避免事项
- [ ] 不要创建额外的文档文件（README.md等）
- [ ] 不要包含辅助上下文
- [ ] 不要重复AI已经知道的信息
- [ ] 不要使上下文膨胀

## 从项目生成Skill的指南

### 1. 分析阶段
- 提取核心功能，而非所有功能
- 识别主要使用场景
- 确定适当的自由度级别

### 2. 内容提取
- 从README提取关键信息
- 识别主要命令和API
- 提取实际示例

### 3. 模板填充
- **名称**: 使用项目名称，小写，连字符分隔
- **描述**: 项目功能 + 触发条件
- **示例**: 实际可运行的命令
- **功能**: 核心功能，非所有功能

### 4. 结构创建
- 创建标准目录结构
- 将详细内容放入引用文件
- 将可执行代码放入脚本
- 将模板文件放入资源

## 示例：转换一个工具项目

### 原始项目
- 名称: `markdown-formatter`
- 描述: "A tool for formatting Markdown documents"
- 功能: 格式化、美化、验证Markdown

### 生成的Skill
```markdown
---
name: "markdown-formatter"
description: "Format and beautify Markdown documents with consistent styling. Use when user needs to clean up Markdown files, enforce formatting rules, or prepare documentation for publication."
---

# Markdown Formatter

Format Markdown documents with consistent styling rules.

## Quick Start

```bash
markdown-formatter input.md --output formatted.md
```

## Core Features

- Consistent heading levels
- Table formatting
- List normalization
- Link reference cleanup

## Examples

### Format a single file
```bash
markdown-formatter README.md --output README-formatted.md
```

### Format directory recursively
```bash
markdown-formatter docs/ --recursive
```

## Configuration

See [CONFIG.md](references/CONFIG.md) for configuration options.
```

## 性能优化

### 上下文管理
1. **保持SKILL.md精简**: < 500行，< 5k单词
2. **使用引用文件**: 将详细内容移到references/
3. **延迟加载**: 只在需要时加载内容
4. **压缩内容**: 移除冗余和空白

### 文件组织
1. **按功能组织**: 相关文件放在一起
2. **使用清晰命名**: 描述性文件名
3. **避免深层嵌套**: 保持目录结构扁平
4. **分离关注点**: 指令、代码、资源分离

## 质量保证

### 自动化检查
```bash
# 检查SKILL.md格式
python -c "
import yaml, re
with open('SKILL.md', 'r') as f:
    content = f.read()
    
# 检查frontmatter
match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
if match:
    frontmatter = yaml.safe_load(match.group(1))
    assert 'name' in frontmatter, 'Missing name'
    assert 'description' in frontmatter, 'Missing description'
    print('✓ Frontmatter valid')
else:
    print('✗ Missing frontmatter')
"

# 检查文件大小
import os
size = os.path.getsize('SKILL.md')
if size < 100000:  # 100KB
    print('✓ SKILL.md size OK')
else:
    print('✗ SKILL.md too large')
```

### 手动审查
1. **功能完整性**: 技能是否完成其宣称的功能？
2. **触发准确性**: 描述是否准确反映何时使用？
3. **示例可用性**: 示例是否实际可运行？
4. **错误处理**: 是否包含适当的错误处理？

## 更新和维护

### 版本控制
- 使用语义化版本控制
- 维护变更日志
- 向后兼容性考虑

### 定期审查
- 每月审查技能有效性
- 更新过时信息
- 优化性能和大小

## 总结

创建有效的Skill需要：
1. **理解AI的能力**: 只添加AI不知道的信息
2. **关注用户体验**: 清晰、简洁、有用
3. **优化性能**: 管理上下文使用
4. **持续改进**: 定期审查和更新

通过遵循此模板和指南，你可以创建高质量、高效、有用的Skills，为AI代理提供真正的价值。