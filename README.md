# 跟着 labuladong 学算法

按照 [labuladong 的算法笔记](https://labuladong.online/) 学习路径，逐章学习、亲手实现、记录笔记。

## 快速开始

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e . pytest black ruff mypy

# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e . pytest black ruff mypy
```

## 使用方式

### 日常学习流程

1. **学习** → 阅读 labuladong 对应章节
2. **实现** → 打开 `chapters/chXX_xxx/` 下的 `.py` 文件，填写 `TODO` 部分
3. **调试** → 按 **F5**（选择「▶ 运行当前文件」），立即看到输出结果
4. **笔记** → 在同目录的 `notes.md` 中记录思路、踩坑、总结
5. **打勾** → 回到本文件，更新下方学习进度

### 调试技巧

- 每个 `.py` 文件底部都有 `if __name__ == "__main__":` 调试区域
- F5 运行当前文件，可以打断点、单步执行
- `scratch.py` 是万能草稿本，随时写代码跑

### 可视化工具

```python
from dsa import build_linked_list, build_tree

# 链表打印
print(build_linked_list([1, 2, 3]))  # 1 -> 2 -> 3 -> None

# 二叉树打印
print(build_tree([1, 2, 3, None, 4]))
#   1
#  / \
# 2   3
#  \
#   4
```

## 项目结构

```
├── chapters/                  # 按 labuladong 章节组织的学习内容
│   └── ch01_array_linked_list/
│       ├── notes.md           # 学习笔记（思路、踩坑、总结）
│       └── 01_detect_cycle.py # 题解代码（含调试区域）
├── src/dsa/                   # 工具包（数据结构构造器 + 可视化）
│   ├── list_node.py           # ListNode + 链表构造器
│   └── tree_node.py           # TreeNode + 二叉树构造器
├── scratch.py                 # 草稿本（随手写代码 F5 运行）
├── .vscode/launch.json        # F5 调试配置
└── pyproject.toml             # 项目配置
```

### 新增章节模板

学到新章节时，创建对应文件夹即可：

```
chapters/ch02_binary_tree/
├── notes.md                   # 复制已有的 notes.md 改改标题
└── 01_invert_tree.py          # 新建题解文件
```

每个 `.py` 文件建议格式：

```python
"""LeetCode XXX - 题目名称

链接: https://leetcode.cn/problems/xxx/
对应 labuladong: https://labuladong.online/algo/xxx/

题目: ...
思路: ...
"""
from dsa import ...

def solution(...):
    # TODO: 请自行实现
    raise NotImplementedError

# ============================================================
# 调试区域 —— F5 运行当前文件即可看到输出
# ============================================================
if __name__ == "__main__":
    # 构造测试数据
    # 调用函数
    # 打印结果
    pass
```

---

## 学习进度

> 参考路线：[labuladong 速成路线图](https://labuladong.online/)

### 第一阶段：数据结构基础

- [ ] **ch01 数组与链表**
  - [ ] 环形链表 II（LeetCode 142）
  - [ ] 反转链表（LeetCode 206）
  - [ ] 合并两个有序链表（LeetCode 21）
  - [ ] 删除链表倒数第 N 个节点（LeetCode 19）
  - [ ] 链表的中间节点（LeetCode 876）

- [ ] **ch02 二叉树**
  - [ ] 二叉树的最大深度（LeetCode 104）
  - [ ] 翻转二叉树（LeetCode 226）
  - [ ] 二叉树的直径（LeetCode 543）
  - [ ] 二叉树展开为链表（LeetCode 114）

### 第二阶段：核心算法框架

- [ ] **ch03 双指针技巧**
- [ ] **ch04 滑动窗口**
- [ ] **ch05 二分查找**
- [ ] **ch06 BFS 算法**
- [ ] **ch07 回溯算法**
- [ ] **ch08 动态规划**

### 第三阶段：进阶扩展

- [ ] **ch09 图算法**
- [ ] **ch10 贪心算法**
- [ ] **ch11 数学技巧**

---

*章节编号和内容可随学习进度自由调整，以你实际跟的 labuladong 路线为准。*

