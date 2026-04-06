#!/usr/bin/env python3
"""
EverythingSkill主脚本
将GitHub项目或本地文件夹转换为Skill
"""

import argparse
import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Optional

def convert_github_to_skill(github_url: str, output_dir: str, api_token: Optional[str] = None) -> str:
    """将GitHub项目转换为Skill"""
    print(f"开始转换GitHub项目: {github_url}")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 步骤1: 分析GitHub项目
        print("步骤1: 分析GitHub项目...")
        analysis_file = os.path.join(temp_dir, "project-analysis.json")
        
        # 运行分析脚本
        analyze_script = os.path.join(os.path.dirname(__file__), "analyze-github.py")
        import subprocess
        cmd = [sys.executable, analyze_script, github_url, "--output", analysis_file]
        if api_token:
            cmd.extend(["--token", api_token])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"分析失败: {result.stderr}")
            return ""
        
        # 步骤2: 生成Skill
        print("步骤2: 生成Skill...")
        generate_script = os.path.join(os.path.dirname(__file__), "generate-skill.py")
        cmd = [sys.executable, generate_script, analysis_file, "--output", output_dir]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"生成失败: {result.stderr}")
            return ""
        
        # 读取生成结果
        with open(analysis_file, 'r', encoding='utf-8') as f:
            project_info = json.load(f)
        
        skill_name = project_info.get("name", "").lower()
        skill_name = skill_name.replace(' ', '-').replace('.', '-')
        
        skill_dir = os.path.join(output_dir, skill_name)
        if os.path.exists(skill_dir):
            print(f"Skill生成成功: {skill_dir}")
            return skill_dir
        else:
            print("Skill生成失败: 目录未创建")
            return ""

def convert_folder_to_skill(folder_path: str, output_dir: str) -> str:
    """将本地文件夹转换为Skill"""
    print(f"开始转换本地文件夹: {folder_path}")
    
    # 分析文件夹结构
    folder_info = analyze_local_folder(folder_path)
    if not folder_info:
        print("文件夹分析失败")
        return ""
    
    # 创建临时分析文件
    with tempfile.TemporaryDirectory() as temp_dir:
        analysis_file = os.path.join(temp_dir, "folder-analysis.json")
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(folder_info, f, indent=2, ensure_ascii=False)
        
        # 使用相同的生成脚本
        generate_script = os.path.join(os.path.dirname(__file__), "generate-skill.py")
        cmd = [sys.executable, generate_script, analysis_file, "--output", output_dir]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"生成失败: {result.stderr}")
            return ""
        
        skill_name = folder_info.get("name", "local-folder").lower()
        skill_name = skill_name.replace(' ', '-').replace('.', '-')
        
        skill_dir = os.path.join(output_dir, skill_name)
        if os.path.exists(skill_dir):
            print(f"Skill生成成功: {skill_dir}")
            
            # 复制原始文件夹内容到assets目录
            assets_dir = os.path.join(skill_dir, "assets", "original-content")
            os.makedirs(assets_dir, exist_ok=True)
            
            # 复制文件（排除一些不需要的文件）
            exclude_patterns = ['.git', '.github', '__pycache__', '.DS_Store']
            copy_folder_contents(folder_path, assets_dir, exclude_patterns)
            
            return skill_dir
        else:
            print("Skill生成失败: 目录未创建")
            return ""

def analyze_local_folder(folder_path: str) -> dict:
    """分析本地文件夹"""
    folder_path = Path(folder_path).absolute()
    if not folder_path.exists() or not folder_path.is_dir():
        return {}
    
    info = {
        "name": folder_path.name,
        "path": str(folder_path),
        "type": "local_folder",
        "file_count": 0,
        "dir_count": 0,
        "file_types": {},
        "important_files": [],
        "readme_content": "",
        "structure": []
    }
    
    # 遍历文件夹
    for root, dirs, files in os.walk(folder_path):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        rel_root = Path(root).relative_to(folder_path)
        
        for file in files:
            if file.startswith('.'):
                continue
                
            info["file_count"] += 1
            ext = Path(file).suffix.lower()
            if ext:
                info["file_types"][ext] = info["file_types"].get(ext, 0) + 1
            
            file_path = rel_root / file if str(rel_root) != '.' else Path(file)
            
            # 检查重要文件
            file_lower = file.lower()
            if any(keyword in file_lower for keyword in ['readme', 'license', 'package.json', 'requirements.txt', 
                                                       'cargo.toml', 'pyproject.toml', 'dockerfile', 'makefile']):
                info["important_files"].append(str(file_path))
            
            # 如果是README，读取内容
            if 'readme' in file_lower and file_lower.endswith('.md'):
                try:
                    with open(Path(root) / file, 'r', encoding='utf-8') as f:
                        info["readme_content"] = f.read(5000)  # 只读前5000字符
                except:
                    pass
    
    # 统计目录数量
    for root, dirs, _ in os.walk(folder_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        info["dir_count"] += len(dirs)
    
    # 分析项目类型
    info["project_type"] = determine_folder_type(info)
    
    # 提取关键信息
    info["description"] = extract_description(info)
    info["key_features"] = extract_features(info)
    
    return info

def determine_folder_type(info: dict) -> str:
    """确定文件夹类型"""
    file_types = info.get("file_types", {})
    important_files = info.get("important_files", [])
    
    # 检查技术栈线索
    has_python = any(ext in ['.py', '.pyc'] for ext in file_types)
    has_js = any(ext in ['.js', '.jsx', '.ts', '.tsx'] for ext in file_types)
    has_html = any(ext in ['.html', '.htm'] for ext in file_types)
    has_md = any(ext in ['.md', '.markdown'] for ext in file_types)
    
    # 检查配置文件
    has_package_json = any('package.json' in f.lower() for f in important_files)
    has_requirements = any('requirements.txt' in f.lower() for f in important_files)
    has_dockerfile = any('dockerfile' in f.lower() for f in important_files)
    
    # 推断类型
    if has_md and info.get("file_count", 0) > 10 and info.get("dir_count", 0) > 3:
        # 有很多Markdown文件和目录，可能是文档项目
        return "resource"
    elif has_package_json or has_js:
        # 有package.json或JS文件，可能是Node.js工具
        return "tool"
    elif has_python or has_requirements:
        # 有Python文件或requirements.txt，可能是Python工具
        return "tool"
    elif has_html and (has_js or has_python):
        # 有HTML和JS/Python，可能是Web应用
        return "application"
    elif has_dockerfile:
        # 有Dockerfile，可能是容器化应用
        return "application"
    else:
        return "unknown"

def extract_description(info: dict) -> str:
    """从文件夹信息提取描述"""
    readme = info.get("readme_content", "")
    
    # 从README提取第一段
    if readme:
        lines = readme.split('\n')
        description_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('!['):
                description_lines.append(line)
                if len(description_lines) >= 2:
                    break
        
        if description_lines:
            return ' '.join(description_lines)
    
    # 基于文件类型生成描述
    file_types = info.get("file_types", {})
    if file_types.get('.md', 0) > 5:
        return f"文档集合，包含 {file_types.get('.md', 0)} 个Markdown文件"
    elif file_types.get('.py', 0) > 3:
        return f"Python项目，包含 {file_types.get('.py', 0)} 个Python文件"
    elif file_types.get('.js', 0) > 3:
        return f"JavaScript项目，包含 {file_types.get('.js', 0)} 个JS文件"
    else:
        return f"本地项目，包含 {info.get('file_count', 0)} 个文件"

def extract_features(info: dict) -> list:
    """从文件夹信息提取功能特性"""
    features = []
    file_types = info.get("file_types", {})
    
    # 基于文件类型推断功能
    if file_types.get('.md', 0) > 0:
        features.append("提供文档资源")
    if file_types.get('.py', 0) > 0:
        features.append("包含Python代码")
    if file_types.get('.js', 0) > 0:
        features.append("包含JavaScript代码")
    if file_types.get('.json', 0) > 0:
        features.append("包含配置文件")
    if file_types.get('.html', 0) > 0:
        features.append("包含HTML页面")
    if file_types.get('.css', 0) > 0:
        features.append("包含样式文件")
    
    # 基于重要文件推断功能
    important_files = info.get("important_files", [])
    for file in important_files:
        file_lower = file.lower()
        if 'readme' in file_lower:
            features.append("提供使用说明")
        if 'license' in file_lower:
            features.append("包含许可证信息")
        if 'package.json' in file_lower:
            features.append("支持npm包管理")
        if 'requirements.txt' in file_lower:
            features.append("支持pip依赖管理")
        if 'dockerfile' in file_lower:
            features.append("支持容器化部署")
    
    return features[:5]  # 限制数量

def copy_folder_contents(src: str, dst: str, exclude_patterns: list):
    """复制文件夹内容，排除特定模式"""
    src_path = Path(src)
    dst_path = Path(dst)
    
    # 使用walk来避免递归深度问题
    for root, dirs, files in os.walk(src_path, topdown=True):
        # 过滤排除的目录
        dirs[:] = [d for d in dirs if not any(pattern in os.path.join(root, d) for pattern in exclude_patterns)]
        
        for file in files:
            file_path = Path(root) / file
            
            # 检查是否应该排除
            should_exclude = False
            for pattern in exclude_patterns:
                if pattern in str(file_path):
                    should_exclude = True
                    break
            
            if should_exclude:
                continue
            
            # 计算相对路径
            rel_path = file_path.relative_to(src_path)
            target_path = dst_path / rel_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, target_path)

def main():
    parser = argparse.ArgumentParser(description="EverythingSkill - 将GitHub项目或本地文件夹转换为Skill")
    parser.add_argument("source", help="GitHub URL或本地文件夹路径")
    parser.add_argument("--output", "-o", default=".", help="输出目录")
    parser.add_argument("--token", "-t", help="GitHub API令牌（用于GitHub项目）")
    parser.add_argument("--type", choices=["auto", "github", "folder"], default="auto", 
                       help="源类型（auto: 自动检测, github: GitHub项目, folder: 本地文件夹）")
    
    args = parser.parse_args()
    
    # 自动检测类型
    if args.type == "auto":
        if args.source.startswith(('http://', 'https://')) and 'github.com' in args.source:
            source_type = "github"
        elif os.path.isdir(args.source):
            source_type = "folder"
        else:
            print(f"错误: 无法识别源类型: {args.source}")
            print("请使用 --type 参数明确指定类型")
            return 1
    else:
        source_type = args.type
    
    # 确保输出目录存在
    os.makedirs(args.output, exist_ok=True)
    
    # 根据类型转换
    if source_type == "github":
        skill_dir = convert_github_to_skill(args.source, args.output, args.token)
    elif source_type == "folder":
        skill_dir = convert_folder_to_skill(args.source, args.output)
    else:
        print(f"错误: 不支持的源类型: {source_type}")
        return 1
    
    if skill_dir:
        print(f"\n✅ 转换成功！")
        print(f"Skill目录: {skill_dir}")
        print(f"\n下一步操作:")
        print(f"1. 检查生成的Skill: cd {skill_dir}")
        print(f"2. 查看SKILL.md文件")
        print(f"3. 根据需要手动优化内容")
        print(f"4. 测试Skill功能")
        return 0
    else:
        print("\n❌ 转换失败")
        return 1

if __name__ == "__main__":
    # 添加必要的导入
    import subprocess
    sys.exit(main())