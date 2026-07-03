"""pytest 全局配置：自动将 src/ 加入 Python 路径。

这样测试文件中可以直接 `from dsa import ...`，
无需手动处理 sys.path。
"""

import sys
from pathlib import Path

# 将 src/ 目录加入 Python 路径
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# 将项目根目录加入路径，方便测试中 import chapters.xxx
root_path = str(Path(__file__).parent)
if root_path not in sys.path:
    sys.path.insert(0, root_path)
