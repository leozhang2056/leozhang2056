"""
Semantic QA Search with Embedding-based Similarity
增强面试QA的语义检索能力
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

try:
    from sentence_transformers import SentenceTransformer
    _HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    _HAS_SENTENCE_TRANSFORMERS = False


@dataclass
class QARecord:
    """面试QA记录"""
    id: str
    question: str
    answer_points: List[str]
    source: str
    section: Optional[str] = None
    evidence: List[Dict] = field(default_factory=list)
    tips: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None


def embed_texts(
    texts: List[str],
    model_name: str = "all-MiniLM-L6-v2",
    cache_dir: Optional[Path] = None,
) -> List[List[float]]:
    """
    将文本列表转换为嵌入向量
    
    Args:
        texts: 文本列表
        model_name: 模型名称 (默认 all-MiniLM-L6-v2)
        cache_dir: 模型缓存目录
    
    Returns:
        嵌入向量列表
    """
    if not _HAS_SENTENCE_TRANSFORMERS:
        raise ImportError(
            "sentence-transformers is required for semantic search. "
            "Run: pip install sentence-transformers"
        )
    
    model = SentenceTransformer(model_name, cache_folder=str(cache_dir) if cache_dir else None)
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """计算余弦相似度"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class SemanticQA:
    """
    支持语义检索的面试QA系统
    
    用法:
        qa = SemanticQA(repo_root)
        results = qa.search("如何优化Android启动速度", top_k=5)
    """
    
    def __init__(self, repo_root: Path, use_cache: bool = True):
        self.repo_root = Path(repo_root)
        self.qa_dir = self._find_qa_dir()
        self._cache_file = self.repo_root / ".cache" / "qa_embeddings.json"
        self._use_cache = use_cache
        self._records: List[QARecord] = []
        self._indexed = False
    
    def _find_qa_dir(self) -> Path:
        """查找QA目录"""
        root_qa = self.repo_root / "interview_qa"
        if root_qa.exists():
            return root_qa
        kb_qa = self.repo_root / "kb" / "interview_qa"
        if kb_qa.exists():
            return kb_qa
        raise FileNotFoundError("interview_qa directory not found")
    
    def load_all(self) -> List[QARecord]:
        """加载所有QA记录"""
        from interview_qa_cli import load_technical, load_behavioral, load_role_specific
        
        records = []
        
        # technical
        for q in load_technical(self.repo_root):
            records.append(QARecord(
                id=q.get("id", ""),
                question=q.get("question", ""),
                answer_points=q.get("answer_points", []),
                source="technical",
                evidence=q.get("evidence", []),
                tips=q.get("tips", []),
            ))
        
        # behavioral
        for q in load_behavioral(self.repo_root):
            records.append(QARecord(
                id=q.get("id", ""),
                question=q.get("question", ""),
                answer_points=q.get("answer_points", []),
                source="behavioral",
                evidence=q.get("evidence", []),
                tips=q.get("tips", []),
            ))
        
        # role_specific
        role_data = load_role_specific(self.repo_root)
        for section, questions in role_data.items():
            for q in questions:
                records.append(QARecord(
                    id=q.get("id", ""),
                    question=q.get("question", ""),
                    answer_points=q.get("answer_points", []),
                    source="role_specific",
                    section=section,
                    evidence=q.get("evidence", []),
                    tips=q.get("tips", []),
                ))
        
        self._records = records
        return records
    
    def _load_cache(self) -> Dict[str, List[float]]:
        """加载嵌入缓存"""
        if not self._cache_file.exists():
            return {}
        try:
            with open(self._cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _save_cache(self, cache: Dict[str, List[float]]) -> None:
        """保存嵌入缓存"""
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._cache_file, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    
    def build_index(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        force: bool = False,
    ) -> None:
        """
        构建语义索引
        
        Args:
            model_name: 嵌入模型名称
            force: 强制重新构建（忽略缓存）
        """
        if not _HAS_SENTENCE_TRANSFORMERS:
            print("[SemanticQA] sentence-transformers not available, skipping embedding index")
            return
        
        if not self._records:
            self.load_all()
        
        cache = {} if force else self._load_cache()
        to_embed = []
        
        for record in self._records:
            if record.id in cache and cache[record.id]:
                record.embedding = cache[record.id]
            else:
                to_embed.append(record)
        
        if to_embed:
            print(f"[SemanticQA] Embedding {len(to_embed)} questions...")
            texts = [r.question for r in to_embed]
            embeddings = embed_texts(texts, model_name)
            
            for record, emb in zip(to_embed, embeddings):
                record.embedding = emb
                cache[record.id] = emb
        
        if to_embed:
            self._save_cache(cache)
        
        self._indexed = True
        print(f"[SemanticQA] Indexed {len(self._records)} QA records")
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        category: Optional[str] = None,
        role: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        语义搜索面试QA
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            category: 过滤 category (technical/behavioral/role_specific)
            role: 过滤 role (android/backend/ai/iot)
        
        Returns:
            相关QA列表（包含相似度分数）
        """
        if not self._records:
            self.load_all()
        
        if not self._indexed:
            try:
                self.build_index()
            except ImportError:
                print("[SemanticQA] Fallback to keyword matching")
                return self._keyword_search(query, top_k, category, role)
        
        # 获取查询嵌入
        try:
            query_emb = embed_texts([query])[0]
        except ImportError:
            return self._keyword_search(query, top_k, category, role)
        
        # 计算相似度
        results = []
        for record in self._records:
            if category and record.source != category:
                continue
            if role and record.section:
                if role not in record.section:
                    continue
            
            if record.embedding:
                sim = _cosine_similarity(query_emb, record.embedding)
                results.append({
                    "id": record.id,
                    "question": record.question,
                    "answer_points": record.answer_points,
                    "source": record.source,
                    "section": record.section,
                    "evidence": record.evidence,
                    "tips": record.tips,
                    "similarity": sim,
                })
        
        # 排序返回
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
    
    def _keyword_search(
        self,
        query: str,
        top_k: int = 5,
        category: Optional[str] = None,
        role: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """关键词回退搜索"""
        from interview_qa_cli import list_questions
        
        questions = list_questions(self.repo_root, category=category, role=role, search=query)
        return [
            {
                "id": q.get("id", ""),
                "question": q.get("question", ""),
                "answer_points": q.get("answer_points", []),
                "source": q.get("_source", ""),
                "section": q.get("_section", ""),
                "evidence": q.get("evidence", []),
                "tips": q.get("tips", []),
                "similarity": 1.0,  # 标记为关键词匹配
            }
            for q in questions[:top_k]
        ]


def main():
    """CLI测试"""
    import argparse
    repo_root = Path(__file__).parent.parent.parent
    
    parser = argparse.ArgumentParser(description="Semantic QA search")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--category")
    parser.add_argument("--role")
    parser.add_argument("--build", action="store_true", help="Build index first")
    args = parser.parse_args()
    
    qa = SemanticQA(repo_root)
    
    if args.build:
        qa.build_index()
        return
    
    if not args.query:
        print("Usage: semantic_qa.py <query> [--top-k N]")
        return
    
    results = qa.search(args.query, top_k=args.top_k, category=args.category, role=args.role)
    
    print(f"\nFound {len(results)} results:\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. [sim={r['similarity']:.3f}] {r['question']}")
        print(f"   Source: {r['source']}")
        if r.get('section'):
            print(f"   Section: {r['section']}")
        print()


if __name__ == "__main__":
    main()