from file_operations import copy_dir


dir_path_static = "./static"
dir_path_public = "./public"


def main():
    print("Copying static files to public directory...")
    copy_dir(dir_path_static, dir_path_public)

if __name__ == "__main__":
    main()