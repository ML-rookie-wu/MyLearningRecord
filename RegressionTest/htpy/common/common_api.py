import os
import re


def get_specified_path(dir_name: str, cur_path: str):
    if dir_name is None:
        print("The directory name is none")
        return

    cur_dir_name = os.path.basename(cur_path)
    if cur_dir_name == dir_name:
        return cur_path

    parent_dir = os.path.dirname(cur_path)
    if parent_dir == cur_path:  # 如果已经到达了根目录，但是还没有找到目标文件夹，则返回None
        return None

    return get_specified_path(dir_name, os.path.dirname(cur_path))


def match_pattern(p, l, n):
    m = re.match(p, l)
    if m is not None:
        result = []
        for i in range(0, n):
            result.append(m.group(i+1))
        return result
    else:
        return None

