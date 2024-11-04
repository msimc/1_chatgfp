# File Name: project_structure_tree.py
# Location: root of your project directory
# Description: Generates a tree view of the project structure, focusing only on relevant directories and files, including all scripts and file names in the various subdirectories. Includes date and time of last modification. Additionally generates a file listing the last 10 modified files.
# Updated: 2024-11-04, 16:15 CET

import os
import datetime

# Directories and files to include
INCLUDED_DIRS = {'src', 'alembic', 'database', 'scripts', 'tests', 'config'}
INCLUDED_EXTENSIONS = {'.py', '.md', '.ini', '.json', '.sql', '.env'}
EXCLUDED_DIRS = {'venv', 'node_modules', 'migrations', 'dist', 'build', '.git', '__pycache__', '.pytest_cache', '.vscode', 'lib', 'bin', 'pre_restructure_20241103_141411'}


def is_relevant_dir(path):
    """Check if a directory is relevant to the project."""
    return any(part in INCLUDED_DIRS for part in path.split(os.sep))


def is_relevant_file(filename):
    """Check if a file has a relevant extension."""
    return any(filename.endswith(ext) for ext in INCLUDED_EXTENSIONS)


def print_tree(directory, prefix='', output_file=None):
    """Recursively print the directory structure."""
    try:
        entries = sorted(os.listdir(directory))
        entries = [entry for entry in entries if entry not in EXCLUDED_DIRS]
        for index, entry in enumerate(entries):
            path = os.path.join(directory, entry)
            connector = '└── ' if index == len(entries) - 1 else '├── '

            if os.path.isdir(path):
                line = f"{prefix}{connector}{entry}/"
            elif os.path.isfile(path):
                last_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
                line = f"{prefix}{connector}{entry} (Last Modified: {last_modified_time})"
            else:
                continue

            if output_file:
                output_file.write(line + '\n')
            else:
                print(line)

            if os.path.isdir(path):
                if is_relevant_dir(path):
                    print_tree(path, prefix + ('    ' if connector == '└── ' else '│   '), output_file)
    except PermissionError:
        if output_file:
            output_file.write(f"{prefix}[Permission Denied]\n")
        else:
            print(f"{prefix}[Permission Denied]")


def get_last_modified_files(directory, num_files=10):
    """Get the last `num_files` modified files in the directory and subdirectories, excluding irrelevant directories and virtual environment content."""
    modified_files = []
    for root, dirs, files in os.walk(directory):
        # Filter out irrelevant directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith('venv')]
        for file in files:
            if is_relevant_file(file) and 'venv' not in root:
                path = os.path.join(root, file)
                last_modified_time = os.path.getmtime(path)
                modified_files.append((path, last_modified_time))

    # Sort files by last modified time, descending
    modified_files.sort(key=lambda x: x[1], reverse=True)
    return modified_files[:num_files]


if __name__ == "__main__":
    project_root = os.path.abspath('.')

    # Generate the complete project tree view
    output_file_path = os.path.join(project_root, 'project_tree_view_result.txt')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"Project structure of {project_root}:\n")
        print_tree(project_root, output_file=output_file)

    # Generate the last 10 modified files view, excluding irrelevant directories like 'venv'
    last_modified_files = get_last_modified_files(project_root, num_files=10)
    last_modified_output_path = os.path.join(project_root, 'project_tree_view_result_last_10_files_only.txt')
    with open(last_modified_output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Last 10 modified files in the project:\n")
        for path, mod_time in last_modified_files:
            formatted_time = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            output_file.write(f"{path} (Last Modified: {formatted_time})\n")

# End of File: project_structure_tree.py
# Location: root of your project directoryP