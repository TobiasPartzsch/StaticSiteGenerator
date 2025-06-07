from file_operations import copy_dir
from generator import generate_page


dir_path_static = "./static"
dir_path_public = "./public"


def main():
    print("Copying static files to public directory...")
    copy_dir(dir_path_static, dir_path_public)
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()