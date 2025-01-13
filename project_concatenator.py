import os
import argparse


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
        for file in files:
            file_path = os.path.join(root, file)
            if file_path in exclude_files:
                continue
            for i, file_type in enumerate(file_types):
                if file.endswith(f".{file_type}") or file == file_type:
                    files_by_type[i].append(file_path)

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
                        out_file.write("-" * 100 + "\n")
                        out_file.write(f"File Path = {file_path}\n")
                        out_file.write(f"File Name = {os.path.basename(file_path)}\n\n")
                        out_file.write(content + "\n")
                except Exception as e:
                    out_file.write(f"Error reading {file_path}: {e}\n")


def append_directory_structure(file_paths, base_path, output_file):
    """
    Appends the directory structure in a tree-like format to the output file, including only the files in file_paths.

    Args:
        file_paths (list of str): List of file paths to include in the directory structure.
        base_path (str): The base directory path to print the structure for.
        output_file (str): The path to the output text file.
    """
    file_paths = set(file_paths)

    def walk_dir(path, prefix=""):
        contents = [
            name for name in os.listdir(path)
            if (os.path.join(path, name) in file_paths or os.path.isdir(os.path.join(path, name)))
               and ".git" not in name and ".idea" not in name
        ]
        pointers = ["├── "] * (len(contents) - 1) + ["└── "]
        for pointer, name in zip(pointers, contents):
            full_path = os.path.join(path, name)
            with open(output_file, 'a', encoding='utf-8') as out_file:
                out_file.write(f"{prefix}{pointer}{name}\n")
            if os.path.isdir(full_path):
                extension = "│   " if pointer == "├── " else "    "
                walk_dir(full_path, prefix=prefix + extension)

    with open(output_file, 'a', encoding='utf-8') as out_file:
        out_file.write("-" * 30 + "\n")
        out_file.write("Directory Structure\n")
    walk_dir(base_path)


def main():
    args = parse_arguments()

    directory = args.directory if args.directory else os.getcwd()
    file_types = args.types if args.types else ['py', 'txt', 'yml', 'Dockerfile', 'init.sql']
    output_file = args.output if args.output else os.path.join(os.getcwd(), 'concatenated_project.txt')

    # Exclude the output file and the script file itself
    script_file = os.path.abspath(__file__)
    exclude_files = [output_file, script_file]

    files_by_type = search_files(directory, file_types, exclude_files=exclude_files)

    # Flatten files_by_type to get a single list of all files
    all_files = [file for file_list in files_by_type for file in file_list]

    create_aggregated_file(files_by_type, output_file)
    append_directory_structure(all_files, directory, output_file)
    print(f"Aggregated file created at {output_file}")


if __name__ == "__main__":
    main()

