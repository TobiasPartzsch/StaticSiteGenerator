import sys
from file_operations import copy_dir
from generator import generate_pages_recursive


dir_path_static = "./static"
dir_path_public = "./public"


def main():
    basepath = sys.argv[0] or '/'

    print("Copying static files to public directory...")
    copy_dir(dir_path_static, dir_path_public)
    generate_pages_recursive("content", "template.html", "public", basepath)


if __name__ == "__main__":
    main()