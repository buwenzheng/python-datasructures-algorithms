# python-datastructures-algorithms

面向数据结构与算法练习的 Python 项目骨架，按「模板化」思路组织题解，便于复用与调试。

- 学习资料参考：[labuladong 的算法笔记](https://labuladong.online/)
- 目录：`src/` 为包源码，`tests/` 为单元测试，`.vscode/` 为调试配置。

## 快速开始（Windows PowerShell）

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e . pytest black ruff mypy rich pytest-cov
.\.venv\Scripts\python.exe -m pytest -q
```

## 快速开始（macOS / Linux，zsh/bash）

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e . pytest black ruff mypy rich pytest-cov
pytest -q
```

- 退出虚拟环境：`deactivate`

## 常用命令

```bash
# 运行单个用例
pytest -q tests/linked_list/test_detect_cycle.py -k detect_cycle

# 运行示例脚本
python -m scripts.run_problem --cycle-pos 1

# 代码质量
black .
ruff check .
mypy src
```

## 目录约定

- `src/dsa/templates/`：滑动窗口、快慢指针、DFS/BFS、二分、回溯、DP 等模板
- `src/dsa/algorithms/`：按主题分类的题解实现
- `src/dsa/structures/`：常用数据结构与构造器（`ListNode`/`TreeNode` 等）
- `tests/`：与 `algorithms` 同构的测试用例

## 调试

- VS Code/Cursor 可使用提供的 `launch.json` 运行当前文件、当前测试或示例脚本。

## 许可

本仓库仅供学习交流使用。
