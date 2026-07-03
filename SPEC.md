# SPEC — 技术规格说明书

> Software Requirements Specification (IEEE 830) · 技术视角：具体怎么做、接口规格、实现约束

## 1. 目的与范围

本文档定义个人算法学习工作台的技术实现规格，包括项目结构规范、工具包 API、可视化方案、笔记模板格式、代码质量标准和环境要求。

产品层面的需求定义见 [PRD.md](PRD.md)。

## 2. 项目结构规范

### 2.1 目录结构

```
├── chapters/                   # 学习内容（24 章，对齐 labuladong）
│   ├── ch00_core_framework/    # 核心刷题框架（11 个子主题）
│   │   ├── notes.md            # 索引页（子主题表 + 文章索引）
│   │   ├── 01_framework_thinking/  notes.md + solution.py
│   │   ├── 02_two_pointers/
│   │   └── ...
│   ├── ch01_array_linked_list/ # 数组与链表（3 个子主题）
│   ├── ch02_queue_stack/       # 队列与栈（单 notes.md）
│   ├── ...
│   ├── ch18_dp/                # 动态规划（5 个子主题）
│   └── ch23_sorting/           # 排序算法（3 个子主题）
├── templates/                  # 算法框架模板（自己推导，不抄）
│   └── README.md               # 模板索引
├── src/dsa/                    # 工具包
│   ├── __init__.py             # 包入口 + Windows UTF-8 处理
│   ├── list_node.py            # ListNode + 链表构造器
│   ├── tree_node.py            # TreeNode + 二叉树构造器
│   ├── verify.py               # 一键验证题解
│   └── visualize.py            # 终端可视化（5 个函数）
├── scratch.py                  # 草稿本（F5 随手跑）
├── conftest.py                 # pytest 路径配置
├── pyproject.toml              # 项目配置（依赖/lint/test）
├── PRD.md                      # 产品需求文档
├── SPEC.md                     # 本文档（技术规格）
└── .vscode/                    # F5 调试 + 扩展推荐
```

### 2.2 章节拆分规则

| 条件 | 结构 |
|------|------|
| 文章数 ≤ 6 篇 | 单 `notes.md`（含全部 6 模块） |
| 文章数 ≥ 7 篇 | 拆分子目录，每个含 `notes.md` + `solution.py`，主 `notes.md` 变索引页 |

### 2.3 子目录文件规范

**notes.md**（统一增强型笔记模板）：

```markdown
# 主题名称

> 简要描述

## 学习资源
- labuladong 文章链接
- PythonTutor 链接
- Debug Visualizer 使用提示

## LeetCode 对应题目
> 以下为本章/本节对应的核心 LeetCode 题目，学完后建议去对应刷题。
- 题号 题目名称

## 一句话概括
<!-- 逼自己用一句话说清楚这个概念到底是什么。写不出说明还没懂。 -->

## 核心要点
<!-- 用自己的话拆解成几个关键点，每个关键点配一句话解释。不抄原文，用自己的语言重组。 -->

### 要点 1：……
### 要点 2：……
### 要点 3：……

## 关键代码框架
（手写本章节的关键模板代码，不用复制粘贴）

## 类比理解
<!-- 用生活中的类比解释抽象概念。好的类比能让概念一次记住。 -->

| 概念 | 类比 |
|------|------|
| …… | …… |

## 对比与区分
<!-- 用对比表厘清容易混淆的概念边界 -->

## 自测问答
<!-- 苏格拉底式自问自答。如果能流畅回答，说明真懂了。学完后来填。 -->

**Q1：……**

**Q2：……**

## 踩坑记录
（实际写代码时遇到的错误和顿悟）

## 知识连接
- 这个知识点和前面学的什么有关？
- 后面哪里会用到这个知识点？
```

> **纯概念主题**（如框架思维、复杂度分析）不需要 solution.py，只保留 notes.md 即可。
> 关键代码框架段落可省略或写示意伪码。

**solution.py**（空白题解文件，可选）：

```python
"""题解描述

LeetCode 链接: ...
"""

from dsa import verify


if __name__ == "__main__":
    pass
```

### 2.4 索引页规范（有子目录的章节）

主 `notes.md` 变为索引页，包含：
1. 子主题表（子目录 → 主题 → 文章数）
2. 全部文章索引（含 labuladong 链接 + 子目录映射）
3. PythonTutor + Debug Visualizer 工具链接
4. 本章总结段落（学完后填写）

## 3. dsa 工具包规格

### 3.1 ListNode（`src/dsa/list_node.py`）

**数据结构**：

```python
class ListNode:
    val: int
    next: Optional[ListNode]
```

**方法**：

| 方法 | 行为 |
|------|------|
| `__str__` | 可视化打印，自动检测环：`1 -> 2 -> 3 -> [回到 2]` |
| `__eq__(other)` | 按值比较两个链表（忽略环） |
| `__repr__` | 同 `__str__` |
| `to_list()` | 转值列表 `[int]`（遇环停止） |
| `getVisualizationData()` | 返回 graph 格式 JSON（Debug Visualizer 用） |

**构造函数**：

| 函数 | 签名 | 说明 |
|------|------|------|
| `build_linked_list` | `(values: Iterable[int]) -> Optional[ListNode]` | 从值列表构造链表 |
| `build_cycle_list` | `(values: Iterable[int], pos: int) -> Optional[ListNode]` | 构造带环链表（`pos=-1` 无环） |

### 3.2 TreeNode（`src/dsa/tree_node.py`）

**数据结构**：

```python
class TreeNode:
    val: int
    left: Optional[TreeNode]
    right: Optional[TreeNode]
```

**方法**：

| 方法 | 行为 |
|------|------|
| `__str__` | 树形打印（递归生成可视化行） |
| `__eq__(other)` | 结构和值比较（递归） |
| `__repr__` | 同 `__str__` |
| `to_list()` | 层序序列化 `list[int \| None]`（LeetCode 格式） |
| `getVisualizationData()` | 返回 tree 格式 JSON（Debug Visualizer 用） |

**构造函数**：

| 函数 | 签名 | 说明 |
|------|------|------|
| `build_tree` | `(values: Iterable[int \| None]) -> Optional[TreeNode]` | 逐元素 BFS 构建（非 zip trick，安全处理奇数长度） |
| `tree_to_list` | `(root: Optional[TreeNode]) -> list[int \| None]` | 层序序列化，去掉尾部 None |

### 3.3 verify（`src/dsa/verify.py`）

**签名**：

```python
def verify(func: Callable, cases: list[tuple]) -> None
```

**用例格式**：

| 格式 | 说明 |
|------|------|
| `(args, expected)` | 基本格式 |
| `(args, expected, "描述")` | 带描述 |

`args` 可以是单值（自动包装为单参数调用）或 tuple（解包为多参数调用）。

**行为**：
- 自动处理 ListNode/TreeNode 的深度比较（通过 `_deep_equal`）
- 彩色输出 ✅/❌ + 通过率汇总
- 异常时输出 💥 + 异常信息

### 3.4 visualize（`src/dsa/visualize.py`）

依赖：`rich` 库，`Console(legacy_windows=False)` 解决 Windows 编码。

| 函数 | 签名 | 用途 |
|------|------|------|
| `show_linked_list` | `(head, highlights=None, label=None)` | 链表可视化 + 高亮节点 |
| `show_tree` | `(root, label=None)` | 二叉树树形打印 |
| `show_array` | `(arr, pointers=None, label=None)` | 数组可视化 + 指针标记 |
| `show_dp` | `(dp, highlight=None, label=None)` | DP 表格可视化 + 高亮格子 |
| `show_window` | `(s, left, right, label=None)` | 滑动窗口 `[left, right)` |

## 4. 可视化方案

### 4.1 三套工具组合

| 工具 | 场景 | 使用方式 |
|------|------|---------|
| **Debug Visualizer** | 调试时实时看链表/树结构 | F5 → Ctrl+Shift+P → New View → 输入 `head.getVisualizationData()` |
| **终端可视化** | 快速看算法状态快照 | 代码中调用 `show_xxx()` |
| **PythonTutor** | 理解递归和指针执行流程 | 粘贴代码到 pythontutor.com |

### 4.2 Debug Visualizer JSON 格式

**ListNode** → graph 格式：

```json
{
  "kind": {"graph": true},
  "nodes": [{"id": "0", "label": "1"}, ...],
  "edges": [{"from": "0", "to": "1", "label": "next"}, ...]
}
```

支持环检测：通过 `id(node)` 跟踪已访问节点，检测到环时添加回边。

**TreeNode** → tree 格式：

```json
{
  "kind": {"tree": true},
  "root": {"value": "4", "left": {...}, "right": {...}}
}
```

### 4.3 工具与章节映射

| 函数 | 适用章节 |
|------|---------|
| `show_linked_list` | ch00 双指针 / ch08 链表算法 |
| `show_tree` | ch04 二叉树 / ch11 树算法 |
| `show_array` | ch09 数组算法 |
| `show_dp` | ch18 动态规划 |
| `show_window` | ch09 滑动窗口 |

## 5. LeetCode 题目对照规范

每个 `notes.md` 必须包含 `## LeetCode 对应题目` 段落。

**段落位置**：在「学习资源」之后、「核心概念」之前。

**格式**：

```markdown
## LeetCode 对应题目

> 以下为本章/本节对应的核心 LeetCode 题目，学完后建议去对应刷题。

- 题号 题目名称
- 题号 题目名称
```

## 6. 代码质量标准

| 工具 | 用途 | 配置位置 |
|------|------|---------|
| ruff | Lint（E/F/I/N/UP/B 规则） | pyproject.toml `[tool.ruff.lint]` |
| black | 格式化（line-length=100） | pyproject.toml `[tool.black]` |
| mypy | 类型检查（strict 模式） | pyproject.toml `[tool.mypy]` |
| pytest | 测试框架（chapters/ + templates/） | pyproject.toml `[tool.pytest]` |

**特殊规则**：

| 规则 | 说明 |
|------|------|
| `N802` 忽略 | `getVisualizationData()` 方法名必须驼峰（Debug Visualizer 扩展要求） |
| `E501` 忽略 | 行长度由 black 控制 |

**Python 版本特性**：使用 `X | None` 代替 `Optional[X]`，`list[X]` 代替 `List[X]`，`Callable` 从 `collections.abc` 导入。

## 7. 环境要求

| 项目 | 要求 |
|------|------|
| Python | ≥ 3.11 |
| 包管理 | pip + editable install (`pip install -e ".[dev]"`) |
| 虚拟环境 | venv（`.venv/`） |
| 操作系统 | Windows / macOS / Linux |
| IDE | VSCode（推荐，F5 调试 + Debug Visualizer 扩展） |

### 7.1 Windows 特殊处理

| 问题 | 解决方案 |
|------|---------|
| emoji 输出乱码 | `__init__.py` 中 `sys.stdout.reconfigure(encoding="utf-8")` |
| rich 库 PowerShell 编码 | `Console(legacy_windows=False)` |
| 换行符不一致 | `.gitattributes` 强制 `.py`/`.md` 使用 LF |

### 7.2 依赖

**运行时**：`rich >= 13.0`

**开发时**：`pytest >= 7.0`、`black >= 23.0`、`ruff >= 0.1`、`mypy >= 1.0`

### 7.3 VSCode 配置

| 文件 | 内容 |
|------|------|
| `launch.json` | 3 种 F5 配置：运行当前文件 / 运行草稿本 / 运行 pytest |
| `settings.json` | pytest 启用 + black 格式化 + ruff onSave |
| `extensions.json` | 推荐 `hediet.debug-visualizer` |

---

*产品需求定义见 [PRD.md](PRD.md)*
