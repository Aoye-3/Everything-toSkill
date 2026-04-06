---
name: everything-skill
description: Convert GitHub projects or local document folders into usable Skills. Use when user has a GitHub repository or local folder with valuable content that should be transformed into an AI-accessible Skill for easier integration and usage within the IDE.
---

# EverythingSkill

Transform any GitHub project or local document folder into a fully functional Skill that AI agents can understand and use.

## Overview

EverythingSkill automates the process of converting existing codebases and documentation into structured Skills that can be invoked by AI agents within the IDE. It analyzes project structure, extracts key information, and generates a complete Skill directory with appropriate documentation, scripts, and configuration.

## Design Philosophy

### Core Principle: Augment, Not Replace (增强而非替代)
EverythingSkill is built on the fundamental belief that AI should **augment human capabilities**, not replace humans. The Skills we create are not meant to displace developers, document authors, or knowledge workers, but to:

1. **Enhance Productivity**: Delegate repetitive, pattern-based tasks to AI, allowing humans to focus on creative work
2. **Extend Personal Capabilities**: Transform personal knowledge and experience into reusable AI abilities
3. **Preserve Team Wisdom**: Prevent knowledge loss and ensure team continuity
4. **Accelerate Learning**: Provide new members with instant access to knowledge and guidance

**核心理念**: AI应该增强人类的能力，而不是替代人类。我们创建的Skills不是为了取代开发者、文档作者或知识工作者，而是为了增强工作效率、扩展个人能力、保存团队智慧和加速学习过程。

### Self-Directed Transformation: Control Your Own Knowledge (自主转换)
"与其被人做成Skill，不如自己来转换一些可以帮助自己的内容被自己使用" - This philosophy is embodied in:

1. **Autonomy**: Developers can independently decide which projects to convert into Skills
2. **Control**: Complete control over the conversion process, content, and quality
3. **Personalization**: Customize Skills according to personal or team needs
4. **Iterative Optimization**: Continuously improve and optimize your Skills library

**自主转换理念**: 开发者可以自主决定将哪些项目转化为Skills，完全控制转换过程、内容和质量，根据个人或团队需求定制Skills，持续改进和优化自己的Skills库。自主转换的核心是让开发者自己掌控自己的知识。

### Inspiration from Colleague-Skill
The colleague-skill project demonstrates how to transform "cold farewells" into "warm skills" - a concept that deeply influenced EverythingSkill's design:

1. **Emotional Connection**: Technical tools can have emotional value, helping teams stay connected
2. **Knowledge Transmission**: Ensure valuable knowledge doesn't disappear with personnel changes
3. **Continuous Availability**: Allow departed colleagues' wisdom to continue serving the team
4. **Human-Centered Design**: Technology should serve human needs, not the other way around

### Practical Application of OpenAI Guidelines
Following OpenAI's SKILL creation guidelines is not just about technical compliance, but about:

1. **Efficient Collaboration**: Ensure Skills can be effectively understood and used by AI agents
2. **Resource Optimization**: Make judicious use of the precious context window resource
3. **Quality Assurance**: Adhere to industry best practices to create high-quality Skills
4. **Maintainability**: Create Skill structures that are easy to maintain and update

## Quick Start

### Convert a GitHub Project

```bash
# Convert a GitHub repository to a Skill
python scripts/everything-skill.py https://github.com/username/repository --output ./generated-skills

# With GitHub API token (for private repos or rate limiting)
python scripts/everything-skill.py https://github.com/username/repository --token YOUR_GITHUB_TOKEN --output ./generated-skills
```

### Convert a Local Folder

```bash
# Convert a local folder to a Skill
python scripts/everything-skill.py /path/to/your/folder --output ./generated-skills
```

### Manual Analysis and Generation

```bash
# Step 1: Analyze a GitHub project
python scripts/analyze-github.py https://github.com/username/repository --output analysis.json

# Step 2: Analyze a local folder
python scripts/analyze-folder.py /path/to/folder --output analysis.json

# Step 3: Generate Skill from analysis
python scripts/generate-skill.py analysis.json --output ./generated-skills
```

## Features

### Automatic Analysis
- **GitHub Project Analysis**: Extracts repository metadata, README content, file structure, and key features
- **Local Folder Analysis**: Scans directory structure, file types, and documentation content
- **Project Type Detection**: Automatically identifies project type (tool, resource, application, framework, colleague-skill)
- **Key Feature Extraction**: Identifies and extracts core functionality from documentation
- **OpenAI Compliance Check**: Validates generated Skills against OpenAI SKILL guidelines

### Smart Skill Generation
- **Template-Based Generation**: Uses appropriate templates based on project type
- **Automatic Documentation**: Generates comprehensive SKILL.md with usage examples
- **Directory Structure**: Creates complete Skill directory with scripts, config, and assets
- **Configuration Files**: Generates appropriate configuration templates
- **Progressive Disclosure**: Implements OpenAI's progressive disclosure patterns
- **Context Optimization**: Keeps SKILL.md concise, moves details to references/

### Project Type Support
- **Tool Projects**: Command-line tools, libraries, SDKs (uses tool-template.md)
- **Resource Projects**: Documentation collections, code examples, design resources (uses resource-template.md)
- **Application Projects**: Web apps, desktop applications, services
- **Framework Projects**: Development frameworks, boilerplates
- **Colleague-Skill Projects**: Transform colleague knowledge into AI skills (uses colleague-skill-template.md)
- **OpenAI-Compliant Projects**: Follows OpenAI SKILL creation guidelines (uses openai-compliant-template.md)

## Best Practices (Based on OpenAI Guidelines)

### Core Principles
1. **Conciseness is Key**: The context window is a shared resource. Only add information that AI doesn't already know.
2. **Appropriate Degrees of Freedom**:
   - **High freedom**: Text-based instructions for flexible tasks
   - **Medium freedom**: Pseudocode or parameterized scripts
   - **Low freedom**: Specific scripts for fragile operations
3. **Progressive Disclosure**: Three-level loading system:
   - Metadata (name + description) - Always in context
   - SKILL.md body - When skill triggers
   - Bundled resources - As needed by AI

### Skill Structure Compliance
- **Required**: SKILL.md with YAML frontmatter (name + description)
- **Recommended**: agents/openai.yaml for UI metadata
- **Optional**: scripts/, references/, assets/ directories
- **Avoid**: README.md, INSTALLATION_GUIDE.md, etc. (only include AI-needed files)

### From Colleague-Skill Project Insights
1. **Knowledge Transformation**: Convert human expertise into AI-accessible skills
2. **Structured Data**: Use meta.json, persona.md, work.md for colleague data
3. **Multi-language Support**: Include multiple language READMEs when applicable
4. **Practical Scenarios**: Focus on real-world use cases like knowledge preservation

## Detailed Usage

### GitHub Project Conversion

1. **Provide GitHub URL**: Point to any public GitHub repository
2. **Optional Authentication**: Use GitHub token for private repos or higher rate limits
3. **Output Location**: Specify where to save the generated Skill
4. **Automatic Processing**: The tool analyzes and generates everything automatically

Example with detailed output:
```bash
python scripts/everything-skill.py https://github.com/markdown/formatter \
  --output ./my-skills \
  --token ghp_your_token_here
```

### Local Folder Conversion

1. **Provide Folder Path**: Point to any local directory
2. **Content Analysis**: The tool scans and analyzes all files
3. **Skill Generation**: Creates Skill based on folder content
4. **Original Content Preservation**: Copies original files to assets/original-content

Example:
```bash
python scripts/everything-skill.py ./my-documentation-project \
  --output ./generated-skills \
  --type folder
```

### Customization Options

#### Analysis Customization
```bash
# Limit API calls (GitHub)
python scripts/analyze-github.py https://github.com/user/repo --token YOUR_TOKEN --depth 2

# Exclude certain directories (local)
# Modify analyze-folder.py to customize exclusion patterns
```

#### Generation Customization
```bash
# Use custom template
python scripts/generate-skill.py analysis.json --template ./custom-template.md

# Override project type
# Edit the analysis.json file before generation
```

## Generated Skill Structure

A typical generated Skill includes:

```
generated-skill-name/
├── SKILL.md                    # Main Skill documentation
├── scripts/                    # Execution scripts
│   ├── run-tool.py            # Main execution script (for tools)
│   ├── browse-resources.py    # Resource browser (for resources)
│   └── setup.py               # Setup/installation script
├── config/                     # Configuration files
│   ├── skill-config.json      # Skill metadata
│   ├── default-config.json    # Default configuration
│   └── config-template.json   # Configuration template
├── assets/                     # Resource files
│   ├── original-content/      # Original project files (for folders)
│   └── resources/             # Additional resources
├── examples/                   # Usage examples
│   ├── basic-usage.md
│   ├── advanced-features.md
│   └── integration-examples.md
└── README-SKILL.md            # Additional Skill documentation
```

## Templates

EverythingSkill uses intelligent templates based on project type:

### Tool Projects (`tool-template.md`)
- Command-line interface documentation
- Installation and setup instructions
- Usage examples and API reference
- Configuration options

### Resource Projects (`resource-template.md`)
- Resource catalog and indexing
- Search and browsing functionality
- Usage guidelines
- Contribution instructions

### Application Projects
- Deployment instructions
- Configuration guides
- API documentation
- User guides

### Framework Projects
- Setup and initialization
- Architecture overview
- Best practices
- Extension guides

## Configuration

### GitHub API Configuration
For GitHub projects, you may need a personal access token:
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with `repo` scope
3. Use the token with `--token` parameter

### Analysis Configuration
Modify these scripts to customize analysis:
- `scripts/analyze-github.py`: GitHub-specific analysis
- `scripts/analyze-folder.py`: Local folder analysis
- `scripts/templates/`: Template files for different project types

### Generation Configuration
Edit `scripts/generate-skill.py` to:
- Change default directory structure
- Modify template selection logic
- Customize content generation

## Examples

### Example 1: Convert a Markdown Formatter
```bash
# Convert a markdown formatting tool
python scripts/everything-skill.py https://github.com/example/markdown-formatter --output ./skills

# Result: Creates ./skills/markdown-formatter/ with:
# - SKILL.md explaining how to format markdown
# - Scripts to run the formatter
# - Configuration templates
# - Usage examples
```

### Example 2: Convert Documentation Folder
```bash
# Convert a local documentation folder
python scripts/everything-skill.py ./api-docs --output ./skills

# Result: Creates ./skills/api-docs/ with:
# - SKILL.md for accessing API documentation
# - Search scripts for finding documentation
# - Original docs in assets/original-content/
# - Usage examples for common queries
```

### Example 3: Convert a CLI Tool
```bash
# Convert a command-line utility
python scripts/everything-skill.py https://github.com/example/cli-tool --output ./skills

# Result: Creates ./skills/cli-tool/ with:
# - SKILL.md with command reference
# - Wrapper scripts for common operations
# - Configuration examples
# - Integration examples
```

## Best Practices

### Before Conversion
1. **Clean Up**: Ensure the project has a clear README and structure
2. **Documentation**: Good documentation leads to better Skill generation
3. **Organization**: Well-organized projects convert more effectively

### After Conversion
1. **Review**: Always review the generated Skill for accuracy
2. **Test**: Test the Skill with actual use cases
3. **Optimize**: Customize the generated Skill for your specific needs
4. **Update**: Keep the Skill updated with source project changes

### Skill Quality
1. **Clear Triggers**: Ensure the description clearly states when to use the Skill
2. **Practical Examples**: Include real, runnable examples
3. **Error Handling**: Document common errors and solutions
4. **Progressive Disclosure**: Use references for detailed information

## Troubleshooting

### Common Issues

#### GitHub Rate Limiting
**Problem**: GitHub API rate limiting without token
**Solution**: 
- Use `--token` with a GitHub personal access token
- Wait for rate limit reset (usually 1 hour)
- Use authenticated requests for higher limits

#### Permission Errors
**Problem**: Cannot access private repositories or restricted folders
**Solution**:
- Ensure proper authentication tokens
- Check filesystem permissions for local folders
- Use appropriate scope for GitHub tokens

#### Analysis Failures
**Problem**: Analysis script fails to process project
**Solution**:
- Check network connectivity for GitHub projects
- Verify folder exists and is accessible
- Check for malformed JSON or unusual file structures

#### Generation Issues
**Problem**: Generated Skill has errors or missing information
**Solution**:
- Review the analysis JSON file for completeness
- Check template files for errors
- Manually edit the generated Skill as needed

### Debugging

#### Verbose Output
```bash
# Add debug prints to scripts
# Or run with Python debug mode
python -m pdb scripts/everything-skill.py https://github.com/example/repo
```

#### Step-by-Step Execution
```bash
# Run each step separately
python scripts/analyze-github.py https://github.com/example/repo --output analysis.json
python scripts/generate-skill.py analysis.json --output ./skills
```

## Integration with IDE

### Automatic Skill Discovery
Generated Skills are placed in the standard `.trae/skills/` directory structure, making them automatically discoverable by the IDE.

### Manual Installation
To use a generated Skill:
1. Copy the generated Skill folder to `.trae/skills/`
2. Restart the IDE or reload Skills
3. The Skill will be available for AI agents to use

### Skill Testing
Test your generated Skill by:
1. Asking the AI agent to use the Skill
2. Testing the example commands
3. Verifying the expected functionality

## Limitations

### Current Limitations
1. **Complex Projects**: Very large or complex projects may require manual optimization
2. **Custom Build Systems**: Projects with unusual build systems may need manual configuration
3. **Dynamic Content**: Projects with dynamically generated content may not be fully captured
4. **Binary Files**: Analysis focuses on text files; binary files are noted but not analyzed

### Known Issues
1. **Nested Dependencies**: Deeply nested dependency structures may not be fully analyzed
2. **Non-Standard Documentation**: Projects without standard README structure may have incomplete documentation
3. **API Changes**: GitHub API changes may affect the analysis script

## Future Enhancements

### Planned Features
1. **More Project Types**: Support for additional project types
2. **Better Template System**: More flexible and customizable templates
3. **Interactive Mode**: Guided conversion with user input
4. **Batch Processing**: Convert multiple projects at once
5. **Skill Validation**: Automated testing of generated Skills

### Community Contributions
1. **Custom Templates**: Users can create and share custom templates
2. **Analysis Plugins**: Extensible analysis for specific project types
3. **Integration Plugins**: Integration with other tools and platforms

## Support

### Getting Help
1. **Documentation**: This Skill documentation
2. **Examples**: Example conversions in the `examples/` directory
3. **Templates**: Review template files for customization

### Reporting Issues
1. **GitHub Issues**: Report issues with the conversion process
2. **Feature Requests**: Suggest new features or improvements
3. **Template Improvements**: Contribute better templates for specific project types

## License and Attribution

EverythingSkill is provided as a tool to help create Skills from existing projects. Generated Skills should respect the licenses of the original projects.

### Attribution
When using generated Skills:
1. Credit the original project authors
2. Respect the original project's license
3. Provide attribution in the generated Skill documentation

### License Compliance
- Generated Skills include original project license information when available
- Users are responsible for ensuring license compliance
- Modify generated Skills as needed to meet licensing requirements

## Open Source License

EverythingSkill itself is released under the **MIT License**:

```
MIT License

Copyright (c) 2026 EverythingSkill Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Third-Party Acknowledgments

EverythingSkill acknowledges and respects the following projects and resources:

1. **OpenAI SKILL Creation Guidelines**: For establishing industry best practices
2. **colleague-skill project**: For the innovative concept of transforming human knowledge into AI skills
3. **GitHub API**: For enabling project analysis and data extraction
4. **OpenAI Models**: For following AI agent interaction best practices

### Disclaimer

1. **Not an Official Tool**: EverythingSkill is not an official OpenAI tool
2. **No Warranty**: The software is provided "as is", without warranty of any kind
3. **Limitation of Liability**: In no event shall the authors be liable for any claims or damages
4. **Compliance Responsibility**: Users are responsible for ensuring compliance with all applicable laws and regulations

### Citation

When using or referencing EverythingSkill in academic or professional work:

```
EverythingSkill: A tool for converting GitHub projects and local folders into AI-accessible Skills.
Version 1.0. MIT License. Available at: https://github.com/example/everything-skill
```

### Ethical Use

1. **Respect Original Licenses**: Always respect the licenses of projects you convert
2. **Obtain Necessary Permissions**: Ensure you have the right to convert and use content
3. **Provide Proper Attribution**: Give credit to original authors and projects
4. **Use Responsibly**: Ensure your use of generated Skills is ethical and legal

---

*EverythingSkill - Making every project accessible to AI agents*

**License**: MIT  
**Copyright**: © 2026 EverythingSkill Contributors  
**Version**: 1.0.0  
**Last Updated**: 2026-04-06