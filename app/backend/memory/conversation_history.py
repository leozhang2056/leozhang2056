"""
Conversation History - 会话日志记录
记录每次交互的上下文，支持会话记忆和追溯
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class InteractionType(Enum):
    """交互类型"""
    CV_GENERATE = "cv_generate"
    CV_ITERATE = "cv_iterate"
    COVER_LETTER = "cover_letter"
    EMAIL = "email"
    JD_FETCH = "jd_fetch"
    INTERVIEW_QA = "interview_qa"
    MATCH = "match"
    QUERY = "query"


@dataclass
class Interaction:
    """单次交互记录"""
    id: str
    timestamp: str
    type: str
    input: Dict[str, Any]
    output: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConversationHistory:
    """
    对话历史管理器
    
    用法:
        history = ConversationHistory(repo_root)
        
        # 记录交互
        history.log(
            type=InteractionType.CV_GENERATE,
            input={"role": "android"},
            output={"pdf": "...", "projects": ["..."]},
        )
        
        # 查询历史
        recent = history.get_recent(limit=5)
    """
    
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self._log_file = self.repo_root / ".cache" / "conversation_history.json"
        self._ensure_log_file()
    
    def _ensure_log_file(self) -> None:
        """确保日志文件存在"""
        if not self._log_file.exists():
            self._log_file.parent.mkdir(parents=True, exist_ok=True)
            self._save([])
    
    def _load(self) -> List[Dict[str, Any]]:
        """加载历史记录"""
        try:
            with open(self._log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    
    def _save(self, data: List[Dict[str, Any]]) -> None:
        """保存历史记录"""
        with open(self._log_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        return f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def log(
        self,
        type: InteractionType,
        input: Dict[str, Any],
        output: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
        keep: bool = True,
    ) -> str:
        """
        记录一次交互
        
        Args:
            type: 交互类型
            input: 输入参数
            output: 输出结果
            metadata: 额外元数据
            keep: 是否持久化（False只存内存）
        
        Returns:
            交互ID
        """
        interaction = Interaction(
            id=self._generate_id(),
            timestamp=datetime.now().isoformat(),
            type=type.value,
            input=self._sanitize(input),
            output=self._sanitize(output),
            metadata=metadata or {},
        )
        
        data = self._load()
        data.append(asdict(interaction))
        
        if keep:
            self._save(data)
        
        return interaction.id
    
    def _sanitize(self, obj: Any) -> Any:
        """清理敏感数据"""
        if isinstance(obj, dict):
            return {
                k: self._sanitize(v)
                for k, v in obj.items()
                if k not in ("api_key", "token", "secret", "password")
            }
        elif isinstance(obj, list):
            return [self._sanitize(x) for x in obj]
        return obj
    
    def get_recent(
        self,
        limit: int = 10,
        type: Optional[InteractionType] = None,
    ) -> List[Dict[str, Any]]:
        """
        获取最近的交互记录
        
        Args:
            limit: 返回数量
            type: 过滤类型
        """
        data = self._load()
        
        if type:
            data = [x for x in data if x.get("type") == type.value]
        
        return data[-limit:]
    
    def get_by_id(self, interaction_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取交互记录"""
        data = self._load()
        for item in data:
            if item.get("id") == interaction_id:
                return item
        return None
    
    def search(
        self,
        keyword: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        搜索历史记录
        
        Args:
            keyword: 关键词
            limit: 返回数量
        """
        data = self._load()
        keyword = keyword.lower()
        results = []
        
        for item in data:
            # 搜索输入输出中的关键词
            input_str = json.dumps(item.get("input", {})).lower()
            output_str = json.dumps(item.get("output", {})).lower()
            
            if keyword in input_str or keyword in output_str:
                results.append(item)
        
        return results[-limit:]
    
    def get_session(self, date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取指定日期的会话记录
        
        Args:
            date: 日期 (YYYY-MM-DD)，默认今天
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        data = self._load()
        return [x for x in data if x.get("timestamp", "").startswith(date)]
    
    def clear_old(self, days: int = 30) -> int:
        """
        清理旧记录
        
        Args:
            days: 保留最近天数
        
        Returns:
            删除的记录数
        """
        from datetime import timedelta
        
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        data = self._load()
        original_count = len(data)
        
        data = [x for x in data if x.get("timestamp", "") > cutoff]
        
        self._save(data)
        return original_count - len(data)


def log_interaction(
    repo_root: Path,
    type: InteractionType,
    input: Dict[str, Any],
    output: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """
    便捷函数：记录交互
    
    用法:
        log_interaction(
            repo_root,
            type=InteractionType.CV_GENERATE,
            input={"role": "android"},
            output={"pdf": "..."},
        )
    """
    history = ConversationHistory(repo_root)
    return history.log(type, input, output, metadata)


def main():
    """CLI测试"""
    import argparse
    repo_root = Path(__file__).parent.parent.parent
    
    parser = argparse.ArgumentParser(description="Conversation history")
    parser.add_argument("--recent", type=int, help="Show recent N interactions")
    parser.add_argument("--type", help="Filter by type")
    parser.add_argument("--search", help="Search keyword")
    parser.add_argument("--clear", type=int, metavar="DAYS", help="Clear records older than DAYS days")
    args = parser.parse_args()
    
    history = ConversationHistory(repo_root)
    
    if args.clear:
        n = history.clear_old(args.clear)
        print(f"Cleared {n} old records")
        return
    
    if args.recent:
        for item in history.get_recent(args.recent, type=args.type):
            print(f"[{item['timestamp']}] {item['type']}")
            print(f"  Input: {json.dumps(item['input'], ensure_ascii=False)[:100]}")
            print()
        return
    
    if args.search:
        for item in history.search(args.search):
            print(f"[{item['timestamp']}] {item['type']}")
            print(f"  Input: {json.dumps(item['input'], ensure_ascii=False)[:100]}")
            print(f"  Output: {json.dumps(item['output'], ensure_ascii=False)[:100]}")
            print()
        return
    
    print("Usage: conversation_history.py --recent N [--type TYPE]")


if __name__ == "__main__":
    main()