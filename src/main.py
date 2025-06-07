import sys
from file_operations import copy_dir
from generator import generate_pages_recursive


dir_path_static = "./static"
dir_path_content = "./content"
dir_path_output = "./docs"


def main():
    basepath = sys.argv[1] if len(sys.argv) >1 else '/'
    print(f"basepath is {basepath}")

    print("Copying static files to output directory...")
    copy_dir(dir_path_static, dir_path_output)
    generate_pages_recursive(dir_path_content, "template.html", dir_path_output, basepath)


if __name__ == "__main__":
    main()