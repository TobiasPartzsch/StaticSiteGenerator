import os
import shutil


def copy_dir(src_dir: str, dest_dir: str):
    if not os.path.exists(src_dir) or not os.path.isdir(src_dir):
        raise RuntimeError(f"Source directory {src_dir} doesn't exist or is not directory")

    if os.path.exists(dest_dir):
        # clear destination if it already exists
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

    for entry in sorted(os.listdir(src_dir)):
        entry_path = os.path.join(src_dir, entry)
        dest_path = os.path.join(dest_dir, entry)

        if os.path.isfile(entry_path):
            print(f"Copying {entry_path} to {dest_path}")
            shutil.copy(entry_path, dest_path)
        elif os.path.isdir(entry_path):
            copy_dir(entry_path, dest_path)
