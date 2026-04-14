"""
LLM Patch Decision Log - LLM迭代决策日志
记录AI修改KB的决策，支持追溯和回滚
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class PatchStatus(Enum):
    """Patch状态"""
    PENDING = "pending"
    APPLIED = "applied"
    REVERTED = "reverted"
    FAILED = "failed"


class PatchType(Enum):
    """Patch类型"""
    PROFILE = "profile"
    SKILLS = "skills"
    PROJECT = "project"
    BULLETS = "bullets"
    QA = "qa"
    CONFIG = "config"


@dataclass
class PatchDecision:
    """单次Patch决策"""
    id: str
    timestamp: str
    iteration_id: str
    type: str
    target_file: str
    original_content: str
    new_content: str
    reason: str
    status: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class LLMPatchLog:
    """
    LLM Patch 决策日志管理器
    
    用法:
        log = LLMPatchLog(repo_root)
        
        # 记录决策
        log.record_decision(
            iteration_id="20260414_143022",
            type=PatchType.PROFILE,
            target_file="kb/profile.yaml",
            original_content="...",
            new_content="...",
            reason="Add Android keyword",
        )
        
        # 获取历史
        decisions = log.get_by_iteration("20260414_143022")
        
        # 回滚
        log.revert("patch_001")
    """
    
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self._log_file = self.repo_root / ".cache" / "llm_patch_log.json"
        self._backup_dir = self.repo_root / ".cache" / "kb_backups"
        self._ensure_dirs()
    
    def _ensure_dirs(self) -> None:
        """确保目录存在"""
        self._log_file.parent.mkdir(parents=True, exist_ok=True)
        self._backup_dir.mkdir(parents=True, exist_ok=True)
    
    def _load(self) -> List[Dict[str, Any]]:
        """加载日志"""
        if not self._log_file.exists():
            return []
        try:
            with open(self._log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    
    def _save(self, data: List[Dict[str, Any]]) -> None:
        """保存日志"""
        with open(self._log_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        return f"patch_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def _backup_file(self, file_path: Path) -> Path:
        """备份文件"""
        if not file_path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = self._backup_dir / backup_name
        
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def record_decision(
        self,
        iteration_id: str,
        type: PatchType,
        target_file: str,
        original_content: str,
        new_content: str,
        reason: str,
        status: PatchStatus = PatchStatus.PENDING,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        记录一次Patch决策
        
        Args:
            iteration_id: 迭代ID
            type: Patch类型
            target_file: 目标文件路径
            original_content: 原内容
            new_content: 新内容
            reason: 修改原因
            status: 状态
            metadata: 额外元数据
        
        Returns:
            Patch ID
        """
        patch_id = self._generate_id()
        
        # 备份原文件
        backup_path = self._backup_file(self.repo_root / target_file)
        
        decision = {
            "id": patch_id,
            "timestamp": datetime.now().isoformat(),
            "iteration_id": iteration_id,
            "type": type.value,
            "target_file": target_file,
            "backup_file": str(backup_path) if backup_path else None,
            "original_content": original_content,
            "new_content": new_content,
            "reason": reason,
            "status": status.value,
            "metadata": metadata or {},
        }
        
        data = self._load()
        data.append(decision)
        self._save(data)
        
        return patch_id
    
    def apply_patch(self, patch_id: str) -> bool:
        """
        应用Patch
        
        Args:
            patch_id: Patch ID
        
        Returns:
            是否成功
        """
        data = self._load()
        
        for decision in data:
            if decision.get("id") != patch_id:
                continue
            
            target_path = self.repo_root / decision["target_file"]
            
            try:
                # 写入新内容
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(decision["new_content"])
                
                # 更新状态
                decision["status"] = PatchStatus.APPLIED.value
                self._save(data)
                return True
            except Exception as e:
                decision["status"] = PatchStatus.FAILED.value
                decision["metadata"]["error"] = str(e)
                self._save(data)
                return False
        
        return False
    
    def revert_patch(self, patch_id: str) -> bool:
        """
        回滚Patch
        
        Args:
            patch_id: Patch ID
        
        Returns:
            是否成功
        """
        data = self._load()
        
        for decision in data:
            if decision.get("id") != patch_id:
                continue
            
            target_path = self.repo_root / decision["target_file"]
            backup_path = decision.get("backup_file")
            
            if not backup_path or not Path(backup_path).exists():
                # 尝试从 new_content 回滚（有风险）
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(decision["original_content"])
            else:
                shutil.copy2(backup_path, target_path)
            
            # 更新状态
            decision["status"] = PatchStatus.REVERTED.value
            self._save(data)
            return True
        
        return False
    
    def get_by_iteration(self, iteration_id: str) -> List[Dict[str, Any]]:
        """获取指定迭代的所有决策"""
        data = self._load()
        return [x for x in data if x.get("iteration_id") == iteration_id]
    
    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近的决策"""
        data = self._load()
        return data[-limit:]
    
    def get_pending(self) -> List[Dict[str, Any]]:
        """获取待应用的决策"""
        data = self._load()
        return [x for x in data if x.get("status") == PatchStatus.PENDING.value]
    
    def get_status_summary(self) -> Dict[str, int]:
        """获取状态统计"""
        data = self._load()
        summary = {}
        for decision in data:
            status = decision.get("status", "unknown")
            summary[status] = summary.get(status, 0) + 1
        return summary


def log_patch_decision(
    repo_root: Path,
    iteration_id: str,
    type: PatchType,
    target_file: str,
    original_content: str,
    new_content: str,
    reason: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """
    便捷函数：记录Patch决策
    
    用法:
        log_patch_decision(
            repo_root,
            iteration_id="20260414_143022",
            type=PatchType.PROFILE,
            target_file="kb/profile.yaml",
            original_content="...",
            new_content="...",
            reason="Add Android keyword",
        )
    """
    log = LLMPatchLog(repo_root)
    return log.record_decision(
        iteration_id=iteration_id,
        type=type,
        target_file=target_file,
        original_content=original_content,
        new_content=new_content,
        reason=reason,
        metadata=metadata,
    )


def main():
    """CLI测试"""
    import argparse
    repo_root = Path(__file__).parent.parent.parent
    
    parser = argparse.ArgumentParser(description="LLM patch log")
    parser.add_argument("--recent", type=int, help="Show recent N patches")
    parser.add_argument("--iteration", help="Show patches by iteration ID")
    parser.add_argument("--status", action="store_true", help="Show status summary")
    parser.add_argument("--apply", metavar="PATCH_ID", help="Apply a patch")
    parser.add_argument("--revert", metavar="PATCH_ID", help="Revert a patch")
    args = parser.parse_args()
    
    log = LLMPatchLog(repo_root)
    
    if args.apply:
        success = log.apply_patch(args.apply)
        print(f"Apply {'success' if success else 'failed'}")
        return
    
    if args.revert:
        success = log.revert_patch(args.revert)
        print(f"Revert {'success' if success else 'failed'}")
        return
    
    if args.status:
        summary = log.get_status_summary()
        print("Status summary:")
        for status, count in summary.items():
            print(f"  {status}: {count}")
        return
    
    if args.iteration:
        patches = log.get_by_iteration(args.iteration)
        print(f"Found {len(patches)} patches:")
        for p in patches:
            print(f"  [{p['status']}] {p['type']} -> {p['target_file']}")
            print(f"    Reason: {p['reason']}")
        return
    
    if args.recent:
        for p in log.get_recent(args.recent):
            print(f"[{p['timestamp']}] {p['id']}")
            print(f"  {p['type']} -> {p['target_file']} [{p['status']}]")
            print(f"  Reason: {p['reason']}")
            print()
        return
    
    print("Usage: llm_patch_log.py --recent N | --iteration ID | --status")


if __name__ == "__main__":
    main()