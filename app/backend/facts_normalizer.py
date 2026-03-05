#!/usr/bin/env python3
"""
Project Facts Normalizer
项目事实数据标准化工具

将各种格式的 facts.yaml 转换为统一的标准格式
"""

import yaml
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class FactsNormalizer:
    """Facts.yaml 标准化器"""
    
    def __init__(self):
        self.changes_log = []
    
    def normalize_file(self, file_path: Path) -> bool:
        """
        标准化单个 facts.yaml 文件
        
        Returns:
            是否有修改
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                data = yaml.safe_load(content)
        except Exception as e:
            print(f"❌ 读取失败 {file_path}: {e}")
            return False
        
        if not data:
            return False
        
        original_data = yaml.dump(data, sort_keys=False, allow_unicode=True)
        
        # 应用各种标准化转换
        self._normalize_metrics(data)
        self._normalize_timeline(data)
        self._normalize_highlights(data)
        self._normalize_tech_stack_groups(data)
        self._add_missing_defaults(data)
        
        new_data = yaml.dump(data, sort_keys=False, allow_unicode=True)
        
        if original_data != new_data:
            # 保留原始文件注释和格式
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(yaml.dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False))
            print(f"✓ 已标准化: {file_path.name}")
            return True
        
        return False
    
    def _normalize_metrics(self, data: Dict[str, Any]):
        """标准化 metrics 格式"""
        if "metrics" not in data:
            return
        
        metrics = data["metrics"]
        if not isinstance(metrics, list):
            return
        
        new_metrics = []
        for item in metrics:
            if isinstance(item, dict):
                # 检查是否已经是新格式
                if "value" in item and "label" in item:
                    new_metrics.append(item)
                else:
                    # 转换旧格式
                    # 旧格式: {metric: "5+", unit: "factory sites", description: "..."}
                    # 或: {metric: "30%+", description: "..."}
                    old_metric = item.get("metric", "")
                    unit = item.get("unit", "")
                    description = item.get("description", "")
                    
                    # 提取 value 和 label
                    if old_metric:
                        # 尝试分离数值和单位
                        match = re.match(r'^([0-9.]+%?|\d+)\s*(.*)$', str(old_metric))
                        if match:
                            value = match.group(1)
                            label_from_metric = match.group(2).strip()
                        else:
                            value = old_metric
                            label_from_metric = ""
                        
                        new_item = {
                            "value": value,
                            "label": label_from_metric or unit or "metric",
                            "description": description,
                        }
                        
                        if unit and label_from_metric != unit:
                            new_item["unit"] = unit
                        
                        new_metrics.append(new_item)
        
        data["metrics"] = new_metrics
    
    def _normalize_timeline(self, data: Dict[str, Any]):
        """标准化 timeline，填充缺失的日期"""
        if "timeline" not in data:
            data["timeline"] = {}
        
        timeline = data["timeline"]
        
        # 如果 start 或 end 为空，使用默认值
        if not timeline.get("start"):
            timeline["start"] = "TBD"
        
        if not timeline.get("end"):
            timeline["end"] = "TBD"
    
    def _normalize_highlights(self, data: Dict[str, Any]):
        """确保 highlights 存在"""
        if "highlights" not in data or not data["highlights"]:
            # 从 summary 生成 highlights
            summary = data.get("summary", "")
            if summary:
                # 简单的启发式提取
                sentences = [s.strip() for s in summary.split('.') if len(s.strip()) > 20]
                data["highlights"] = sentences[:5] if sentences else ["Project highlights to be added"]
            else:
                data["highlights"] = ["Project highlights to be added"]
    
    def _normalize_tech_stack_groups(self, data: Dict[str, Any]):
        """标准化 tech_stack 分组名称"""
        if "tech_stack" not in data:
            return
        
        tech_stack = data["tech_stack"]
        
        # 分组名称映射
        group_mapping = {
            "android": "mobile",
            "mobile": "mobile",
            "computer_vision": "ai_ml",
            "face_recognition": "ai_ml",
            "data_processing": "backend",
            "mlops": "devops",
            "infrastructure": "devops",
            "deployment": "devops",
            "protocols": "iot",
            "iot_protocols": "iot",
            "gateway": "iot",
            "android_gateway": "iot",
            "embedded": "iot",
            "hardware": "iot",
            "sensors": "iot",
            "gis": "domain",
            "platform": "platforms",
            "push_notification": "backend",
            "access_control": "domain",
            "integration": "domain",
            "robotics": "domain",
            "ai": "ai_ml",
        }
        
        new_tech_stack = {}
        for key, value in tech_stack.items():
            new_key = group_mapping.get(key, key)
            if new_key in new_tech_stack:
                # 合并重复的组
                if isinstance(new_tech_stack[new_key], list) and isinstance(value, list):
                    new_tech_stack[new_key] = list(set(new_tech_stack[new_key] + value))
            else:
                new_tech_stack[new_key] = value
        
        data["tech_stack"] = new_tech_stack
    
    def _add_missing_defaults(self, data: Dict[str, Any]):
        """添加缺失的默认字段"""
        # 确保 last_updated 存在
        if "last_updated" not in data:
            data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        
        # 确保 keywords 存在
        if "keywords" not in data or not data["keywords"]:
            # 从 tech_stack 和 category 生成关键词
            keywords = set()
            
            if "category" in data:
                keywords.update(data["category"])
            
            if "tech_stack" in data:
                for group, items in data["tech_stack"].items():
                    if isinstance(items, list):
                        keywords.update(items)
            
            data["keywords"] = sorted(list(keywords))[:20]  # 限制数量
        
        # 确保 related_to_roles 存在
        if "related_to_roles" not in data:
            data["related_to_roles"] = []
        
        # 确保 skills_demonstrated 存在
        if "skills_demonstrated" not in data:
            data["skills_demonstrated"] = {"technical": []}


def normalize_all_projects(projects_dir: Path):
    """标准化所有项目的 facts.yaml"""
    normalizer = FactsNormalizer()
    modified_count = 0
    
    print("=" * 60)
    print("Project Facts Normalizer")
    print("=" * 60)
    
    for project_dir in sorted(projects_dir.iterdir()):
        if not project_dir.is_dir():
            continue
        
        facts_file = project_dir / "facts.yaml"
        if not facts_file.exists():
            print(f"⚠️  跳过 {project_dir.name}: 缺少 facts.yaml")
            continue
        
        if normalizer.normalize_file(facts_file):
            modified_count += 1
    
    print("=" * 60)
    print(f"标准化完成: {modified_count} 个文件已修改")
    print("=" * 60)


if __name__ == "__main__":
    projects_dir = Path(__file__).parent.parent.parent / "projects"
    normalize_all_projects(projects_dir)
