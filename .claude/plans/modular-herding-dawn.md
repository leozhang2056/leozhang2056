# Plan: Core Competencies 改为纯文本横排

## Context
用户希望 Core Competencies 从当前的表格布局改为纯文本横排（所有技能逗号分隔在同一段落，自动换行）。

## 修改文件
- `app/backend/generate_cv_from_kb.py` — `_base_template_skills_html` 函数（第 859-920 行）

## 修改内容
将 `_base_template_skills_html` 中表格渲染逻辑替换为：扁平化所有 columns 的 skills，逗号分隔，包裹在一个 `<div class="skill-row">` 中。

```python
# 修改前：表格布局
max_rows = max(len(c["items"]) for c in columns)
header_cells = ...
data_rows = ...
return f'<table class="skills-grid">...'

# 修改后：纯文本横排
all_names = []
for c in columns:
    all_names.extend(c["items"])
return f'<div class="skill-row">{", ".join(html.escape(n) for n in all_names)}</div>'
```

## 验证
1. `python generate.py cv --role android --company "Generic" --title "Senior Android Engineer"` 生成 PDF
2. 确认 Core Competencies 为纯文本逗号分隔横排
3. `python generate.py cv --role backend --company "Test" --title "Senior Engineer"` 确认 backend 也正常
