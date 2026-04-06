#!/usr/bin/env python3
"""
EverythingSkill测试脚本
验证核心功能是否正常工作
"""

import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path

def test_analysis_scripts():
    """测试分析脚本"""
    print("🧪 测试分析脚本...")
    
    # 创建测试文件夹
    with tempfile.TemporaryDirectory() as temp_dir:
        test_folder = Path(temp_dir) / "test-project"
        test_folder.mkdir()
        
        # 创建测试文件
        (test_folder / "README.md").write_text("""
# Test Project

A test project for EverythingSkill.

## Features
- Feature 1: Does something useful
- Feature 2: Does something else useful

## Installation
```bash
pip install test-project
```

## Usage
```bash
test-project --help
```
""")
        
        (test_folder / "test.py").write_text("print('Hello World')")
        (test_folder / "requirements.txt").write_text("requests\npandas\n")
        
        # 测试文件夹分析
        print("  测试文件夹分析...")
        analyze_script = Path(__file__).parent / "analyze-folder.py"
        result = subprocess.run(
            [sys.executable, str(analyze_script), str(test_folder), "--output", "test-analysis.json"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("  ✅ 文件夹分析成功")
            
            # 检查分析结果
            if os.path.exists("test-analysis.json"):
                with open("test-analysis.json", 'r') as f:
                    analysis = json.load(f)
                
                assert analysis.get("name") == "test-project"
                assert analysis.get("project_type") in ["tool", "resource", "application", "unknown"]
                print("  ✅ 分析结果有效")
                
                # 清理
                os.remove("test-analysis.json")
            else:
                print("  ❌ 分析结果文件未创建")
                return False
        else:
            print(f"  ❌ 文件夹分析失败: {result.stderr}")
            return False
    
    print("✅ 分析脚本测试通过")
    return True

def test_generation_scripts():
    """测试生成脚本"""
    print("🧪 测试生成脚本...")
    
    # 创建测试分析数据
    test_analysis = {
        "name": "test-tool",
        "description": "A test tool for demonstration",
        "project_type": "tool",
        "key_features": ["Feature 1", "Feature 2", "Feature 3"],
        "tech_clues": {"has_requirements": True, "is_python": True}
    }
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 保存测试分析
        analysis_file = Path(temp_dir) / "test-analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(test_analysis, f)
        
        # 测试标准生成
        print("  测试标准生成...")
        generate_script = Path(__file__).parent / "generate-skill.py"
        result = subprocess.run(
            [sys.executable, str(generate_script), str(analysis_file), "--output", temp_dir],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # 检查生成的Skill
            skill_dir = Path(temp_dir) / "test-tool"
            if skill_dir.exists():
                required_files = ["SKILL.md", "config/skill-config.json"]
                for file in required_files:
                    if not (skill_dir / file).exists():
                        print(f"  ❌ 缺少必要文件: {file}")
                        return False
                
                print("  ✅ 标准生成成功")
            else:
                print("  ❌ Skill目录未创建")
                return False
        else:
            print(f"  ❌ 标准生成失败: {result.stderr}")
            return False
        
        # 测试改进版生成
        print("  测试改进版生成...")
        generate_v2_script = Path(__file__).parent / "generate-skill-v2.py"
        result = subprocess.run(
            [sys.executable, str(generate_v2_script), str(analysis_file), "--output", temp_dir, "--template", "openai-compliant"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("  ✅ 改进版生成成功")
        else:
            print(f"  ❌ 改进版生成失败: {result.stderr}")
            return False
    
    print("✅ 生成脚本测试通过")
    return True

def test_main_script():
    """测试主脚本"""
    print("🧪 测试主脚本...")
    
    # 创建测试文件夹
    with tempfile.TemporaryDirectory() as temp_dir:
        test_folder = Path(temp_dir) / "test-docs"
        test_folder.mkdir()
        
        # 创建测试文档
        (test_folder / "README.md").write_text("# Test Documentation\n\nSome test docs.")
        (test_folder / "guide.md").write_text("# User Guide\n\nHow to use.")
        
        # 测试主脚本
        main_script = Path(__file__).parent / "everything-skill.py"
        result = subprocess.run(
            [sys.executable, str(main_script), str(test_folder), "--output", temp_dir, "--type", "folder"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # 检查是否有生成的Skill
            skill_dirs = [d for d in Path(temp_dir).iterdir() if d.is_dir()]
            if skill_dirs:
                print("  ✅ 主脚本执行成功")
                
                # 检查生成的Skill
                skill_dir = skill_dirs[0]
                if (skill_dir / "SKILL.md").exists():
                    print("  ✅ Skill文档生成成功")
                else:
                    print("  ❌ Skill文档未生成")
                    return False
            else:
                print("  ❌ 未生成Skill目录")
                return False
        else:
            print(f"  ❌ 主脚本执行失败: {result.stderr}")
            return False
    
    print("✅ 主脚本测试通过")
    return True

def test_templates():
    """测试模板文件"""
    print("🧪 测试模板文件...")
    
    templates_dir = Path(__file__).parent / "templates"
    required_templates = [
        "tool-template.md",
        "resource-template.md",
        "openai-compliant-template.md",
        "colleague-skill-template.md"
    ]
    
    for template in required_templates:
        template_path = templates_dir / template
        if template_path.exists():
            # 检查模板内容
            content = template_path.read_text(encoding='utf-8')
            if len(content) > 100:  # 模板应该有足够的内容
                print(f"  ✅ 模板文件存在: {template}")
            else:
                print(f"  ⚠️  模板文件内容过少: {template}")
        else:
            print(f"  ❌ 缺少模板文件: {template}")
            return False
    
    print("✅ 模板文件测试通过")
    return True

def run_all_tests():
    """运行所有测试"""
    print("🚀 开始EverythingSkill测试...")
    print("=" * 50)
    
    tests = [
        ("分析脚本", test_analysis_scripts),
        ("生成脚本", test_generation_scripts),
        ("主脚本", test_main_script),
        ("模板文件", test_templates),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                print(f"✅ {test_name} - 通过")
            else:
                print(f"❌ {test_name} - 失败")
        except Exception as e:
            print(f"❌ {test_name} - 异常: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {status} - {test_name}")
    
    print(f"\n🎯 总体结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✨ 所有测试通过！EverythingSkill功能正常。")
        return 0
    else:
        print("⚠️  部分测试失败，请检查问题。")
        return 1

def quick_demo():
    """快速演示"""
    print("🎬 EverythingSkill快速演示")
    print("=" * 50)
    
    print("\n1. 📁 项目结构:")
    project_root = Path(__file__).parent.parent
    for item in project_root.rglob("*"):
        if item.is_file() and item.suffix in ['.py', '.md', '.json']:
            rel_path = item.relative_to(project_root)
            print(f"   {rel_path}")
    
    print("\n2. 🛠️  核心脚本:")
    scripts_dir = Path(__file__).parent
    for script in scripts_dir.glob("*.py"):
        print(f"   {script.name}")
    
    print("\n3. 📋 模板文件:")
    templates_dir = scripts_dir / "templates"
    for template in templates_dir.glob("*.md"):
        print(f"   {template.name}")
    
    print("\n4. 🚀 使用示例:")
    print("   # 转换GitHub项目")
    print("   python scripts/everything-skill.py https://github.com/example/repo --output ./skills")
    print("")
    print("   # 转换本地文件夹")
    print("   python scripts/everything-skill.py ./my-docs --output ./skills --type folder")
    print("")
    print("   # 使用改进版生成器")
    print("   python scripts/generate-skill-v2.py analysis.json --output ./skills --template openai-compliant")
    
    print("\n5. 📚 生成的文件:")
    print("   SKILL.md                    # 主技能文档")
    print("   agents/openai.yaml          # AI代理元数据")
    print("   scripts/                    # 执行脚本")
    print("   references/                 # 参考文档")
    print("   assets/                     # 资源文件")
    print("   config/                     # 配置文件")
    
    print("\n✨ 演示完成！")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        quick_demo()
    else:
        sys.exit(run_all_tests())