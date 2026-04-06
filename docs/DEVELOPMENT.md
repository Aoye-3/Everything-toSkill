# 开发指南

## 项目结构

```
Everything-Skill/
├── scripts/                    # 核心脚本
│   ├── everything-skill.py     # 主执行脚本
│   ├── analyze-github.py       # GitHub项目分析
│   ├── analyze-folder.py       # 本地文件夹分析
│   ├── generate-skill-v2.py    # 改进版Skill生成
│   └── templates/              # 模板目录
├── config/                     # 配置文件
├── examples/                   # 使用示例
├── docs/                       # 文档
├── tests/                      # 测试文件
├── SKILL.md                    # 主技能文档
├── README.md                   # 项目说明
├── LICENSE                     # 开源协议
└── .gitignore                  # Git忽略文件
```

## 开发环境设置

1. 克隆仓库
2. 创建虚拟环境
3. 安装开发依赖
4. 运行测试

## 测试
```bash
python scripts/test-everything-skill.py
```

## 贡献指南
1. Fork仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request
