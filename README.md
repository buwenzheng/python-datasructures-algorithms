# 个人算法学习工作台

跟随 [labuladong 完整目录](https://labuladong.online/zh/algo/intro/beginner-learning-plan/) 系统学习数据结构与算法。

## 快速开始

```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
```

验证安装：

```bash
python scratch.py
```

## 日常学习流程

```
1. 学习  → 阅读 labuladong 对应章节（打开 chapters/chXX_xxx/notes.md 看链接）
2. 实现  → 在 chapters/chXX_xxx/ 下新建 .py 文件，从零写解法
3. 验证  → 用 verify() 一键验证，或 F5 跑 __main__ 看输出
4. 可视化 → 用 show_xxx() 看算法执行过程，配合 labuladong 可视化面板对照
5. 测试  → 写 _test.py 文件，用 pytest 正式验证
6. 笔记  → 在 notes.md 中用自己的话记录思路（写到能给别人讲明白）
7. 打勾  → 回到本文件更新进度和掌握程度
```

### 学习方法

1. **先掌握框架** — 不要一开始就陷入细节，先理解每个算法的思维框架（ch00 核心框架章是总纲）
2. **动手实现** — 每学完一个数据结构/算法，从零写一遍代码，不用模板骨架
3. **刷题巩固** — 每学完一个算法模板，立即完成对应习题（notes.md 中有文章链接）
4. **定期复习** — 用掌握程度标记（🔴/🟡/🟢）追踪进度，定期回头重写
5. **利用工具** — Debug Visualizer 调试看结构 / PythonTutor 逐行执行 / labuladong 可视化面板对照

### 可视化工具实战指南

学一个新算法时的完整流程：

```
1. 读 labuladong 文章（notes.md 里有链接）
   → 看网站动画理解原理

2. 自己写代码（solution.py 从零写）
   → 写完用 verify() 验证正确性

3. 验证通过后，加 show_xxx() 看过程
   → 终端可视化，确认算法行为符合预期

4. 如果某一步想不通
   → 粘贴到 PythonTutor 逐行看

5. 如果指针/结构搞不清
   → F5 调试 + Debug Visualizer 实时看
```

#### Debug Visualizer — 调试时实时看结构变化

**适用场景**：写链表/树算法时，想看每一步指针怎么动的

**操作步骤**：

```
1. 在 solution.py 里写好代码，设个断点
2. 按 F5 → 选 "▶ 运行当前文件"
3. Ctrl+Shift+P → 输入 "Debug Visualizer: New View"
4. 在表达式框里输入：
     head.getVisualizationData()   ← 链表
     root.getVisualizationData()   ← 二叉树
5. 按 F10 单步，右侧面板实时刷新
```

**示例**（学 ch00 双指针框架时）：

```python
from dsa import build_linked_list

head = build_linked_list([1, 2, 3, 4, 5])
slow = fast = head
# ← 在这行设断点
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    # ← 在这行设断点，Debug Visualizer 输入 head.getVisualizationData()
```

F10 单步走，每次都能看到链表图形 + slow/fast 高亮节点移动。

#### 终端可视化 — 跑代码时看算法状态快照

**适用场景**：不用开调试器，快速看某一步的结果

每个函数对应的学习场景：

| 函数 | 学哪章时用 | 你能看到什么 |
|------|-----------|-------------|
| `show_linked_list` | ch00 双指针 / ch08 链表 | 高亮 slow/fast 指针位置 |
| `show_tree` | ch04 二叉树 / ch11 树算法 | 树形结构，翻转前后对比 |
| `show_array` | ch09 数组算法 | 双指针 L/R 位置 |
| `show_dp` | ch18 动态规划 | DP 表格逐步填充，高亮当前格 |
| `show_window` | ch09 滑动窗口 | 窗口 [left, right) 扩张收缩 |

**示例**（学 ch18 DP 时）：

```python
from dsa import show_dp

def climb_stairs(n):
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
        show_dp([[dp[j]] for j in range(n+1)], highlight=(i, 0), label=f"dp[{i}]={dp[i]}")
    return dp[n]

# F5 运行，终端会逐步打印 DP 表格填充过程
```

#### PythonTutor — 理解递归和执行流程

**适用场景**：递归写蒙了，想看每一步调用栈怎么走

**操作步骤**：

1. 打开 https://pythontutor.com/python-compiler.html#mode=edit
2. 把你的代码粘贴进去
3. 点 "Visualize Execution" → 一步步按 Next

**示例**（学 ch04 二叉树递归遍历时）：

```python
# 粘贴到 PythonTutor
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def traverse(root):
    if root is None:
        return
    print(f"前序: {root.val}")
    traverse(root.left)
    print(f"中序: {root.val}")
    traverse(root.right)

root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
traverse(root)
```

PythonTutor 会画出递归调用栈，你能看到每一步走到哪个节点、前序中序打印顺序。

> 想快速体验所有可视化函数？运行 `python scratch.py`，已内置全部 demo。

### 题解文件模板

每个题解文件从零开始写，不给骨架：

```python
"""LeetCode 142 - 环形链表 II

链接: https://leetcode.cn/problems/linked-list-cycle-ii/
labuladong: https://labuladong.online/algo/data-structure-basic/linked-list-basic/

题目:
    给定链表 head，若链表中有环，返回入环的第一个节点；否则返回 None。
"""

from dsa import ListNode, build_cycle_list, verify


# 从这里开始写你的代码


if __name__ == "__main__":
    # F5 运行，快速验证
    pass
```

### 一键验证

```python
from dsa import verify

def two_sum(nums, target):
    ...

if __name__ == "__main__":
    verify(two_sum, [
        (([2, 7, 11, 15], 9), [0, 1]),
        (([3, 2, 4], 6), [1, 2]),
    ])
# ✅ Case 1
# ✅ Case 2
# 2/2 passed 🎉
```

### 算法可视化（三套工具组合使用）

#### 1. Debug Visualizer（主力，调试时实时可视化）

安装 [Debug Visualizer](https://marketplace.visualstudio.com/items?itemName=hediet.debug-visualizer) 扩展后，
F5 调试时可以实时看到链表/树的结构变化：

```python
# F5 调试时，打开 Debug Visualizer 视图
# （命令面板 Ctrl+Shift+P → Debug Visualizer: New View）
# 在表达式输入框中输入：

head.getVisualizationData()   # 链表 → 图形化展示节点和指针
root.getVisualizationData()   # 二叉树 → 树形结构

# 然后单步调试（F10/F11），实时看数据结构变化
```

#### 2. 终端可视化（快速检查，不用开调试器）

```python
from dsa import show_linked_list, show_array, show_dp, show_window

# 链表高亮节点
show_linked_list(head, highlights=[slow, fast], label="快慢指针")

# 数组双指针
show_array(nums, {left: "L", right: "R"}, label="双指针")

# DP 表格
show_dp(dp, highlight=(i, j), label=f"dp[{i}][{j}]")

# 滑动窗口
show_window(s, left, right, label=f"窗口 [{left}, {right})")
```

#### 3. 在线工具（理解执行流程）

- [PythonTutor](https://pythontutor.com/python-compiler.html#mode=edit) — 粘贴代码，逐行可视化执行过程，理解递归和指针变化
- [labuladong 可视化面板](https://labuladong.online/zh/roadmap/algo/) — 对照网站上的算法动画

> 每章 notes.md 中已附上对应的工具链接。

## 项目结构

```
├── chapters/                   # 学习内容（对齐 labuladong 完整目录）
│   ├── ch00_core_framework/     # 核心刷题框架（11 个子主题）
│   │   ├── 01_framework_thinking/  # 框架思维
│   │   ├── 02_two_pointers/         # 双指针框架
│   │   ├── ...                      # （共 11 个子主题）
│   │   └── 11_complexity/           # 复杂度分析
│   ├── ch01_array_linked_list/  # 数组与链表
│   ├── ch18_dp/                 # 动态规划（5 个子主题）
│   │   ├── 01_basic/            # 基本技巧
│   │   └── ...                  # （共 5 个子主题）
│   ├── ...                      # （共 24 章）
│   └── ch23_sorting/            # 排序算法
├── templates/                  # 算法框架模板（自己推导，非抄来）
├── src/dsa/                    # 工具包
│   ├── list_node.py             # ListNode + 链表构造器
│   ├── tree_node.py             # TreeNode + 二叉树构造器
│   ├── verify.py                # 一键验证题解
│   └── visualize.py             # 算法可视化工具
├── scratch.py                  # 草稿本（F5 随手跑）
├── conftest.py                 # pytest 路径配置
├── pyproject.toml              # 项目配置
└── .vscode/                    # F5 调试配置 + Debug Visualizer 推荐
```

## 学习进度

> 掌握程度：🔴 看了答案才写出 ｜ 🟡 能写但需要想想 ｜ 🟢 能默写随便秒

### 速成路线顺序（推荐）

```
ch00 核心框架（总纲）
    ↓
ch09 数组算法（双指针/滑动窗口/二分搜索）
    ↓
ch08 链表算法（双指针技巧）
    ↓
ch04 二叉树基础（递归遍历 + 层序遍历）
    ↓
ch16 DFS/回溯算法（排列/组合/子集）
    ↓
ch18 动态规划（子序列 → 背包 → 博弈 → 股票）
    ↓
ch17 BFS 算法（最短路径）
    ↓
ch19 贪心算法 → ch05 BST → ch06 堆 → ch07/15 图
```

> 完整学习顺序按 ch00 → ch23 依次进行；速成路线可跳过基础篇（ch01-ch07）直接从框架章开始。

### 复习追踪

> **间隔复习节奏**：学完后 → 1天 → 3天 → 1周 → 2周 → 1月
>
> 每次复习时：不看笔记重新实现一遍，然后更新掌握程度（🔴→🟡→🟢）

| 章节 | 学完日期 | 第1次 | 第2次 | 第3次 | 第4次 | 第5次 | 当前 |
|------|---------|-------|-------|-------|-------|-------|------|
| ch00 |         |       |       |       |       |       | 🔴   |
| ch01 |         |       |       |       |       |       | 🔴   |
| ch02 |         |       |       |       |       |       | 🔴   |
| ch03 |         |       |       |       |       |       | 🔴   |
| ch04 |         |       |       |       |       |       | 🔴   |
| ch05 |         |       |       |       |       |       | 🔴   |
| ch06 |         |       |       |       |       |       | 🔴   |
| ch07 |         |       |       |       |       |       | 🔴   |
| ch08 |         |       |       |       |       |       | 🔴   |
| ch09 |         |       |       |       |       |       | 🔴   |
| ch10 |         |       |       |       |       |       | 🔴   |
| ch11 |         |       |       |       |       |       | 🔴   |
| ch12 |         |       |       |       |       |       | 🔴   |
| ch13 |         |       |       |       |       |       | 🔴   |
| ch14 |         |       |       |       |       |       | 🔴   |
| ch15 |         |       |       |       |       |       | 🔴   |
| ch16 |         |       |       |       |       |       | 🔴   |
| ch17 |         |       |       |       |       |       | 🔴   |
| ch18 |         |       |       |       |       |       | 🔴   |
| ch19 |         |       |       |       |       |       | 🔴   |
| ch20 |         |       |       |       |       |       | 🔴   |
| ch21 |         |       |       |       |       |       | 🔴   |
| ch22 |         |       |       |       |       |       | 🔴   |
| ch23 |         |       |       |       |       |       | 🔴   |

> 复习时填写日期，掌握程度升级时更新 emoji。


### 第一部分：核心框架

- 🔴 **ch00 核心刷题框架** —— 11 个算法框架速览
  - `01_framework_thinking/` 框架思维
  - `02_two_pointers/` 双指针框架
  - `03_sliding_window/` 滑动窗口框架
  - `04_binary_tree/` 二叉树纲领
  - `05_recursion/` 递归思维
  - `06_dp_framework/` 动态规划框架
  - `07_backtrack/` 回溯框架
  - `08_bfs/` BFS 框架
  - `09_greedy/` 贪心框架
  - `10_divide_conquer/` 分治框架
  - `11_complexity/` 复杂度分析

### 第二部分：数据结构基础

- 🔴 **ch01 数组与链表** —— 顺序存储 / 链式存储 / 环形数组
  - `01_array/` 数组基本原理 + 动态数组实现
  - `02_linked_list/` 链表基本原理 + 代码实现
  - `03_variations/` 环形数组 / 跳表 / 位图
- 🔴 **ch02 队列与栈** —— 操作受限的数据结构
- 🔴 **ch03 哈希表** —— 核心原理 / LinkedHashMap / ArrayHashMap
- 🔴 **ch04 二叉树基础及遍历** —— 递归遍历 / 层序遍历 / DFS & BFS
- 🔴 **ch05 二叉搜索树** —— 左小右大
  - `01_basics/` BST 基础（特性 + 搜索）
  - `02_operations/` BST 操作（遍历 / 构造 / 增删改查）
- 🔴 **ch06 二叉堆** —— 优先级队列 / swim & sink
- 🔴 **ch07 图结构** —— 术语 / 通用实现 / DFS & BFS 遍历

### 第三部分：算法刷题

- 🔴 **ch08 链表算法** —— 双指针技巧
- 🔴 **ch09 数组算法** —— 双指针 / 滑动窗口 / 二分搜索 / 位运算
  - `01_two_pointers/` 双指针技巧 + 习题
  - `02_sliding_window/` 滑动窗口框架 + 习题
  - `03_binary_search/` 二分搜索详解 + 习题
  - `04_bit_ops/` 位运算
- 🔴 **ch10 队列栈算法** —— 单调栈 / 单调队列
  - `01_stack_queue/` 栈与队列互拟 + 括号
  - `02_monotonic_stack/` 单调栈思维 + 习题
  - `03_monotonic_queue/` 单调队列思维 + 习题
- 🔴 **ch11 二叉树算法** —— 遍历思维 / 分解问题思维
  - `01_framework/` 二叉树纲领
  - `02_thinking/` 两种思维（思路篇 + 后序篇）
  - `03_techniques/` 常用技巧（序列化 / 还原 / 右视图）
  - `04_exercises/` 习题集
- 🔴 **ch12 二叉搜索树算法** —— 特性 / 基操 / 构造
  - `01_basics/` BST 基本操作（搜索 + 遍历）
  - `02_construction/` BST 构造 + 增删改查
- 🔴 **ch13 字典树** —— 前缀匹配
- 🔴 **ch14 数据结构设计** —— LRU / LFU / 设计题
  - `01_basic/` 基础设计（哈希集合 / 循环队列 / 双端队列）
  - `02_stack/` 栈设计（最小栈 / 最大栈）
  - `03_cache/` 缓存设计（LRU / LFU）
  - `04_advanced/` 高级设计（中位数 / 推特 / 自动补全）
- 🔴 **ch15 图算法** —— 环检测 / 拓扑排序 / 二分图 / 并查集 / MST / Dijkstra
  - `01_basics/` 图基础 + 遍历
  - `02_topological/` 拓扑排序 + 环检测
  - `03_bipartite/` 二分图判定 + 匈牙利算法
  - `04_shortest_path/` 最短路径（Dijkstra / Bellman-Ford）
  - `05_mst/` 最小生成树（Kruskal / Prim / 并查集）
- 🔴 **ch16 DFS/回溯算法** —— 排列 / 组合 / 子集 / 岛屿
  - `01_framework/` 回溯框架
  - `02_permutation/` 排列/组合/子集 + 球盒模型
  - `03_classic/` 经典问题（数独/N皇后 + 岛屿）
  - `04_exercises/` 习题集（括号生成 + 集合划分）
- 🔴 **ch17 BFS 算法** —— 最短路径
- 🔴 **ch18 动态规划** —— 基本技巧 / 子序列 / 背包 / 博弈股票 / 习题集
  - `01_basic/` 基本技巧（独立性、状态转移方程）
  - `02_subsequence/` 子序列问题（LCS、编辑距离、LIS）
  - `03_knapsack/` 背包问题（0-1/子集/完全）
  - `04_game_stock/` 博弈/股票/打家劫舍
  - `05_exercises/` 习题集（经典 + 难题）
- 🔴 **ch19 贪心算法** —— 贪心选择性质
  - `01_framework/` 贪心框架
  - `02_interval/` 区间问题（调度 + 重叠）
  - `03_exercises/` 习题集（跳跃游戏 + 经典）
- 🔴 **ch20 分治算法** —— 分而治之
- 🔴 **ch21 数学技巧** —— 素数 / 随机算法 / 位运算
  - `01_bit_ops/` 位运算（一行代码 + 常用位操作）
  - `02_number_theory/` 数论（数学技巧 + 素数 + 阶乘）
  - `03_probability/` 概率与随机（缺失重复 + 概率 + 随机算法）
- 🔴 **ch22 经典面试题** —— 接雨水 / 丑数 / 区间
  - `01_rain_water/` 接雨水
  - `02_ugly_number/` 丑数系列
  - `03_misc/` 其他经典（区间 + 烧饼排序 + 字符串乘法 + 完美矩形）
- 🔴 **ch23 排序算法** —— 十大排序串讲
  - `01_overview/` 排序概览
  - `02_merge_sort/` 归并排序
  - `03_quick_sort/` 快速排序 + 快速选择 + 堆排序

---

*章节内容以 [labuladong 完整目录](https://labuladong.online/zh/algo/intro/beginner-learning-plan/) 为准。*
