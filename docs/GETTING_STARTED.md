# 快速开始指南

## 安装

### 从源码安装
```bash
git clone https://github.com/Aoye-3/Everything-Skill.git
cd Everything-Skill
```

### 安装依赖
```bash
pip install -r requirements.txt
```

## 基本使用

### 转换GitHub项目
```bash
python scripts/everything-skill.py https://github.com/example/repo --output ./skills
```

### 转换本地文件夹
```bash
python scripts/everything-skill.py ./my-docs --output ./skills --type folder
```

## 更多资源
- 查看 [examples/](examples/) 目录获取更多示例
- 参考 [SKILL.md](SKILL.md) 获取完整文档
