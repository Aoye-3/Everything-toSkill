# 资源类项目Skill模板

## 模板说明
此模板适用于资源类GitHub项目，如文档集合、代码示例、设计资源等。

## 核心结构

### 1. SKILL.md 结构
```markdown
---
name: "{skill_name}"
description: "{description} Use when user needs access to {resource_type} resources for {use_case}."
---

# {project_name}

{project_description}

## 资源概览

### 资源类型
- {resource_type_1}
- {resource_type_2}
- {resource_type_3}

### 资源数量
- 总计: {total_resources} 个资源
- 分类: {categories_count} 个类别
- 更新: {last_updated}

## 快速访问

### 浏览资源
```bash
# 查看所有资源
{view_command}

# 搜索特定资源
{search_command}
```

### 使用资源
```bash
# 获取单个资源
{get_command}

# 批量处理
{batch_command}
```

## 资源目录

### 按类别
{categories_list}

### 按标签
{tags_list}

### 按格式
{formats_list}

## 使用指南

### 基本使用
{basic_usage_guide}

### 高级搜索
{advanced_search_guide}

### 集成使用
{integration_guide}

## 示例

### 示例1: 查找资源
```bash
{example_find}
```

### 示例2: 使用资源
```bash
{example_use}
```

### 示例3: 贡献资源
```bash
{example_contribute}
```

## 贡献指南

### 添加新资源
{contribution_guide}

### 资源格式要求
{format_requirements}

### 质量标准
{quality_standards}

## 维护信息

### 更新频率
{update_frequency}

### 质量检查
{quality_checks}

### 版本历史
{version_history}
```

### 2. 资源目录结构
```
assets/
├── resources/                 # 资源文件
│   ├── category-1/
│   │   ├── resource-1.ext
│   │   ├── resource-2.ext
│   │   └── metadata.json
│   ├── category-2/
│   │   └── ...
│   └── index.json            # 资源索引
├── templates/                # 资源模板
│   ├── template-1.ext
│   ├── template-2.ext
│   └── README.md
└── previews/                 # 资源预览
    ├── preview-1.png
    ├── preview-2.png
    └── index.html
```

### 3. 工具脚本结构
```
scripts/
├── browse-resources.py       # 资源浏览工具
├── search-resources.py       # 资源搜索工具
├── download-resource.py      # 资源下载工具
└── update-index.py           # 索引更新工具
```

### 4. 文档结构
```
docs/
├── usage-guide.md            # 使用指南
├── contribution-guide.md     # 贡献指南
├── api-reference.md          # API参考
└── examples/                 # 示例目录
    ├── basic-usage.md
    ├── advanced-search.md
    └── integration-examples.md
```

## 填充指南

### 1. 元数据填充
- `{skill_name}`: 使用描述性名称，如 `awesome-design-resources`
- `{description}`: 描述资源类型和用途
- `{resource_type}`: 资源类型，如 "design templates", "code snippets", "documentation"
- `{use_case}`: 使用场景，如 "UI design", "API development", "learning"

### 2. 资源信息填充
- `{resource_type_1}`, `{resource_type_2}`: 具体的资源类型
- `{total_resources}`: 资源总数
- `{categories_count}`: 分类数量
- `{last_updated}`: 最后更新时间

### 3. 命令填充
- `{view_command}`: 查看资源命令
- `{search_command}`: 搜索资源命令
- `{get_command}`: 获取资源命令
- `{batch_command}`: 批量处理命令

### 4. 列表填充
- `{categories_list}`: 分类列表（Markdown格式）
- `{tags_list}`: 标签列表
- `{formats_list}`: 格式列表

### 5. 指南填充
- `{basic_usage_guide}`: 基本使用指南
- `{advanced_search_guide}`: 高级搜索指南
- `{integration_guide}`: 集成使用指南

## 最佳实践

### 1. 资源组织
- **分类清晰**: 按功能、类型、难度等分类
- **标签系统**: 使用标签方便搜索
- **元数据完整**: 每个资源包含完整元数据
- **预览可用**: 提供资源预览

### 2. 搜索功能
- **全文搜索**: 支持关键词搜索
- **过滤选项**: 按类型、标签、格式过滤
- **排序功能**: 按相关度、时间、评分排序

### 3. 使用体验
- **简单获取**: 一键获取资源
- **格式转换**: 支持多种格式
- **集成友好**: 易于集成到工作流

### 4. 质量控制
- **审核流程**: 新资源需要审核
- **质量评分**: 用户评分系统
- **定期更新**: 保持资源新鲜度

## 自动填充规则

### 从GitHub项目提取
1. **资源统计**: 分析文件结构统计资源数量
2. **分类识别**: 从目录结构识别分类
3. **格式分析**: 分析文件扩展名识别格式
4. **元数据提取**: 从README和配置文件提取元数据

### 智能推断
1. **资源类型**: 根据内容推断类型（代码、文档、设计等）
2. **使用场景**: 根据描述推断使用场景
3. **搜索关键词**: 从文件名和内容提取关键词
4. **质量指标**: 根据星标、提交频率等推断质量

## 验证标准

### 必须包含
- [ ] 完整的资源目录
- [ ] 搜索和浏览功能
- [ ] 使用示例
- [ ] 贡献指南

### 推荐包含
- [ ] 资源预览
- [ ] 格式转换工具
- [ ] 质量评分系统
- [ ] 更新通知

### 可选包含
- [ ] API接口
- [ ] 命令行工具
- [ ] 浏览器扩展
- [ ] 编辑器插件

## 示例填充

### 输入项目
- 名称: `awesome-design-md`
- 描述: `Curated collection of DESIGN.md files from popular websites`
- 内容: 58个DESIGN.md文件，按公司分类
- 结构: `design-md/`目录包含多个子目录

### 生成Skill
- Skill名称: `awesome-design-md`
- 触发条件: `Use when user needs access to design system resources for UI generation`
- 资源类型: `Design system documents, color palettes, typography rules`
- 资源数量: `58个DESIGN.md文件，40+个公司`
- 浏览命令: `python scripts/browse-designs.py`
- 搜索命令: `python scripts/search-designs.py "dark theme"`

## 特殊考虑

### 1. 大资源处理
- 分页加载
- 懒加载预览
- 增量下载

### 2. 版权问题
- 明确版权声明
- 使用许可说明
-  attribution要求

### 3. 更新维护
- 自动更新检查
- 变更日志
- 向后兼容性

### 4. 国际化
- 多语言支持
- 本地化资源
- 翻译指南

## 性能优化

### 1. 索引优化
- 构建搜索索引
- 缓存热门资源
- 预加载预览

### 2. 加载优化
- 按需加载
- 压缩传输
- CDN分发

### 3. 搜索优化
- 关键词索引
- 相关性排序
- 拼写纠正

## 扩展性设计

### 1. 插件系统
- 资源处理器插件
- 搜索插件
- 导出插件

### 2. API设计
- RESTful API
- GraphQL支持
- WebSocket实时更新

### 3. 集成接口
- 编辑器集成
- CI/CD集成
- 设计工具集成