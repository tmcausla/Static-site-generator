import shutil
import os
from markdown_to_html import markdown_to_html_node

def static_to_public(static_path='static', public_path='public'):
    if os.path.exists(static_path):
        for entry in os.listdir(static_path):
            new_static_path = os.path.join(static_path, entry)
            new_public_path = os.path.join(public_path, entry)

            if os.path.isdir(new_static_path):
                # print(f"making new dir: {new_public_path}")
                os.mkdir(new_public_path)
                static_to_public(new_static_path, new_public_path)

            elif os.path.isfile(new_static_path):
                # print(f"making path: {new_public_path}")
                shutil.copy(new_static_path, new_public_path)

def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()

        if line.startswith('# '):
            title = line[1:].strip()
            if title:
                return title
        
    raise Exception("there is no title in this markdown file")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating a path from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md_file:
        markdown = md_file.read()
    with open(template_path) as template_file:
        template = template_file.read()

    html_str = markdown_to_html_node(markdown).to_html()
    md_title = extract_title(markdown)
    template = template.replace("{{ Title }}", md_title).replace("{{ Content }}", html_str)

    with open(dest_path, 'w') as new_file:
        new_file.write(template)
        print(f"successfully created {dest_path}")


# main fxn
def main():
    if os.path.exists('public'):
        # print("clearing public dir")
        shutil.rmtree('public')
    os.mkdir('public')
    # print("made new public dir")

    static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
