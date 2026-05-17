import os
import shutil
import sys

from markdown_blocks import markdown_to_html_node


def copy_directory_contents(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)
    copy_recursive(source, destination)


def copy_recursive(source, destination):
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            print(f"Copying {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            os.mkdir(destination_path)
            copy_recursive(source_path, destination_path)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("markdown must contain an h1 heading")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as markdown_file:
        markdown = markdown_file.read()

    with open(template_path) as template_file:
        template = template_file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    destination_dir = os.path.dirname(dest_path)
    if destination_dir != "":
        os.makedirs(destination_dir, exist_ok=True)

    with open(dest_path, "w") as destination_file:
        destination_file.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        destination_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_path):
            if source_path.endswith(".md"):
                destination_path = destination_path[:-3] + ".html"
                generate_page(source_path, template_path, destination_path, basepath)
        else:
            generate_pages_recursive(
                source_path,
                template_path,
                destination_path,
                basepath,
            )


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_path = os.path.join(project_root, "static")
    docs_path = os.path.join(project_root, "docs")
    content_path = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")

    copy_directory_contents(static_path, docs_path)
    generate_pages_recursive(content_path, template_path, docs_path, basepath)


if __name__ == "__main__":
    main()
