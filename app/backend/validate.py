#!/usr/bin/env python3
"""
简单的 facts.yaml 验证脚本
"""

import yaml
from pathlib import Path

def validate_facts(file_path: Path) -> list:
    """验证单个 facts.yaml 文件"""
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"YAML 解析错误: {e}"]
    
    if not data:
        return ["文件为空"]
    
    # 必需字段
    required = ["project_id", "name", "type", "timeline", "role", 
                "summary", "highlights", "tech_stack", "keywords", "last_updated",
                "skills_demonstrated", "related_to_roles"]
    
    for field in required:
        if field not in data:
            errors.append(f"缺少必需字段: {field}")
    
    # 验证 timeline
    if "timeline" in data:
        timeline = data["timeline"]
        if not timeline.get("start"):
            errors.append("timeline.start 为空")
        if not timeline.get("end"):
            errors.append("timeline.end 为空")
    
    # 验证 metrics 格式
    if "metrics" in data and isinstance(data["metrics"], list):
        for i, m in enumerate(data["metrics"]):
            if isinstance(m, dict):
                if "value" not in m:
                    errors.append(f"metrics[{i}] 缺少 value")
                if "label" not in m:
                    errors.append(f"metrics[{i}] 缺少 label")
    
    return errors


def main():
    projects_dir = Path(__file__).parent.parent.parent / "projects"
    
    print("=" * 60)
    print("Facts.yaml 验证结果")
    print("=" * 60)
    
    all_pass = True
    for project_dir in sorted(projects_dir.iterdir()):
        if not project_dir.is_dir():
            continue
        
        facts_file = project_dir / "facts.yaml"
        if not facts_file.exists():
            print(f"\n⚠️  {project_dir.name}: 缺少 facts.yaml")
            all_pass = False
            continue
        
        errors = validate_facts(facts_file)
        if errors:
            print(f"\n❌ {project_dir.name}:")
            for e in errors:
                print(f"   - {e}")
            all_pass = False
        else:
            print(f"✓ {project_dir.name}")
    
    print("\n" + "=" * 60)
    if all_pass:
        print("✅ 所有项目验证通过！")
    else:
        print("❌ 存在验证错误")
    print("=" * 60)


if __name__ == "__main__":
    main()
