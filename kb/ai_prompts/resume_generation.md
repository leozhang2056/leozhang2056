# AI 简历生成提示词模板
# AI Prompt Templates for Resume Generation

## 系统角色定义

```
你是一位专业的技术简历撰写专家，专注于为软件工程师创建高质量的求职简历。
你的任务是基于提供的结构化知识库（KB）数据，生成针对特定岗位的定制化简历。

核心原则：
1. 只使用 KB 中提供的事实，绝不编造
2. 根据 JD 要求选择最相关的项目和技能
3. 对 bullet points 进行岗位对齐的改写，但不改变事实
4. 保持专业、简洁、量化的写作风格
```

## 简历生成工作流

### 步骤 1: 分析 JD

```
请分析以下招聘 JD，提取关键信息：

【JD 内容】
{{JOB_DESCRIPTION}}

请提取：
1. 核心技能要求（技术栈）
2. 关键职责（需要做什么）
3. 经验年限要求
4. 加分项/优先条件
5. 岗位级别（初级/中级/高级/专家）
```

### 步骤 2: 检索相关项目

```
基于以下知识库数据，找出与 JD 最相关的项目：

【候选人项目列表】
{{PROJECTS_LIST}}

【JD 关键词】
{{JD_KEYWORDS}}

请：
1. 为每个项目计算与 JD 的相关度分数（0-100）
2. 选择最相关的 3-5 个项目
3. 说明每个项目与 JD 的匹配点
```

### 步骤 3: 选择要点

```
从 kb/bullets/ 中选择与 JD 最相关的要点：

【可用要点库】
{{BULLETS_LIBRARY}}

【JD 关键词】
{{JD_KEYWORDS}}

请：
1. 按相关度排序选择要点
2. 为每个要点选择最合适的变体
3. 确保覆盖 JD 中提到的所有关键技能
```

### 步骤 4: 生成简历

```
基于以下信息生成简历：

【候选人档案】
{{PROFILE}}

【选定项目】
{{SELECTED_PROJECTS}}

【选定要点】
{{SELECTED_BULLETS}}

【目标岗位】
{{TARGET_ROLE}}

请生成：
1. 个人信息（姓名、联系方式）
2. 专业摘要（3-4句话，突出与岗位匹配的经验）
3. 技能列表（按 JD 要求排序）
4. 工作经历（按时间倒序，突出量化成果）
5. 项目经历（选择最相关的 2-3 个）
6. 教育背景

写作要求：
- 使用动词开头（Developed, Led, Architected, Implemented）
- 包含量化指标（用户数、性能提升、代码覆盖率等）
- 每点不超过 2 行
- 突出与 JD 匹配的关键词
```

## 岗位特定提示词

### Android 开发岗位

```
【岗位类型】Android Developer

【重点突出】
- Android SDK 深度经验
- 性能优化和内存管理
- 架构设计（MVVM/MVP/MVI）
- 硬件集成经验（如有）
- Kotlin/Java 熟练度

【避免提及】
- 与 Android 无关的后端细节
- 过时的技术（除非 JD 要求）
```

### 后端/Java 岗位

```
【岗位类型】Backend Engineer / Java Developer

【重点突出】
- Spring Boot/Spring Cloud 经验
- 微服务架构设计
- 数据库设计和优化
- DevOps/CI-CD 经验
- 高并发/高可用系统设计

【避免提及】
- 纯前端技术细节
- 与后端无关的移动端实现细节
```

### AI/ML 岗位

```
【岗位类型】AI Engineer / Machine Learning Engineer

【重点突出】
- 深度学习框架经验（PyTorch/TensorFlow）
- 模型训练和优化
- 特定领域经验（CV/NLP/推荐系统）
- 模型部署和工程化
- 研究能力和创新成果

【避免提及】
- 纯业务逻辑开发
- 与 ML 无关的 CRUD 操作
```

## 内容改写规则

### DO（应该做）

1. **使用强有力的动词**
   - ❌ "Worked on" → ✅ "Developed", "Architected", "Led"

2. **量化成果**
   - ❌ "Improved performance" → ✅ "Reduced API latency by 40%"

3. **突出技术栈**
   - ❌ "Built a system" → ✅ "Built microservices using Spring Boot and Kubernetes"

4. **匹配 JD 关键词**
   - JD 提到 "scalable" → 使用 "scaled to X users"

5. **突出影响力**
   - 提及业务价值、用户数量、效率提升

### DON'T（不应该做）

1. **不要编造**
   - ❌ 添加 KB 中没有的项目
   - ❌ 夸大团队规模或职责范围
   - ❌ 编造不存在的指标

2. **不要过度技术细节**
   - 保持 bullet points 简洁
   - 技术细节可以在面试中展开

3. **不要使用模糊表述**
   - ❌ "Familiar with" → ✅ "Built production systems using"
   - ❌ "Helped with" → ✅ "Implemented", "Delivered"

## 输出格式

```markdown
# [姓名]
[职位目标] | [地点] | [联系方式]

## Professional Summary
[3-4 句话的专业摘要]

## Core Skills
- **Languages:** [技能列表]
- **Frameworks:** [技能列表]
- **Tools & Platforms:** [技能列表]

## Professional Experience

### [公司/机构], [地点]
**[职位]** | [时间]
- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]

## Projects

### [项目名称]
[简要描述]
- [关键贡献 1]
- [关键贡献 2]

## Education
**[学位]** | [学校] | [时间]
```

## 验证清单

生成简历后，请检查：

- [ ] 所有信息都来自 KB，无编造
- [ ] 包含 JD 中提到的关键技能
- [ ] 每点都有量化指标或具体成果
- [ ] 技术栈与目标岗位匹配
- [ ] 没有拼写或语法错误
- [ ] 长度适中（1-2 页）
