import os
from markdown_blocks import BlockType, markdown_to_html_node

MD_EXT = ".md"

def extract_title(markdown: str) -> str:
    h1 = f"{BlockType.HEADING} "
    for line in markdown.split('\n'):
        if line.startswith(h1):
            return line[2:]
    raise ValueError(f"No first-level heading found in {"\n".join(markdown.split('\n'))}")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path) as from_file:
        from_content = from_file.read()

    with open(template_path) as template_file:
        template_content = template_file.read()

    content = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", content)

    # make sure dest_path directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(template_content)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    print(f"Generating pages in {dir_path_content} to {dest_dir_path} using {template_path}.")
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        f, ext = os.path.splitext(entry)
        if os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path, entry))
        elif ext.lower() == MD_EXT:
            generate_page(entry_path, template_path, os.path.join(dest_dir_path, f"{f}.html"))
        else:
            print(f"ignore {entry}")
