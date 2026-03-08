# Career KB 简历生成规则
# Resume Generation Rules

> 基于 LaTeX 模板和多次迭代优化总结的最佳实践

---

## 1. 内容约束规则

### 1.1 Summary（个人总结）
- **长度**: 3-5 句话，一段式，不换行
- **结构**: 身份定位 + 核心经验 + 关键技能 + 成就亮点
- **禁止**: 签证信息、工作权利、过于详细的个人背景
- **必须包含**: 毕业时间（精确到月）、经验年限、核心专长

**模板**:
```
Senior Android Developer with [X]+ years of experience building enterprise mobile and backend systems. 
Currently completing [Degree] at [University] (graduating [Month Year]). 
Proven expertise in [核心技术栈], and [关键能力]. 
Track record of [量化成就].
```

### 1.2 Key Skills（技能）
- **分类**: 7-8 个类别，每类一行
- **排序**: 按重要性排序，核心技能在前
- **格式**: `类别: 技能1, 技能2, 技能3`
- **禁止**: 过于细分的子类别、不相关的技能

**标准分类**:
1. Programming（编程语言）
2. AI / ML（人工智能）
3. AI Coding Tools（AI工具）
4. Full-Stack（全栈技术）
5. DevOps & Cloud（运维云）
6. Databases（数据库）
7. IoT Integration（物联网）

### 1.3 Experience（工作经历）
- **项目数量**: 4-5 个核心项目
- **每个项目**:
  - 标题行: 项目名称 + 公司 + 时间
  - 角色描述: 1 句话概括职责
  -  bullet points: 3-4 条，动词开头，量化结果
- **动词**: Built, Developed, Architected, Led, Improved, Optimized, Integrated
- **量化**: 数字、百分比、时间指标

**禁止**:
- 超过 5 个项目
- 每个项目超过 4 个 bullet points
- 无意义的描述（如 "Participated in meetings"）

### 1.4 Education（教育）
- **条目**: 2 个（硕士 + 本科）
- **每行**: 学位 + 学校 + 时间
- **细节**: 1 句话补充（论文主题、奖学金等）

### 1.5 Licenses & Certifications（证书）
- **格式**: 居左对齐，无圆点
- **每行**: 证书名称 — 颁发机构 + 年份（右对齐）
- **数量**: 4-6 个核心证书

---

## 2. 格式约束规则

### 2.1 视觉层次
```
姓名 (24pt, 加粗, 居中, 深蓝色)
  ↓
联系信息 (10.5pt, 居中, 可点击链接)
  ↓
分隔线 (1.5pt, 深蓝色)
  ↓
章节标题 (12pt, 加粗, 左对齐, 带下划线)
  ↓
正文 (10-10.5pt, 左对齐)
```

### 2.2 颜色规范
| 元素 | 颜色 | 用途 |
|------|------|------|
| 姓名/标题 | #000080 (深蓝) | 突出重要信息 |
| 链接 | #000080 | 邮箱、LinkedIn、GitHub |
| 正文 | #000 (黑色) | 主要内容 |
| 日期 | #999 (浅灰) | 时间信息 |
| 分隔线 | #000080 | 章节分隔 |

### 2.3 间距规范
- 页边距: 15mm
- 章节间距: 12px
- 段落间距: 6-8px
- 行高: 1.35-1.4

### 2.4 图标使用
- LinkedIn: 蓝色图标 + 链接
- GitHub: 黑色图标 + 链接
- 联系信息: 使用符号 (✉, ✆, ✈) 或文字

---

## 3. 内容质量规则

### 3.1 量化原则
每个 bullet point 尽可能包含数字:
- 用户规模: "10,000+ DAU"
- 性能指标: "<200ms latency"
- 效率提升: "30%+ improvement"
- 可用性: "99.9% uptime"
- 时间: "6 months early"

### 3.2 动词开头
- ✅ Built, Developed, Architected, Led
- ✅ Improved, Optimized, Reduced, Increased
- ✅ Integrated, Deployed, Automated
- ❌ Participated, Helped, Assisted

### 3.3 技术栈融入
自然融入技术名词，而非罗列:
- ✅ "Built CI/CD pipelines with Docker, Jenkins, Nginx"
- ❌ "Skills: Docker, Jenkins, Nginx"

### 3.4 主次分明
- **主要**: Android, Java Backend（详细描述）
- **次要**: AI/ML, DevOps（简要提及）
- **加分项**: Security, Reverse Engineering（一句话带过）

---

## 4. 生成检查清单

生成简历后检查:

- [ ] Summary 是一段话，3-5 句，无签证信息
- [ ] Skills 7-8 行，按重要性排序
- [ ] Experience 4-5 个项目，每项目 3-4 个 bullet points
- [ ] 每个 bullet point 动词开头
- [ ] 至少 3 个量化指标
- [ ] Education 2 个条目
- [ ] Licenses 居左，无圆点，日期右对齐
- [ ] 所有链接可点击
- [ ] 图标显示正常
- [ ] 颜色符合规范
- [ ] 无换行错误
- [ ] 一页或两页内完成

---

## 5. 自动化生成参数

```python
# PDF 设置
PAGE_SIZE = A4
MARGIN = 15mm
FONT_SIZE_NAME = 24pt
FONT_SIZE_SECTION = 12pt
FONT_SIZE_BODY = 10.5pt
FONT_SIZE_SMALL = 10pt

# 颜色
COLOR_PRIMARY = "#000080"  # 深蓝
COLOR_TEXT = "#000000"     # 黑
COLOR_DATE = "#999999"     # 浅灰
COLOR_LINK = "#000080"     # 深蓝

# 间距
SECTION_SPACING = 12
PARAGRAPH_SPACING = 6
LINE_HEIGHT = 1.35
```

---

*规则版本: 2025-03-07*
*基于 CV_Common.tex 模板优化*
