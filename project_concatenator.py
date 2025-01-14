import os
import argparse

# Directories to exclude anywhere in the path
EXCLUDED_DIRS = {".git", ".idea", ".terraform"}


def has_excluded_dir(path_str: str, excluded_dirs: set) -> bool:
    """
    Returns True if any component of path_str matches
    one of the excluded_dirs.
    """
    parts = os.path.abspath(path_str).split(os.sep)
    return any(part == ex for part in parts for ex in excluded_dirs)


def parse_arguments():
    """
    Parses command-line arguments for the script.

    Returns:
        Namespace: Parsed arguments including directory, file types, and output file path.
    """
    parser = argparse.ArgumentParser(description="Aggregate file contents based on types.")
    parser.add_argument(
        '-d', '--directory',
        help="Directory to search. Defaults to the current directory."
    )
    parser.add_argument(
        '-t', '--types',
        nargs='+',
        help="List of file types to include (e.g., txt, py, yml). Defaults to [py, txt, yml]."
    )
    parser.add_argument(
        '-o', '--output',
        help="Path to the output file. Defaults to 'concatenated_project.txt' in the current directory."
    )
    return parser.parse_args()


def search_files(base_path, file_types, exclude_files):
    """
    Recursively searches for files matching the given types in the specified path.

    Args:
        base_path (str): Directory path to search in.
        file_types (list of str): List of file extensions or file names to match.
        exclude_files (list of str): List of files to exclude from the results.

    Returns:
        list of lists: A list where each element is a list containing files of a certain type.
    """
    files_by_type = [[] for _ in file_types]

    for root, _, files in os.walk(base_path):
        # Skip the entire directory if it's under an excluded path
        if has_excluded_dir(root, EXCLUDED_DIRS):
            continue

        for file in files:
            file_path = os.path.join(root, file)
            # Skip excluded files or paths containing excluded dirs
            if file_path in exclude_files or has_excluded_dir(file_path, EXCLUDED_DIRS):
                continue

            for i, file_type in enumerate(file_types):
                # Match if file ends with .<file_type> or equals <file_type>
                if file.endswith(f".{file_type}") or file == file_type:
                    files_by_type[i].append(file_path)

    # Sort each list to maintain a consistent order
    for file_list in files_by_type:
        file_list.sort()

    return files_by_type


def create_aggregated_file(files_by_type, output_file):
    """
    Creates a new text file with the contents of all files in files_by_type.

    Args:
        files_by_type (list of lists): A list of lists of file paths to read.
        output_file (str): The path to the output text file.
    """
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for file_list in files_by_type:
            for file_path in file_list:
                try:
                    with open(file_path, 'r', encoding='utf-8') as in_file:
                        content = in_file.read()
                        out_file.write("-" * 60 + "\n")
                        out_file.write(f"File Path = {file_path}\n")
                        out_file.write(f"File Name = {os.path.basename(file_path)}\n\n")
                        out_file.write(content + "\n")
                except Exception as e:
                    out_file.write(f"Error reading {file_path}: {e}\n")


def append_directory_structure(file_paths, base_path, output_file):
    """
    Appends the directory structure in a tree-like format to the output file,
    including only the files in file_paths and skipping excluded directories.

    Args:
        file_paths (list of str): List of file paths to include in the directory structure.
        base_path (str): The base directory path to print the structure for.
        output_file (str): The path to the output text file.
    """
    file_paths_set = set(file_paths)

    def walk_dir(path, prefix=""):
        # Only show items that are:
        #   1. In file_paths_set or are directories
        #   2. NOT under an excluded directory path
        contents = []
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            if has_excluded_dir(full_path, EXCLUDED_DIRS):
                continue
            if full_path in file_paths_set or os.path.isdir(full_path):
                contents.append(name)

        # Create pointers for tree-like visualization
        pointers = ["├── "] * (len(contents) - 1) + ["└── "] if contents else []
        for pointer, name in zip(pointers, contents):
            full_path = os.path.join(path, name)
            with open(output_file, 'a', encoding='utf-8') as out_file:
                out_file.write(f"{prefix}{pointer}{name}\n")
            # Recurse into directories
            if os.path.isdir(full_path):
                extension = "│   " if pointer == "├── " else "    "
                walk_dir(full_path, prefix=prefix + extension)

    # Append a header
    with open(output_file, 'a', encoding='utf-8') as out_file:
        out_file.write("-" * 60 + "\n")
        out_file.write("Directory Structure\n")

    walk_dir(base_path)


def main():
    args = parse_arguments()

    directory = args.directory if args.directory else os.getcwd()
    file_types = args.types if args.types else ['py', 'txt', 'yml', 'Dockerfile', 'init.sql', 'README.md', 'tf']
    output_file = args.output if args.output else os.path.join(os.getcwd(), 'concatenated_project.txt')

    # Exclude the output file and the script file itself
    script_file = os.path.abspath(__file__)
    exclude_files = [output_file, script_file]

    # 1) Search and filter out excluded files
    files_by_type = search_files(directory, file_types, exclude_files=exclude_files)

    # 2) Flatten files_by_type to a single list
    all_files = [f for file_list in files_by_type for f in file_list]

    # 3) Create the aggregated file from matching files
    create_aggregated_file(files_by_type, output_file)

    # 4) Append the directory structure, skipping excluded directories
    append_directory_structure(all_files, directory, output_file)

    print(f"Aggregated file created at {output_file}")


if __name__ == "__main__":
    main()
