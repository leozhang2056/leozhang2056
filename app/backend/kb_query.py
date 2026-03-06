#!/usr/bin/env python3
"""
Knowledge Base Query Tool
知识库查询工具

用于 AI 快速检索和匹配知识库内容
"""

import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ProjectMatch:
    """项目匹配结果"""
    project_id: str
    name: str
    relevance_score: float
    matched_keywords: List[str]
    highlights: List[str]


class KBQuery:
    """知识库查询器"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path(__file__).parent.parent.parent
        self.projects_dir = self.base_path / "projects"
        self.kb_dir = self.base_path / "kb"
        self._cache = {}
    
    def load_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """加载单个项目数据"""
        if project_id in self._cache:
            return self._cache[project_id]
        
        facts_file = self.projects_dir / project_id / "facts.yaml"
        if not facts_file.exists():
            return None
        
        try:
            with open(facts_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                self._cache[project_id] = data
                return data
        except Exception:
            return None
    
    def load_all_projects(self) -> Dict[str, Dict[str, Any]]:
        """加载所有项目数据"""
        projects = {}
        for project_dir in self.projects_dir.iterdir():
            if project_dir.is_dir():
                project_id = project_dir.name
                data = self.load_project(project_id)
                if data:
                    projects[project_id] = data
        return projects
    
    def load_bullets(self, category: str = None) -> List[Dict[str, Any]]:
        """加载要点库"""
        bullets = []
        bullets_dir = self.kb_dir / "bullets"
        
        if not bullets_dir.exists():
            return bullets
        
        for bullet_file in bullets_dir.glob("*.yaml"):
            try:
                with open(bullet_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'bullets' in data:
                        for bullet in data['bullets']:
                            if category is None or bullet.get('category') == category:
                                bullets.append(bullet)
            except Exception:
                continue
        
        return bullets
    
    def search_projects_by_keywords(self, keywords: List[str]) -> List[ProjectMatch]:
        """根据关键词搜索项目"""
        projects = self.load_all_projects()
        matches = []
        
        for project_id, data in projects.items():
            score = 0
            matched = []
            
            # 检查 keywords 字段
            project_keywords = [k.lower() for k in data.get('keywords', [])]
            for kw in keywords:
                kw_lower = kw.lower()
                if kw_lower in project_keywords:
                    score += 1
                    matched.append(kw)
            
            # 检查 related_to_roles
            roles = [r.lower() for r in data.get('related_to_roles', [])]
            for kw in keywords:
                kw_lower = kw.lower()
                if any(kw_lower in r for r in roles):
                    score += 0.5
                    if kw not in matched:
                        matched.append(kw)
            
            # 检查 tech_stack
            tech_stack = data.get('tech_stack', {})
            all_techs = []
            for tech_list in tech_stack.values():
                if isinstance(tech_list, list):
                    all_techs.extend([t.lower() for t in tech_list])
            
            for kw in keywords:
                kw_lower = kw.lower()
                if any(kw_lower in t for t in all_techs):
                    score += 0.8
                    if kw not in matched:
                        matched.append(kw)
            
            if score > 0:
                matches.append(ProjectMatch(
                    project_id=project_id,
                    name=data.get('name', project_id),
                    relevance_score=score,
                    matched_keywords=matched,
                    highlights=data.get('highlights', [])[:3]
                ))
        
        # 按相关度排序
        matches.sort(key=lambda x: x.relevance_score, reverse=True)
        return matches
    
    def search_bullets_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        """根据标签搜索要点"""
        bullets = self.load_bullets()
        matches = []
        
        for bullet in bullets:
            bullet_tags = [t.lower() for t in bullet.get('tags', [])]
            score = 0
            
            for tag in tags:
                tag_lower = tag.lower()
                if tag_lower in bullet_tags:
                    score += 1
            
            if score > 0:
                bullet['_match_score'] = score
                matches.append(bullet)
        
        matches.sort(key=lambda x: x.get('_match_score', 0), reverse=True)
        return matches
    
    def get_project_relations(self, project_id: str) -> List[Dict[str, Any]]:
        """获取项目关联关系"""
        relations_file = self.kb_dir / "project_relations.yaml"
        if not relations_file.exists():
            return []
        
        try:
            with open(relations_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                relations = data.get('relations', [])
                
                # 找到与该项目相关的所有关系
                related = []
                for rel in relations:
                    if rel.get('from') == project_id or rel.get('to') == project_id:
                        related.append(rel)
                
                return related
        except Exception:
            return []
    
    def get_skill_matrix(self) -> Dict[str, Any]:
        """获取技能矩阵"""
        relations_file = self.kb_dir / "project_relations.yaml"
        if not relations_file.exists():
            return {}
        
        try:
            with open(relations_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data.get('skill_matrix', {})
        except Exception:
            return {}


def main():
    """命令行查询工具"""
    import sys
    
    query = KBQuery()
    
    print("=" * 60)
    print("Knowledge Base Query Tool")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python kb_query.py projects                    # List all projects")
        print("  python kb_query.py search <keyword1> <keyword2> ...  # Search by keywords")
        print("  python kb_query.py bullets <tag1> <tag2> ...   # Search bullets by tags")
        print("  python kb_query.py relations <project_id>      # Get project relations")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "projects":
        projects = query.load_all_projects()
        print(f"\nTotal Projects: {len(projects)}")
        for pid, data in sorted(projects.items()):
            print(f"  - {pid}: {data.get('name', 'N/A')}")
    
    elif cmd == "search" and len(sys.argv) > 2:
        keywords = sys.argv[2:]
        print(f"\nSearching for: {keywords}")
        matches = query.search_projects_by_keywords(keywords)
        print(f"\nFound {len(matches)} matching projects:")
        for match in matches[:5]:
            print(f"\n  [{match.relevance_score:.1f}] {match.name}")
            print(f"       Matched: {', '.join(match.matched_keywords)}")
            print(f"       Highlights:")
            for h in match.highlights[:2]:
                print(f"         - {h[:80]}...")
    
    elif cmd == "bullets" and len(sys.argv) > 2:
        tags = sys.argv[2:]
        print(f"\nSearching bullets for tags: {tags}")
        matches = query.search_bullets_by_tags(tags)
        print(f"\nFound {len(matches)} matching bullets:")
        for bullet in matches[:5]:
            print(f"\n  [{bullet.get('_match_score', 0)}] {bullet.get('id', 'N/A')}")
            print(f"       Original: {bullet.get('original', 'N/A')[:80]}...")
    
    elif cmd == "relations" and len(sys.argv) > 2:
        project_id = sys.argv[2]
        print(f"\nRelations for: {project_id}")
        relations = query.get_project_relations(project_id)
        print(f"\nFound {len(relations)} relations:")
        for rel in relations:
            print(f"  {rel.get('from')} -> {rel.get('to')}")
            print(f"    Type: {rel.get('type')}")
            print(f"    Description: {rel.get('description', 'N/A')}")
    
    else:
        print("Unknown command. Use: projects, search, bullets, relations")


if __name__ == "__main__":
    main()
