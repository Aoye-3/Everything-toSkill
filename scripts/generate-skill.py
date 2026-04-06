#!/usr/bin/env python3
"""
Skill生成脚本
基于项目分析结果生成Skill目录结构
"""

import argparse
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class SkillGenerator:
    """Skill生成器"""
    
    def __init__(self, project_info: Dict[str, Any], output_dir: str):
        self.project_info = project_info
        self.output_dir = output_dir
        self.skill_name = self._generate_skill_name()
        
    def _generate_skill_name(self) -> str:
        """生成Skill名称"""
        name = self.project_info.get("name", "").lower()
        
        # 移除特殊字符，用连字符替换空格和点
        name = re.sub(r'[^\w\s-]', '', name)
        name = re.sub(r'[-\s]+', '-', name)
        
        # 确保名称以字母开头
        if name and not name[0].isalpha():
            name = "skill-" + name
        
        return name or "generated-skill"
    
    def generate(self):
        """生成完整的Skill结构"""
        print(f"生成Skill: {self.skill_name}")
        
        # 创建Skill目录
        skill_dir = os.path.join(self.output_dir, self.skill_name)
        os.makedirs(skill_dir, exist_ok=True)
        
        # 生成SKILL.md
        self._generate_skill_md(skill_dir)
        
        # 创建子目录
        subdirs = ["scripts", "config", "assets", "examples"]
        for subdir in subdirs:
            os.makedirs(os.path.join(skill_dir, subdir), exist_ok=True)
        
        # 根据项目类型生成特定内容
        project_type = self.project_info.get("project_type", "unknown")
        
        if project_type == "tool":
            self._generate_tool_skill(skill_dir)
        elif project_type == "resource":
            self._generate_resource_skill(skill_dir)
        elif project_type == "application":
            self._generate_app_skill(skill_dir)
        else:
            self._generate_generic_skill(skill_dir)
        
        # 生成配置文件
        self._generate_config_files(skill_dir)
        
        # 生成示例文件
        self._generate_example_files(skill_dir)
        
        print(f"Skill生成完成！目录: {skill_dir}")
        return skill_dir
    
    def _generate_skill_md(self, skill_dir: str):
        """生成SKILL.md文件"""
        skill_md_path = os.path.join(skill_dir, "SKILL.md")
        
        # 提取项目信息
        name = self.project_info.get("name", "")
        description = self.project_info.get("description", "")
        full_name = self.project_info.get("full_name", "")
        url = self.project_info.get("url", "")
        language = self.project_info.get("language", "")
        project_type = self.project_info.get("project_type", "unknown")
        
        # 生成触发条件描述
        trigger_description = self._generate_trigger_description()
        
        # 生成SKILL.md内容
        content = f"""---
name: "{self.skill_name}"
description: "{description} {trigger_description}"
---

# {name}

{description}

## 项目信息

- **GitHub仓库**: [{full_name}]({url})
- **主要语言**: {language or "未指定"}
- **项目类型**: {self._get_project_type_display(project_type)}
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 快速开始

### 安装依赖

```bash
# 根据项目类型选择适当的安装命令
{self._get_installation_commands()}
```

### 基本使用

```bash
# 基本命令示例
{self._get_basic_usage()}
```

## 功能特性

{self._generate_features_section()}

## 详细指南

### 配置说明

{self._generate_config_section()}

### API参考

{self._generate_api_section()}

### 示例

{self._generate_examples_section()}

## 故障排除

{self._generate_troubleshooting_section()}

## 相关资源

- [GitHub仓库]({url})
- [问题跟踪]({url}/issues)
- [讨论区]({url}/discussions)

---

*此Skill由EverythingSkill自动生成，基于GitHub项目: {full_name}*
"""
        
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_trigger_description(self) -> str:
        """生成触发条件描述"""
        project_type = self.project_info.get("project_type", "unknown")
        key_features = self.project_info.get("key_features", [])
        
        if project_type == "tool":
            base_desc = "Use when user needs to perform tasks related to"
        elif project_type == "resource":
            base_desc = "Use when user needs access to resources about"
        elif project_type == "application":
            base_desc = "Use when user needs to work with applications for"
        else:
            base_desc = "Use when user needs assistance with"
        
        # 添加关键功能
        if key_features:
            features_text = ", ".join(key_features[:3])
            return f"{base_desc} {features_text}"
        else:
            project_name = self.project_info.get("name", "this tool")
            return f"{base_desc} {project_name}"
    
    def _get_project_type_display(self, project_type: str) -> str:
        """获取项目类型显示文本"""
        type_map = {
            "tool": "工具类项目",
            "resource": "资源类项目", 
            "application": "应用类项目",
            "framework": "框架类项目",
            "unknown": "未知类型"
        }
        return type_map.get(project_type, "未知类型")
    
    def _get_installation_commands(self) -> str:
        """获取安装命令"""
        clues = self.project_info.get("tech_clues", {})
        
        if clues.get("has_package_json"):
            return "npm install\n# 或\nyarn install"
        elif clues.get("has_requirements"):
            return "pip install -r requirements.txt"
        elif clues.get("has_cargo_toml"):
            return "cargo build"
        elif clues.get("is_python"):
            return "pip install ."
        elif clues.get("is_js"):
            return "npm install"
        else:
            return "# 请参考项目README中的安装说明"
    
    def _get_basic_usage(self) -> str:
        """获取基本使用命令"""
        project_name = self.project_info.get("name", "").lower()
        
        if "cli" in project_name or "command" in project_name:
            return f"{project_name} --help"
        else:
            return f"# 请参考项目README中的使用说明"
    
    def _generate_features_section(self) -> str:
        """生成功能特性部分"""
        key_features = self.project_info.get("key_features", [])
        
        if key_features:
            features_text = "\n".join([f"- {feature}" for feature in key_features])
            return features_text
        else:
            return "请参考项目README了解详细功能特性。"
    
    def _generate_config_section(self) -> str:
        """生成配置说明部分"""
        return """配置选项因项目而异。请参考项目文档了解详细的配置说明。

常见配置方式：
1. 环境变量
2. 配置文件（如 config.json, .env 等）
3. 命令行参数
"""
    
    def _generate_api_section(self) -> str:
        """生成API参考部分"""
        return """API接口因项目类型而异：

- **工具类项目**: 通常提供命令行接口
- **库/框架类项目**: 提供编程接口和文档
- **应用类项目**: 提供用户界面或Web API

请参考项目文档了解详细的API说明。
"""
    
    def _generate_examples_section(self) -> str:
        """生成示例部分"""
        return """### 示例1: 基本使用

```bash
# 基本命令示例
echo "请根据实际项目替换此示例"
```

### 示例2: 高级功能

```python
# Python使用示例（如果适用）
import generated_module

result = generated_module.do_something()
print(result)
```

更多示例请参考项目文档和examples目录。
"""
    
    def _generate_troubleshooting_section(self) -> str:
        """生成故障排除部分"""
        return """## 常见问题

### 1. 安装失败
- 检查系统依赖是否满足
- 查看错误信息中的具体提示
- 参考项目README中的安装说明

### 2. 运行错误
- 检查配置文件是否正确
- 验证输入参数格式
- 查看日志文件获取详细信息

### 3. 功能异常
- 检查版本兼容性
- 查看已知问题列表
- 在GitHub Issues中搜索类似问题

## 获取帮助

1. 查看项目README文档
2. 搜索GitHub Issues
3. 在讨论区提问
"""
    
    def _generate_tool_skill(self, skill_dir: str):
        """生成工具类Skill的特定内容"""
        # 创建工具类特定的脚本
        scripts_dir = os.path.join(skill_dir, "scripts")
        
        # 创建包装器脚本模板
        wrapper_script = os.path.join(scripts_dir, "run-tool.py")
        wrapper_content = """#!/usr/bin/env python3
"""
        with open(wrapper_script, 'w', encoding='utf-8') as f:
            f.write(wrapper_content)
        
        # 使脚本可执行
        os.chmod(wrapper_script, 0o755)
    
    def _generate_resource_skill(self, skill_dir: str):
        """生成资源类Skill的特定内容"""
        # 创建资源索引文件
        resources_dir = os.path.join(skill_dir, "assets")
        
        # 创建资源索引
        index_file = os.path.join(resources_dir, "RESOURCES.md")
        index_content = f"""# 资源索引

此Skill提供以下资源：

## 文档资源

1. 项目文档
2. 使用指南
3. 示例代码

## 模板文件

1. 配置模板
2. 代码模板
3. 文档模板

## 其他资源

请参考原始GitHub项目获取完整资源列表。
"""
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
    
    def _generate_app_skill(self, skill_dir: str):
        """生成应用类Skill的特定内容"""
        # 创建应用配置模板
        config_dir = os.path.join(skill_dir, "config")
        
        # 创建配置模板
        config_template = os.path.join(config_dir, "config-template.json")
        template_content = """{
  "app_config": {
    "host": "localhost",
    "port": 3000,
    "debug": false,
    "database": {
      "url": "postgresql://localhost/appdb"
    }
  }
}
"""
        with open(config_template, 'w', encoding='utf-8') as f:
            f.write(template_content)
    
    def _generate_generic_skill(self, skill_dir: str):
        """生成通用Skill内容"""
        # 创建通用README
        readme_file = os.path.join(skill_dir, "README-SKILL.md")
        readme_content = f"""# Skill使用说明

此Skill基于GitHub项目生成，提供对以下功能的访问：

## 可用功能

1. 项目核心功能
2. 常用命令和操作
3. 配置和部署指南

## 使用方法

在IDE中使用此Skill时，系统会自动识别相关任务并调用适当的工具和脚本。

## 注意事项

- 此Skill为自动生成，可能需要手动优化
- 某些功能可能需要额外配置
- 请参考原始项目文档获取最新信息
"""
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def _generate_config_files(self, skill_dir: str):
        """生成配置文件"""
        config_dir = os.path.join(skill_dir, "config")
        
        # 创建skill-config.json
        config_file = os.path.join(config_dir, "skill-config.json")
        config_content = {
            "skill_name": self.skill_name,
            "source_project": self.project_info.get("full_name", ""),
            "source_url": self.project_info.get("url", ""),
            "generated_at": datetime.now().isoformat(),
            "project_type": self.project_info.get("project_type", "unknown"),
            "version": "1.0.0",
            "requires_setup": True,
            "dependencies": self._extract_dependencies()
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_content, f, indent=2, ensure_ascii=False)
    
    def _extract_dependencies(self) -> list:
        """提取依赖信息"""
        dependencies = []
        clues = self.project_info.get("tech_clues", {})
        
        if clues.get("has_package_json"):
            dependencies.append("Node.js/npm")
        if clues.get("has_requirements"):
            dependencies.append("Python/pip")
        if clues.get("has_cargo_toml"):
            dependencies.append("Rust/cargo")
        if clues.get("has_dockerfile"):
            dependencies.append("Docker")
        
        return dependencies
    
    def _generate_example_files(self, skill_dir: str):
        """生成示例文件"""
        examples_dir = os.path.join(skill_dir, "examples")
        
        # 创建基本示例
        basic_example = os.path.join(examples_dir, "basic-usage.md")
        example_content = f"""# 基本使用示例

## 示例1: 运行工具

```bash
# 根据项目类型运行相应的命令
echo "运行 {self.project_info.get('name', '项目')}"
```

## 示例2: 配置项目

```bash
# 配置示例
echo "配置步骤因项目而异"
```

## 示例3: 测试功能

```bash
# 测试命令
echo "运行测试以确保功能正常"
```

更多示例请参考原始项目文档。
"""
        with open(basic_example, 'w', encoding='utf-8') as f:
            f.write(example_content)

# 添加缺失的导入
import re

def main():
    parser = argparse.ArgumentParser(description="基于项目分析结果生成Skill")
    parser.add_argument("project_info", help="项目分析结果JSON文件")
    parser.add_argument("--output", "-o", default=".", help="输出目录")
    
    args = parser.parse_args()
    
    try:
        # 读取项目分析结果
        with open(args.project_info, 'r', encoding='utf-8') as f:
            project_info = json.load(f)
        
        # 生成Skill
        generator = SkillGenerator(project_info, args.output)
        skill_dir = generator.generate()
        
        print(f"\nSkill生成成功！")
        print(f"Skill目录: {skill_dir}")
        print(f"Skill名称: {generator.skill_name}")
        print(f"项目类型: {project_info.get('project_type', 'unknown')}")
        
        return 0
        
    except Exception as e:
        print(f"错误: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())