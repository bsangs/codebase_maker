import os
import argparse
import fnmatch
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate a Markdown file with the directory structure and file contents.')
    parser.add_argument('-I', '--ignore', nargs='*', default=[], help='Patterns to ignore (e.g., *.pyc __pycache__)')
    parser.add_argument('-L', '--level', type=int, default=None, help='Max directory depth to traverse')
    parser.add_argument('path', nargs='?', default='.', help='Path to traverse (default: current directory)')
    return parser.parse_args()

def should_ignore(name, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    return False

def generate_tree(root_path, ignore_patterns, max_depth):
    tree_lines = []
    root_name = os.path.basename(os.path.abspath(root_path))
    if root_name == '':
        root_name = os.path.abspath(root_path)
    tree_lines.append("```\n" + root_name)
    
    def recurse(current_path, prefix='', depth=0):
        if max_depth is not None and depth >= max_depth:
            return
        try:
            items = sorted(os.listdir(current_path))
        except PermissionError:
            tree_lines.append(f"{prefix}├── [Permission Denied]")
            return
        items = [item for item in items if not should_ignore(item, ignore_patterns)]
        for index, item in enumerate(items):
            path = os.path.join(current_path, item)
            connector = '├──' if index < len(items) -1 else '└──'
            tree_lines.append(f"{prefix}{connector} {item}")
            if os.path.isdir(path):
                extension = '│   ' if index < len(items) -1 else '    '
                recurse(path, prefix + extension, depth +1)
    recurse(root_path)
    tree_lines.append("```")
    return '\n'.join(tree_lines)

def generate_file_contents(root_path, ignore_patterns, max_depth):
    contents = []
    def recurse(current_path, depth=0):
        if max_depth is not None and depth >= max_depth:
            return
        try:
            for entry in sorted(os.listdir(current_path)):
                if should_ignore(entry, ignore_patterns):
                    continue
                path = os.path.join(current_path, entry)
                if os.path.isdir(path):
                    recurse(path, depth +1)
                else:
                    rel_path = os.path.relpath(path, root_path)
                    contents.append(f"## **{os.path.sep}{rel_path}**\n")
                    _, ext = os.path.splitext(entry)
                    ext = ext.lstrip('.') if ext else ''
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        contents.append(f"```{ext}\n{file_content}\n```\n")
                    except UnicodeDecodeError:
                        # 파일이 텍스트가 아닐 경우 (예: 바이너리 파일)
                        contents.append(f"```text\n[Binary file not displayed]\n```\n")
                    except Exception as e:
                        contents.append(f"```text\n[Could not read file: {e}]\n```\n")
        except PermissionError:
            contents.append(f"**[Permission Denied]: {current_path}**\n")
    recurse(root_path)
    return '\n'.join(contents)

def main():
    args = parse_arguments()
    
    # 현재 스크립트가 실행된 디렉토리 경로
    base_dir = os.path.abspath(os.getcwd())
    codebases_dir = os.path.join(base_dir, "codebases")
    
    # codebases 디렉토리가 없으면 생성
    os.makedirs(codebases_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f"{timestamp}_codebase.md"
    output_filepath = os.path.join(codebases_dir, output_filename)

    # Generate file structure
    tree = generate_tree(args.path, args.ignore, args.level)

    # Generate file contents
    file_contents = generate_file_contents(args.path, args.ignore, args.level)

    # Combine into Markdown
    markdown = f"# 파일구조\n{tree}\n\n# 파일 내용\n{file_contents}"

    # Write to file
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"Markdown 파일이 생성되었습니다: {output_filepath}")
    except Exception as e:
        print(f"Markdown 파일 생성에 실패했습니다: {e}")

if __name__ == "__main__":
    main()
