#!/usr/bin/env python3
"""
本地文件夹分析脚本
用于分析本地文件夹结构并提取Skill转换所需信息
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set
import mimetypes

class FolderAnalyzer:
    """本地文件夹分析器"""
    
    def __init__(self, folder_path: str):
        self.folder_path = Path(folder_path).absolute()
        if not self.folder_path.exists():
            raise ValueError(f"文件夹不存在: {folder_path}")
        if not self.folder_path.is_dir():
            raise ValueError(f"路径不是文件夹: {folder_path}")
        
        self.project_info = {}
    
    def analyze(self) -> Dict:
        """分析文件夹"""
        print(f"开始分析文件夹: {self.folder_path}")
        
        # 基本信息
        self.project_info = {
            "name": self.folder_path.name,
            "path": str(self.folder_path),
            "type": "local_folder",
            "analyzed_at": self._get_current_time(),
        }
        
        # 分析文件夹结构
        self._analyze_structure()
        
        # 分析文件类型和内容
        self._analyze_files()
        
        # 分析README和文档
        self._analyze_documentation()
        
        # 确定项目类型
        self._determine_project_type()
        
        # 提取关键功能
        self._extract_key_features()
        
        # 生成项目描述
        self._generate_description()
        
        print(f"分析完成！项目类型: {self.project_info.get('project_type', '未知')}")
        return self.project_info
    
    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _analyze_structure(self):
        """分析文件夹结构"""
        total_files = 0
        total_dirs = 0
        file_extensions = {}
        dir_structure = []
        
        # 遍历文件夹（限制深度）
        max_depth = 4
        excluded_dirs = {'.git', '.github', '__pycache__', 'node_modules', '.venv', 'venv', '.env'}
        
        def scan_dir(current_path: Path, depth: int, parent_list: List):
            nonlocal total_files, total_dirs
            
            if depth > max_depth:
                return
            
            try:
                items = list(current_path.iterdir())
            except (PermissionError, OSError):
                return
            
            for item in sorted(items, key=lambda x: x.name.lower()):
                # 跳过隐藏文件和排除的目录
                if item.name.startswith('.') or item.name in excluded_dirs:
                    continue
                
                item_info = {
                    "name": item.name,
                    "type": "dir" if item.is_dir() else "file",
                    "path": str(item.relative_to(self.folder_path)),
                }
                
                if item.is_dir():
                    total_dirs += 1
                    item_info["contents"] = []
                    parent_list.append(item_info)
                    scan_dir(item, depth + 1, item_info["contents"])
                else:
                    total_files += 1
                    # 统计文件扩展名
                    ext = item.suffix.lower()
                    if ext:
                        file_extensions[ext] = file_extensions.get(ext, 0) + 1
                    
                    # 记录文件大小
                    try:
                        item_info["size"] = item.stat().st_size
                    except:
                        item_info["size"] = 0
                    
                    parent_list.append(item_info)
        
        scan_dir(self.folder_path, 0, dir_structure)
        
        self.project_info.update({
            "file_count": total_files,
            "dir_count": total_dirs,
            "file_extensions": file_extensions,
            "structure": dir_structure,
            "total_size": self._calculate_total_size(),
        })
    
    def _calculate_total_size(self) -> int:
        """计算文件夹总大小"""
        total_size = 0
        for root, dirs, files in os.walk(self.folder_path):
            # 跳过一些目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                file_path = Path(root) / file
                try:
                    total_size += file_path.stat().st_size
                except:
                    pass
        
        return total_size
    
    def _analyze_files(self):
        """分析文件内容"""
        important_files = []
        code_files = []
        config_files = []
        document_files = []
        
        # 重要文件模式
        important_patterns = [
            r'^readme\.', r'^license', r'^contributing', r'^changelog',
            r'package\.json$', r'requirements\.txt$', r'pyproject\.toml$',
            r'cargo\.toml$', r'go\.mod$', r'gemfile$', r'composer\.json$',
            r'dockerfile$', r'docker-compose\.yml$', r'makefile$',
            r'\.gitignore$', r'\.env\.example$', r'\.travis\.yml$', r'\.github/',
        ]
        
        # 代码文件扩展名
        code_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h', 
                          '.go', '.rs', '.php', '.rb', '.swift', '.kt', '.scala', '.cs'}
        
        # 配置文件扩展名
        config_extensions = {'.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.env'}
        
        # 文档文件扩展名
        doc_extensions = {'.md', '.txt', '.rst', '.adoc', '.tex', '.pdf'}
        
        for root, dirs, files in os.walk(self.folder_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.folder_path)
                
                # 检查重要文件
                for pattern in important_patterns:
                    if re.search(pattern, file, re.IGNORECASE):
                        important_files.append(str(rel_path))
                        break
                
                # 分类文件类型
                ext = file_path.suffix.lower()
                if ext in code_extensions:
                    code_files.append(str(rel_path))
                elif ext in config_extensions:
                    config_files.append(str(rel_path))
                elif ext in doc_extensions:
                    document_files.append(str(rel_path))
        
        self.project_info.update({
            "important_files": important_files,
            "code_files": code_files[:50],  # 限制数量
            "config_files": config_files[:20],
            "document_files": document_files[:30],
        })
    
    def _analyze_documentation(self):
        """分析文档内容"""
        readme_content = ""
        license_content = ""
        
        # 查找README文件
        readme_patterns = [r'^readme\.', r'^readme\.md$', r'^readme\.txt$']
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                for pattern in readme_patterns:
                    if re.search(pattern, file, re.IGNORECASE):
                        try:
                            file_path = Path(root) / file
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                readme_content = f.read(10000)  # 限制读取大小
                            break
                        except:
                            pass
        
        # 查找LICENSE文件
        license_patterns = [r'^license', r'^copying', r'^licence']
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                for pattern in license_patterns:
                    if re.search(pattern, file, re.IGNORECASE):
                        try:
                            file_path = Path(root) / file
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                license_content = f.read(5000)
                            break
                        except:
                            pass
        
        # 提取README中的关键信息
        title = ""
        description = ""
        features = []
        
        if readme_content:
            # 提取标题
            title_match = re.search(r'^#\s+(.+)$', readme_content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
            
            # 提取描述（第一段非标题文本）
            lines = readme_content.split('\n')
            desc_lines = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('!['):
                    desc_lines.append(line)
                    if len(desc_lines) >= 3:
                        break
            
            if desc_lines:
                description = ' '.join(desc_lines)
            
            # 提取功能列表
            features_section = self._extract_section(readme_content, ['features', '功能', '特性'])
            if features_section:
                # 提取列表项
                list_items = re.findall(r'[-*]\s+(.+)$', features_section, re.MULTILINE)
                features = [item.strip() for item in list_items[:10]]
        
        self.project_info.update({
            "title": title,
            "description": description,
            "readme_content": readme_content[:5000] if readme_content else "",  # 限制大小
            "license_content": license_content[:2000] if license_content else "",
            "extracted_features": features,
        })
    
    def _extract_section(self, content: str, section_names: List[str]) -> str:
        """从内容中提取特定部分"""
        content_lower = content.lower()
        
        for name in section_names:
            pattern = rf'^#+\s*{name}\s*$'
            match = re.search(pattern, content_lower, re.MULTILINE | re.IGNORECASE)
            if match:
                start_pos = match.end()
                # 查找下一个同级标题
                next_section = re.search(r'^#+\s+', content[start_pos:], re.MULTILINE)
                if next_section:
                    end_pos = start_pos + next_section.start()
                    return content[start_pos:end_pos].strip()
                else:
                    return content[start_pos:].strip()
        
        return ""
    
    def _determine_project_type(self):
        """确定项目类型"""
        file_extensions = self.project_info.get("file_extensions", {})
        important_files = self.project_info.get("important_files", [])
        code_files = self.project_info.get("code_files", [])
        document_files = self.project_info.get("document_files", [])
        
        # 技术栈线索
        clues = {
            "is_python": any(ext in ['.py'] for ext in file_extensions),
            "is_js": any(ext in ['.js', '.jsx', '.ts', '.tsx'] for ext in file_extensions),
            "is_web": any(ext in ['.html', '.htm', '.css'] for ext in file_extensions),
            "is_documentation": len(document_files) > len(code_files) * 2,  # 文档远多于代码
            "has_package_json": any('package.json' in f.lower() for f in important_files),
            "has_requirements": any('requirements.txt' in f.lower() for f in important_files),
            "has_dockerfile": any('dockerfile' in f.lower() for f in important_files),
            "has_many_md": file_extensions.get('.md', 0) > 10,
        }
        
        # 基于线索确定类型
        project_type = "unknown"
        
        if clues["is_documentation"] or clues["has_many_md"]:
            project_type = "resource"
        elif clues["is_python"] or clues["is_js"] or clues["has_package_json"] or clues["has_requirements"]:
            project_type = "tool"
        elif clues["is_web"]:
            project_type = "application"
        elif clues["has_dockerfile"]:
            project_type = "application"
        
        self.project_info["tech_clues"] = clues
        self.project_info["project_type"] = project_type
    
    def _extract_key_features(self):
        """提取关键功能"""
        features = []
        
        # 从提取的特征中添加
        extracted = self.project_info.get("extracted_features", [])
        features.extend(extracted)
        
        # 从文件类型推断
        file_extensions = self.project_info.get("file_extensions", {})
        if file_extensions.get('.md', 0) > 0:
            features.append(f"包含 {file_extensions.get('.md', 0)} 个文档文件")
        if file_extensions.get('.py', 0) > 0:
            features.append(f"包含 {file_extensions.get('.py', 0)} 个Python脚本")
        if file_extensions.get('.js', 0) > 0:
            features.append(f"包含 {file_extensions.get('.js', 0)} 个JavaScript文件")
        if file_extensions.get('.json', 0) > 0:
            features.append("提供JSON配置文件")
        
        # 从重要文件推断
        important_files = self.project_info.get("important_files", [])
        for file in important_files:
            if 'dockerfile' in file.lower():
                features.append("支持容器化部署")
            if 'package.json' in file.lower():
                features.append("使用npm包管理")
            if 'requirements.txt' in file.lower():
                features.append("使用pip依赖管理")
        
        # 去重并限制数量
        unique_features = []
        seen = set()
        for feature in features:
            if feature not in seen:
                seen.add(feature)
                unique_features.append(feature)
        
        self.project_info["key_features"] = unique_features[:10]
    
    def _generate_description(self):
        """生成项目描述"""
        title = self.project_info.get("title", "")
        extracted_desc = self.project_info.get("description", "")
        
        if extracted_desc:
            self.project_info["generated_description"] = extracted_desc
            return
        
        # 基于分析生成描述
        project_type = self.project_info.get("project_type", "")
        file_count = self.project_info.get("file_count", 0)
        dir_count = self.project_info.get("dir_count", 0)
        
        if project_type == "resource":
            desc = f"文档资源集合，包含 {file_count} 个文件"
            if dir_count > 0:
                desc += f"和 {dir_count} 个目录"
        elif project_type == "tool":
            desc = f"工具项目，包含 {file_count} 个文件"
        elif project_type == "application":
            desc = f"应用程序项目，包含 {file_count} 个文件"
        else:
            desc = f"本地项目，包含 {file_count} 个文件"
        
        if title:
            desc = f"{title} - {desc}"
        
        self.project_info["generated_description"] = desc

def main():
    parser = argparse.ArgumentParser(description="分析本地文件夹并提取Skill转换所需信息")
    parser.add_argument("folder_path", help="本地文件夹路径")
    parser.add_argument("--output", "-o", help="输出JSON文件路径")
    
    args = parser.parse_args()
    
    try:
        analyzer = FolderAnalyzer(args.folder_path)
        folder_info = analyzer.analyze()
        
        # 输出结果
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(folder_info, f, indent=2, ensure_ascii=False)
            print(f"结果已保存到: {args.output}")
        else:
            print(json.dumps(folder_info, indent=2, ensure_ascii=False))
        
        return 0
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())