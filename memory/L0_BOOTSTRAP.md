# L0 启动层（必读）

> 目标：最短上下文，最快进入执行态。

## 项目定位
- 本仓库是 KB 驱动的简历编译系统，不是手工写简历仓库。
- 真相数据源是 `kb/*.yaml` 与 `projects/*/facts.yaml`。
- 输出产物位于 `outputs/`，属于结果，不是事实源。

## 不可变关键事实
- 候选人：Yuchao Zhang（Leo Zhang）
- 毕业时间：February 2026
- 学位：Master of Computer and Information Sciences @ AUT
- 荣誉：First Class Honours，GPA 8.25/9.0
- 经验：10+ years
- 论文：ChatClothes，DOI `10.1109/IVCNZ67716.2025.11281834`
- 面试语言：英文

## 关键入口文件
- 入口命令：`generate.py`
- 简历生成器：`app/backend/generate_cv_from_kb.py`
- 验证器：`app/backend/validate.py`
- 工作规范：`AGENTS.md`
- 约束规则：`.cursorrules`

## 强约束（只保留最核心）
- 禁止编造项目、经历、指标、职责。
- 若信息缺失，输出 `MISSING_INFO`，不要猜测。
- 修改 KB 数据后必须运行：`python app/backend/validate.py`。

## 启动动作（固定顺序）
1. 读取 `memory/L1_SESSION_STATE.md` 获取当前目标与中断点。
2. 判断任务类型，再去 `memory/L2_DEEP_INDEX.md` 选择需要加载的详细文档。
3. 执行最小必要命令，不做全仓库无差别扫描。
