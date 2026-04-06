#!/usr/bin/env python3
"""
GitHub项目分析脚本
用于分析GitHub项目并提取关键信息，为Skill转换做准备
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional, Tuple
import requests
from urllib.parse import urlparse

class GitHubAnalyzer:
    """GitHub项目分析器"""
    
    def __init__(self, github_url: str, api_token: Optional[str] = None):
        self.github_url = github_url
        self.api_token = api_token
        self.project_info = {}
        
        # 解析GitHub URL
        parsed = urlparse(github_url)
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) < 2:
            raise ValueError(f"无效的GitHub URL: {github_url}")
        
        self.owner = path_parts[0]
        self.repo = path_parts[1]
        
        # GitHub API基础URL
        self.api_base = "https://api.github.com"
        self.headers = {}
        if api_token:
            self.headers["Authorization"] = f"token {api_token}"
    
    def analyze(self) -> Dict:
        """分析GitHub项目"""
        print(f"开始分析GitHub项目: {self.owner}/{self.repo}")
        
        # 获取仓库基本信息
        repo_info = self._get_repo_info()
        if not repo_info:
            raise Exception("无法获取仓库信息")
        
        self.project_info = {
            "name": repo_info.get("name", ""),
            "full_name": repo_info.get("full_name", ""),
            "description": repo_info.get("description", ""),
            "url": repo_info.get("html_url", ""),
            "language": repo_info.get("language", ""),
            "stars": repo_info.get("stargazers_count", 0),
            "forks": repo_info.get("forks_count", 0),
            "created_at": repo_info.get("created_at", ""),
            "updated_at": repo_info.get("updated_at", ""),
            "license": repo_info.get("license", {}).get("name", "") if repo_info.get("license") else "",
            "topics": repo_info.get("topics", []),
            "has_wiki": repo_info.get("has_wiki", False),
            "has_pages": repo_info.get("has_pages", False),
            "default_branch": repo_info.get("default_branch", "main"),
        }
        
        # 获取README内容
        readme_content = self._get_readme()
        if readme_content:
            self.project_info["readme"] = readme_content
            self._analyze_readme(readme_content)
        
        # 获取文件结构
        file_structure = self._get_file_structure()
        self.project_info["file_structure"] = file_structure
        self._analyze_file_structure(file_structure)
        
        # 确定项目类型
        self._determine_project_type()
        
        # 提取关键功能
        self._extract_key_features()
        
        print(f"分析完成！项目类型: {self.project_info.get('project_type', '未知')}")
        return self.project_info
    
    def _get_repo_info(self) -> Optional[Dict]:
        """获取仓库基本信息"""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取仓库信息失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取仓库信息时出错: {e}")
            return None
    
    def _get_readme(self) -> Optional[str]:
        """获取README内容"""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/readme"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                # GitHub API返回的是base64编码的内容
                import base64
                content = base64.b64decode(data["content"]).decode("utf-8")
                return content
            else:
                print(f"获取README失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取README时出错: {e}")
            return None
    
    def _get_file_structure(self, path: str = "") -> List[Dict]:
        """获取文件结构"""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/contents/{path}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                contents = response.json()
                file_structure = []
                
                for item in contents:
                    item_info = {
                        "name": item["name"],
                        "type": item["type"],
                        "path": item["path"],
                        "size": item.get("size", 0),
                    }
                    
                    if item["type"] == "dir":
                        # 递归获取子目录内容（限制深度）
                        if path.count('/') < 2:  # 限制递归深度
                            item_info["contents"] = self._get_file_structure(item["path"])
                    
                    file_structure.append(item_info)
                
                return file_structure
            else:
                print(f"获取文件结构失败: {response.status_code}")
                return []
        except Exception as e:
            print(f"获取文件结构时出错: {e}")
            return []
    
    def _analyze_readme(self, readme_content: str):
        """分析README内容"""
        # 提取标题
        title_match = re.search(r'^#\s+(.+)$', readme_content, re.MULTILINE)
        if title_match:
            self.project_info["title"] = title_match.group(1).strip()
        
        # 提取描述（第一段非标题文本）
        lines = readme_content.split('\n')
        description_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('!['):
                description_lines.append(line)
                if len(description_lines) >= 3:  # 取前3行作为描述
                    break
        
        if description_lines:
            self.project_info["readme_description"] = ' '.join(description_lines)
        
        # 检查常见部分
        sections = {
            "installation": False,
            "usage": False,
            "examples": False,
            "api": False,
            "contributing": False,
            "license": False,
        }
        
        readme_lower = readme_content.lower()
        for section in sections:
            if re.search(rf'^#+\s*{section}', readme_lower, re.MULTILINE):
                sections[section] = True
        
        self.project_info["readme_sections"] = sections
    
    def _analyze_file_structure(self, file_structure: List[Dict]):
        """分析文件结构"""
        file_extensions = {}
        important_files = []
        
        def traverse_structure(structure: List[Dict], depth: int = 0):
            nonlocal file_extensions, important_files
            
            for item in structure:
                if item["type"] == "file":
                    # 统计文件扩展名
                    ext = os.path.splitext(item["name"])[1].lower()
                    if ext:
                        file_extensions[ext] = file_extensions.get(ext, 0) + 1
                    
                    # 检查重要文件
                    name_lower = item["name"].lower()
                    if name_lower in ["readme.md", "readme", "license", "license.txt", "license.md", 
                                     "package.json", "requirements.txt", "cargo.toml", "pyproject.toml",
                                     "dockerfile", "docker-compose.yml", "makefile", "cmakelists.txt"]:
                        important_files.append(item["path"])
                
                elif item["type"] == "dir" and "contents" in item:
                    traverse_structure(item["contents"], depth + 1)
        
        traverse_structure(file_structure)
        
        self.project_info["file_extensions"] = file_extensions
        self.project_info["important_files"] = important_files
        
        # 检测项目类型线索
        clues = {
            "is_python": any(ext in [".py", ".pyc", ".pyo"] for ext in file_extensions),
            "is_js": any(ext in [".js", ".jsx", ".ts", ".tsx"] for ext in file_extensions),
            "is_rust": any(ext in [".rs"] for ext in file_extensions),
            "is_go": any(ext in [".go"] for ext in file_extensions),
            "is_java": any(ext in [".java", ".jar"] for ext in file_extensions),
            "has_package_json": "package.json" in [os.path.basename(f) for f in important_files],
            "has_requirements": "requirements.txt" in [os.path.basename(f) for f in important_files],
            "has_cargo_toml": "cargo.toml" in [os.path.basename(f) for f in important_files],
            "has_dockerfile": any("dockerfile" in f.lower() for f in important_files),
        }
        
        self.project_info["tech_clues"] = clues
    
    def _determine_project_type(self):
        """确定项目类型"""
        clues = self.project_info.get("tech_clues", {})
        description = self.project_info.get("description", "").lower()
        readme_desc = self.project_info.get("readme_description", "").lower()
        full_text = f"{description} {readme_desc}"
        
        # 项目类型分类
        project_type = "unknown"
        confidence = 0
        
        # 检查工具类项目关键词
        tool_keywords = ["tool", "utility", "cli", "command-line", "library", "sdk", "api", "framework"]
        tool_matches = sum(1 for kw in tool_keywords if kw in full_text)
        
        # 检查资源类项目关键词
        resource_keywords = ["collection", "curated", "awesome", "list", "resources", "examples", "templates"]
        resource_matches = sum(1 for kw in resource_keywords if kw in full_text)
        
        # 检查应用类项目关键词
        app_keywords = ["app", "application", "web app", "desktop", "mobile", "game", "service"]
        app_matches = sum(1 for kw in app_keywords if kw in full_text)
        
        # 基于关键词确定类型
        if tool_matches > resource_matches and tool_matches > app_matches:
            project_type = "tool"
            confidence = tool_matches / len(tool_keywords)
        elif resource_matches > tool_matches and resource_matches > app_matches:
            project_type = "resource"
            confidence = resource_matches / len(resource_keywords)
        elif app_matches > tool_matches and app_matches > resource_matches:
            project_type = "application"
            confidence = app_matches / len(app_keywords)
        else:
            # 基于技术栈猜测
            if clues.get("has_package_json") or clues.get("is_js"):
                project_type = "tool"  # 大多数JS项目是工具类
            elif clues.get("has_requirements") or clues.get("is_python"):
                project_type = "tool"  # 大多数Python项目是工具类
            else:
                project_type = "unknown"
        
        self.project_info["project_type"] = project_type
        self.project_info["type_confidence"] = confidence
    
    def _extract_key_features(self):
        """提取关键功能"""
        features = []
        
        # 从描述中提取功能
        description = self.project_info.get("description", "")
        readme_desc = self.project_info.get("readme_description", "")
        
        # 简单的关键词提取
        text = f"{description} {readme_desc}"
        
        # 常见功能动词
        action_verbs = ["provides", "offers", "supports", "enables", "allows", "helps", "creates", 
                       "generates", "processes", "analyzes", "manages", "organizes", "transforms"]
        
        for verb in action_verbs:
            pattern = rf'{verb}\s+([^.,;!?]+)'
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                features.append(f"{verb} {match.strip()}")
        
        # 去重
        features = list(set(features))
        
        # 限制数量
        self.project_info["key_features"] = features[:10]

def main():
    parser = argparse.ArgumentParser(description="分析GitHub项目并提取Skill转换所需信息")
    parser.add_argument("github_url", help="GitHub项目URL")
    parser.add_argument("--token", help="GitHub API令牌（可选）")
    parser.add_argument("--output", "-o", help="输出JSON文件路径")
    
    args = parser.parse_args()
    
    try:
        analyzer = GitHubAnalyzer(args.github_url, args.token)
        project_info = analyzer.analyze()
        
        # 输出结果
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(project_info, f, indent=2, ensure_ascii=False)
            print(f"结果已保存到: {args.output}")
        else:
            print(json.dumps(project_info, indent=2, ensure_ascii=False))
        
        return 0
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())