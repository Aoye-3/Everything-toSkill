#!/usr/bin/env python3
"""
改进版Skill生成脚本
基于OpenAI SKILL指南和colleague-skill项目洞察
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

class ImprovedSkillGenerator:
    """改进版Skill生成器，遵循OpenAI指南"""
    
    def __init__(self, project_info: Dict[str, Any], output_dir: str, template: Optional[str] = None):
        self.project_info = project_info
        self.output_dir = output_dir
        self.template = template
        self.skill_name = self._generate_skill_name()
        self.project_type = self._determine_project_type_with_insights()
        
    def _generate_skill_name(self) -> str:
        """生成符合OpenAI指南的Skill名称"""
        name = self.project_info.get("name", "").lower()
        
        # 移除特殊字符，用连字符替换空格和点
        name = re.sub(r'[^\w\s-]', '', name)
        name = re.sub(r'[-\s.]+', '-', name)
        
        # 确保名称以字母开头，小写，连字符分隔
        if name and not name[0].isalpha():
            name = "skill-" + name
        
        # 限制长度
        if len(name) > 50:
            name = name[:50]
        
        return name or "generated-skill"
    
    def _determine_project_type_with_insights(self) -> str:
        """基于项目洞察确定项目类型"""
        project_type = self.project_info.get("project_type", "unknown")
        description = self.project_info.get("description", "").lower()
        name = self.project_info.get("name", "").lower()
        
        # 检查是否为colleague-skill类型项目
        colleague_keywords = ["colleague", "同事", "knowledge", "knowledge transfer", "digital life", "数字生命"]
        if any(keyword in description.lower() or keyword in name.lower() for keyword in colleague_keywords):
            return "colleague-skill"
        
        # 检查是否应使用OpenAI兼容模板
        if self.template == "openai-compliant":
            return "openai-compliant"
        
        return project_type
    
    def generate(self) -> str:
        """生成完整的Skill结构，遵循OpenAI指南"""
        print(f"生成Skill: {self.skill_name} (类型: {self.project_type})")
        
        # 创建Skill目录
        skill_dir = os.path.join(self.output_dir, self.skill_name)
        os.makedirs(skill_dir, exist_ok=True)
        
        # 根据项目类型选择生成策略
        if self.project_type == "colleague-skill":
            self._generate_colleague_skill(skill_dir)
        elif self.project_type == "openai-compliant":
            self._generate_openai_compliant_skill(skill_dir)
        else:
            self._generate_standard_skill(skill_dir)
        
        print(f"Skill生成完成！目录: {skill_dir}")
        return skill_dir
    
    def _generate_colleague_skill(self, skill_dir: str):
        """生成同事技能类型的Skill"""
        print("使用同事技能模板...")
        
        # 创建目录结构
        dirs = ["agents", "colleagues", "scripts", "references", "assets/templates", "assets/examples"]
        for dir_path in dirs:
            os.makedirs(os.path.join(skill_dir, dir_path), exist_ok=True)
        
        # 生成SKILL.md
        self._generate_colleague_skill_md(skill_dir)
        
        # 生成agents/openai.yaml
        self._generate_openai_yaml(skill_dir)
        
        # 生成示例同事数据
        self._generate_example_colleague_data(skill_dir)
        
        # 生成脚本
        self._generate_colleague_scripts(skill_dir)
        
        # 生成参考文档
        self._generate_colleague_references(skill_dir)
        
        # 生成配置
        self._generate_colleague_config(skill_dir)
    
    def _generate_openai_compliant_skill(self, skill_dir: str):
        """生成OpenAI兼容的Skill"""
        print("使用OpenAI兼容模板...")
        
        # 创建目录结构
        dirs = ["agents", "scripts", "references", "assets"]
        for dir_path in dirs:
            os.makedirs(os.path.join(skill_dir, dir_path), exist_ok=True)
        
        # 生成SKILL.md（遵循OpenAI指南）
        self._generate_openai_compliant_skill_md(skill_dir)
        
        # 生成agents/openai.yaml
        self._generate_openai_yaml(skill_dir)
        
        # 生成脚本（如果有）
        self._generate_openai_scripts(skill_dir)
        
        # 生成参考文档（渐进式披露）
        self._generate_openai_references(skill_dir)
    
    def _generate_standard_skill(self, skill_dir: str):
        """生成标准Skill"""
        print("使用标准模板...")
        
        # 创建目录结构
        dirs = ["scripts", "config", "assets", "examples"]
        for dir_path in dirs:
            os.makedirs(os.path.join(skill_dir, dir_path), exist_ok=True)
        
        # 生成SKILL.md
        self._generate_standard_skill_md(skill_dir)
        
        # 生成配置文件
        self._generate_standard_config(skill_dir)
        
        # 生成脚本
        self._generate_standard_scripts(skill_dir)
        
        # 生成示例
        self._generate_standard_examples(skill_dir)
    
    def _generate_colleague_skill_md(self, skill_dir: str):
        """生成同事技能的SKILL.md"""
        skill_md_path = os.path.join(skill_dir, "SKILL.md")
        
        # 提取项目信息
        name = self.project_info.get("name", "Colleague Skill")
        description = self.project_info.get("description", "Transform colleague knowledge into AI skills")
        
        # 生成OpenAI兼容的描述
        openai_description = self._generate_openai_compliant_description()
        
        content = f"""---
name: "{self.skill_name}"
description: "{openai_description}"
---

# {name}

{description}

## Core Concept

Transform colleague knowledge, experience, and communication style into continuously available AI skills for knowledge preservation and team continuity.

## Quick Start

### Import Colleague Data
```bash
python scripts/import-colleague.py --name "Colleague Name" --source "data-source"
```

### Query Colleague Knowledge
```bash
python scripts/query-colleague.py --colleague "Name" --query "technical question"
```

### Generate Work Response
```bash
python scripts/generate-response.py --colleague "Name" --context "work scenario"
```

## Supported Data Sources

### Automatic Collection
- **Feishu**: Message history, documents, multi-dimensional tables (API auto-collection)
- **DingTalk**: Documents, multi-dimensional tables (browser automation)
- **Slack**: Message history (API, 90-day limit for free version)

### Manual Import
- **PDF Documents**: Work documents, reports
- **Images/Screenshots**: Chat screenshots, document screenshots
- **Chat History**: WeChat, Feishu JSON export
- **Emails**: .eml/.mbox format
- **Markdown**: Document files
- **Direct Text**: Paste text content

## Colleague Data Structure

### meta.json (Metadata)
```json
{{
  "name": "Colleague Name",
  "role": "Job Role",
  "expertise": ["Domain Expertise 1", "Domain Expertise 2"],
  "tenure": "Employment Duration",
  "communication_style": "Communication Style",
  "work_patterns": ["Work Pattern 1", "Work Pattern 2"]
}}
```

### persona.md (Persona)
```
# Persona for {{name}}

## Communication Style
- Tone characteristics
- Common expressions
- Communication preferences

## Work Habits
- Working hours
- Response speed
- Work quality requirements

## Professional Knowledge
- Core skills
- Experience domains
- Problem-solving methods
```

### work.md (Work Documentation)
```
# Work Knowledge for {{name}}

## Responsible Projects
- Project 1: Description, tech stack, status
- Project 2: Description, tech stack, status

## Technical Specifications
- Coding standards
- Testing requirements
- Deployment processes

## Common Issues
- Issue 1: Description, solution
- Issue 2: Description, solution
```

## Use Cases

### Case 1: Knowledge Preservation
**Problem**: Colleague departure leaves大量 undocumented knowledge
**Solution**: Import colleague work data to create持续 available skills
**Effect**: New members can "consult" departed colleague's knowledge

### Case 2: Work Continuity
**Problem**: Key personnel temporarily离开, work受阻
**Solution**: Use colleague skills to continue work
**Effect**: Work不中断, maintain consistency

### Case 3: Training Assistance
**Problem**: New employees need快速上手
**Solution**: Use colleague skills as training resources
**Effect**: Accelerate learning curve, reduce training time

## Examples

### Example 1: Import Feishu Colleague Data
```bash
python scripts/import-colleague.py \\
  --name "Zhang San" \\
  --source "feishu" \\
  --user_id "ou_xxxx" \\
  --time_range "2024-01-01:2024-12-31"
```

### Example 2: Query Technical Questions
```bash
python scripts/query-colleague.py \\
  --colleague "Li Si" \\
  --query "How to design API gateway for microservices architecture" \\
  --context "High-concurrency e-commerce system"
```

## Configuration

See [CONFIGURATION.md](references/CONFIGURATION.md) for detailed configuration options.

## Ethical Considerations

### Privacy Protection
1. **Explicit Consent**: Obtain explicit consent from colleagues for data use
2. **Data Anonymization**: Anonymize sensitive information when necessary
3. **Access Control**: Strictly control data access permissions
4. **Data Retention**: Clear data retention期限 and deletion policies

### Transparency
1. **Clear Identification**: Clearly identify AI-generated content
2. **Capability说明**: Clearly state skill limitations
3. **Source Attribution**: Indicate knowledge sources and update dates
4. **Usage Guidelines**: Provide appropriate usage guidelines and warnings

---

*Generated by EverythingSkill with Colleague-Skill template | Follows OpenAI SKILL guidelines*
"""
        
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_openai_compliant_skill_md(self, skill_dir: str):
        """生成OpenAI兼容的SKILL.md"""
        skill_md_path = os.path.join(skill_dir, "SKILL.md")
        
        # 提取项目信息
        name = self.project_info.get("name", "")
        description = self.project_info.get("description", "")
        
        # 生成OpenAI兼容的描述
        openai_description = self._generate_openai_compliant_description()
        
        # 提取关键功能（限制数量）
        key_features = self.project_info.get("key_features", [])
        if len(key_features) > 5:
            key_features = key_features[:5]
        
        content = f"""---
name: "{self.skill_name}"
description: "{openai_description}"
---

# {name}

{description}

## Quick Start

### Basic Usage
```bash
{self._get_basic_usage_command()}
```

### Minimal Example
```bash
{self._get_minimal_example()}
```

## Core Features

{self._format_features_list(key_features)}

## Detailed Guide

### Configuration
{self._get_configuration_guide()}

### Advanced Features
See [ADVANCED.md](references/ADVANCED.md) for advanced features and options.

## Examples

### Example 1: {self._get_example_1_title()}
```bash
{self._get_example_1_code()}
```

### Example 2: {self._get_example_2_title()}
```bash
{self._get_example_2_code()}
```

## Troubleshooting

### Common Issues
{self._get_common_issues()}

### Getting Help
{self._get_help_resources()}

---

*Follows OpenAI SKILL creation guidelines - Concise, focused on core functionality*
"""
        
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_standard_skill_md(self, skill_dir: str):
        """生成标准SKILL.md"""
        skill_md_path = os.path.join(skill_dir, "SKILL.md")
        
        # 提取项目信息
        name = self.project_info.get("name", "")
        description = self.project_info.get("description", "")
        url = self.project_info.get("url", "")
        
        content = f"""---
name: "{self.skill_name}"
description: "{description} Use when {self._generate_trigger_conditions()}."
---

# {name}

{description}

## Project Information

- **Source**: {url if url else "Local folder"}
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Type**: {self.project_type}

## Quick Start

### Installation
```bash
{self._get_installation_command()}
```

### Basic Usage
```bash
{self._get_basic_usage_command()}
```

## Features

{self._generate_features_section()}

## Examples

### Example 1: Basic Operation
```bash
{self._get_example_1_code()}
```

### Example 2: Advanced Usage
```bash
{self._get_example_2_code()}
```

## Configuration

See [CONFIG.md](config/CONFIG.md) for configuration options.

## Troubleshooting

### Common Issues
{self._get_common_issues()}

---

*Generated by EverythingSkill*
"""
        
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_openai_compliant_description(self) -> str:
        """生成OpenAI兼容的描述"""
        description = self.project_info.get("description", "")
        project_type = self.project_type
        
        # 基础描述
        base_desc = description
        
        # 添加触发条件
        trigger = self._generate_trigger_conditions()
        
        # 组合成OpenAI格式
        if trigger:
            return f"{base_desc} Use when {trigger}."
        else:
            return f"{base_desc} Use when user needs to work with {self.skill_name}."
    
    def _generate_trigger_conditions(self) -> str:
        """生成触发条件"""
        project_type = self.project_type
        key_features = self.project_info.get("key_features", [])
        
        if project_type == "colleague-skill":
            return "user needs to preserve team knowledge, continue work after colleague departure, or access specific expertise"
        elif project_type == "tool":
            if key_features:
                feature_str = ", ".join(key_features[:2])
                return f"user needs to {feature_str.lower()}"
            else:
                return f"user needs to use {self.skill_name} tool"
        elif project_type == "resource":
            return f"user needs access to {self.skill_name} resources"
        else:
            return f"user needs to work with {self.skill_name}"
    
    def _generate_openai_yaml(self, skill_dir: str):
        """生成agents/openai.yaml文件"""
        agents_dir = os.path.join(skill_dir, "agents")
        os.makedirs(agents_dir, exist_ok=True)
        
        yaml_path = os.path.join(agents_dir, "openai.yaml")
        
        name = self.project_info.get("name", self.skill_name)
        description = self._generate_openai_compliant_description()
        
        content = f"""# OpenAI UI metadata for {self.skill_name}

display_name: {name}
short_description: {description[:100]}...
default_prompt: "Use the {self.skill_name} skill to {self._get_skill_purpose()}"
"""
        
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _get_skill_purpose(self) -> str:
        """获取技能目的"""
        if self.project_type == "colleague-skill":
            return "preserve and access colleague knowledge"
        elif self.project_type == "tool":
            return f"use the {self.skill_name} tool"
        else:
            return f"work with {self.skill_name}"
    
    # 以下是一些辅助方法，需要根据实际情况实现
    def _get_basic_usage_command(self) -> str:
        return f"# Basic usage command for {self.skill_name}"
    
    def _get_minimal_example(self) -> str:
        return f"# Minimal example for {self.skill_name}"
    
    def _format_features_list(self, features: List[str]) -> str:
        if features:
            return "\n".join([f"- {feature}" for feature in features])
        return "See project documentation for feature details."
    
    def _get_configuration_guide(self) -> str:
        return "See [CONFIGURATION.md](references/CONFIGURATION.md) for detailed configuration options."
    
    def _get_example_1_title(self) -> str:
        return "Basic Operation"
    
    def _get_example_1_code(self) -> str:
        return f"# Example 1 code for {self.skill_name}"
    
    def _get_example_2_title(self) -> str:
        return "Advanced Usage"
    
    def _get_example_2_code(self) -> str:
        return f"# Example 2 code for {self.skill_name}"
    
    def _get_common_issues(self) -> str:
        return "See [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) for common issues and solutions."
    
    def _get_help_resources(self) -> str:
        url = self.project_info.get("url", "")
        if url:
            return f"- [Project Repository]({url})\n- [Issue Tracker]({url}/issues)"
        return "Refer to project documentation for help."
    
    def _get_installation_command(self) -> str:
        clues = self.project_info.get("tech_clues", {})
        if clues.get("has_package_json"):
            return "npm install"
        elif clues.get("has_requirements"):
            return "pip install -r requirements.txt"
        else:
            return "# Check project documentation for installation instructions"
    
    def _generate_features_section(self) -> str:
        key_features = self.project_info.get("key_features", [])
        if key_features:
            return "\n".join([f"- {feature}" for feature in key_features[:10]])
        return "Features extracted from project documentation."
    
    # 以下方法需要根据项目类型实现具体的生成逻辑
    def _generate_example_colleague_data(self, skill_dir: str):
        """生成示例同事数据"""
        colleagues_dir = os.path.join(skill_dir, "colleagues")
        example_dir = os.path.join(colleagues_dir, "example_colleague")
        os.makedirs(example_dir, exist_ok=True)
        
        # 生成meta.json
        meta_content = {
            "name": "Example Colleague",
            "role": "Software Engineer",
            "expertise": ["Python", "API Development", "System Design"],
            "tenure": "2 years",
            "communication_style": "Direct and technical",
            "work_patterns": ["Agile", "Test-driven development"],
            "preferences": {
                "tools": ["VS Code", "Docker", "Git"],
                "formats": ["Markdown", "JSON"],
                "approaches": ["Modular design", "Documentation first"]
            }
        }
        
        with open(os.path.join(example_dir, "meta.json"), 'w', encoding='utf-8') as f:
            json.dump(meta_content, f, indent=2, ensure_ascii=False)
        
        # 生成persona.md
        persona_content = """# Persona for Example Colleague

## Communication Style
- Direct and to the point
- Prefers technical accuracy over politeness
- Uses emojis sparingly, mostly for positive reinforcement

## Work Habits
- Starts work at 9:00 AM, most productive in mornings
- Responds to messages within 1 hour during work hours
- Values code quality and comprehensive testing

## Professional Knowledge
- Expert in Python backend development
- Strong experience with REST API design
- Good understanding of cloud infrastructure
"""
        
        with open(os.path.join(example_dir, "persona.md"), 'w', encoding='utf-8') as f:
            f.write(persona_content)
        
        # 生成work.md
        work_content = """# Work Knowledge for Example Colleague

## Responsible Projects
- **User Authentication Service**: Python/FastAPI, JWT tokens, Redis caching
- **Payment Processing System**: Integration with Stripe and PayPal APIs
- **Data Analytics Pipeline**: AWS Lambda, S3, Athena queries

## Technical Specifications
- Follows PEP 8 for Python code style
- Requires 90%+ test coverage for new code
- Uses Docker for local development and deployment

## Common Issues
- **Database connection pooling**: Always use connection pools, monitor connection counts
- **API rate limiting**: Implement exponential backoff for external API calls
- **Error handling**: Use structured error responses, include request IDs
"""
        
        with open(os.path.join(example_dir, "work.md"), 'w', encoding='utf-8') as f:
            f.write(work_content)
    
    def _generate_colleague_scripts(self, skill_dir: str):
        """生成同事技能脚本"""
        scripts_dir = os.path.join(skill_dir, "scripts")
        
        # 导入脚本
        import_script = os.path.join(scripts_dir, "import-colleague.py")
        import_content = """#!/usr/bin/env python3
"""
        with open(import_script, 'w', encoding='utf-8') as f:
            f.write(import_content)
        
        os.chmod(import_script, 0o755)
    
    def _generate_colleague_references(self, skill_dir: str):
        """生成同事技能参考文档"""
        refs_dir = os.path.join(skill_dir, "references")
        os.makedirs(refs_dir, exist_ok=True)
        
        # 数据源文档
        sources_content = """# Data Sources

## Supported Data Sources

### Feishu (自动采集)
- **Message History**: Via Feishu OpenAPI
- **Documents**: Docs, sheets, mindnotes
- **Multi-dimensional Tables**: Bitable data

### DingTalk (部分自动)
- **Documents**: Auto-collection possible
- **Message History**: Limited by API restrictions

### Manual Import Formats
- PDF documents
- Images and screenshots
- Chat history exports
- Email archives
- Markdown files
"""
        
        with open(os.path.join(refs_dir, "DATA_SOURCES.md"), 'w', encoding='utf-8') as f:
            f.write(sources_content)
    
    def _generate_colleague_config(self, skill_dir: str):
        """生成同事技能配置"""
        config_dir = os.path.join(skill_dir, "config")
        os.makedirs(config_dir, exist_ok=True)
        
        config_content = {
            "skill_name": self.skill_name,
            "version": "1.0.0",
            "colleague_skill": True,
            "data_sources": ["feishu", "dingtalk", "manual"],
            "privacy_settings": {
                "data_encryption": True,
                "access_logging": True,
                "retention_days": 365
            }
        }
        
        with open(os.path.join(config_dir, "skill-config.json"), 'w', encoding='utf-8') as f:
            json.dump(config_content, f, indent=2, ensure_ascii=False)
    
    def _generate_openai_scripts(self, skill_dir: str):
        """生成OpenAI兼容脚本"""
        scripts_dir = os.path.join(skill_dir, "scripts")
        
        # 主脚本
        main_script = os.path.join(scripts_dir, "main.py")
        main_content = """#!/usr/bin/env python3
"""
        with open(main_script, 'w', encoding='utf-8') as f:
            f.write(main_content)
        
        os.chmod(main_script, 0o755)
    
    def _generate_openai_references(self, skill_dir: str):
        """生成OpenAI兼容参考文档（渐进式披露）"""
        refs_dir = os.path.join(skill_dir, "references")
        os.makedirs(refs_dir, exist_ok=True)
        
        # 高级功能文档
        advanced_content = """# Advanced Features

## Feature 1: Detailed Explanation
Detailed explanation of advanced feature 1.

## Feature 2: Configuration Options
All configuration options with examples.

## Feature 3: Integration Guide
How to integrate with other systems.
"""
        
        with open(os.path.join(refs_dir, "ADVANCED.md"), 'w', encoding='utf-8') as f:
            f.write(advanced_content)
        
        # 故障排除文档
        troubleshooting_content = """# Troubleshooting

## Common Issues

### Issue 1: Description
Solution and workaround.

### Issue 2: Description
Solution and workaround.

## Getting Help
- Check the documentation
- Search for similar issues
- Contact support if needed
"""
        
        with open(os.path.join(refs_dir, "TROUBLESHOOTING.md"), 'w', encoding='utf-8') as f:
            f.write(troubleshooting_content)
    
    def _generate_standard_config(self, skill_dir: str):
        """生成标准配置"""
        config_dir = os.path.join(skill_dir, "config")
        
        config_content = {
            "skill_name": self.skill_name,
            "source_project": self.project_info.get("full_name", ""),
            "generated_at": datetime.now().isoformat(),
            "project_type": self.project_type
        }
        
        with open(os.path.join(config_dir, "skill-config.json"), 'w', encoding='utf-8') as f:
            json.dump(config_content, f, indent=2, ensure_ascii=False)
    
    def _generate_standard_scripts(self, skill_dir: str):
        """生成标准脚本"""
        scripts_dir = os.path.join(skill_dir, "scripts")
        
        # 主运行脚本
        run_script = os.path.join(scripts_dir, "run.py")
        run_content = f"""#!/usr/bin/env python3
"""
        with open(run_script, 'w', encoding='utf-8') as f:
            f.write(run_content)
        
        os.chmod(run_script, 0o755)
    
    def _generate_standard_examples(self, skill_dir: str):
        """生成标准示例"""
        examples_dir = os.path.join(skill_dir, "examples")
        
        example_content = f"""# Examples for {self.skill_name}

## Basic Example

```bash
# Basic usage example
echo "Basic example for {self.skill_name}"
```

## Advanced Example

```bash
# Advanced usage example
echo "Advanced example for {self.skill_name}"
"""
        
        with open(os.path.join(examples_dir, "basic-usage.md"), 'w', encoding='utf-8') as f:
            f.write(example_content)

def main():
    parser = argparse.ArgumentParser(description="改进版Skill生成器 - 基于OpenAI指南和项目洞察")
    parser.add_argument("project_info", help="项目分析结果JSON文件")
    parser.add_argument("--output", "-o", default="./generated-skills", help="输出目录")
    parser.add_argument("--template", choices=["openai-compliant", "colleague-skill", "auto"], 
                       default="auto", help="模板类型（auto: 自动检测）")
    
    args = parser.parse_args()
    
    try:
        # 读取项目分析结果
        with open(args.project_info, 'r', encoding='utf-8') as f:
            project_info = json.load(f)
        
        # 生成Skill
        generator = ImprovedSkillGenerator(project_info, args.output, args.template)
        skill_dir = generator.generate()
        
        print(f"\n✅ Skill生成成功！")
        print(f"📁 Skill目录: {skill_dir}")
        print(f"🔤 Skill名称: {generator.skill_name}")
        print(f"🎯 项目类型: {generator.project_type}")
        print(f"📝 模板类型: {generator.template or 'auto'}")
        
        # 显示生成的文件
        print(f"\n📄 生成的文件:")
        for root, dirs, files in os.walk(skill_dir):
            level = root.replace(skill_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # 只显示前5个文件
                print(f"{subindent}{file}")
            if len(files) > 5:
                print(f"{subindent}... and {len(files)-5} more files")
        
        return 0
        
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())