import os



def get_specified_path(dir_name: str, cur_path: str):
    if dir_name is None:
        print("The directory name is none")
        return

    cur_dir_name = os.path.basename(cur_path)
    if cur_dir_name == dir_name:
        return cur_path
    return get_specified_path(dir_name, os.path.dirname(cur_path))

