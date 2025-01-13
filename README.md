# File Aggregator

## Description
The File Aggregator is a Python utility designed to search for files of specific types in a directory, aggregate their contents into a single text file, and append a tree-like directory structure showing only the relevant files. It provides a convenient way to consolidate and review project files.

## Features
- Recursively searches for files of specified types within a directory.
- Aggregates file contents into a single output file with clear separation between file entries.
- Excludes certain directories (e.g., `.git` and `.idea`) from the directory structure.
- Appends a tree-like directory structure of the aggregated files to the output file.

## Usage

### Command-line Arguments

The script accepts the following optional arguments:

- `-d`, `--directory`: The directory to search. Defaults to the current working directory.
- `-t`, `--types`: A list of file types (extensions) to include (e.g., `txt`, `py`, `yml`). Defaults to `['py', 'txt', 'yml']`.
- `-o`, `--output`: The path to the output file. Defaults to `concatenated_project.txt` in the current working directory.

### Example
```bash
python file_aggregator.py -d /path/to/project -t py txt yml -o output.txt
```
This command will:
1. Search the `/path/to/project` directory for `.py`, `.txt`, and `.yml` files.
2. Aggregate their contents into `output.txt`.
3. Append the directory structure of the aggregated files to `output.txt`.

### Output Format

The output file will have the following structure:

```
------------------------------
File Path = /path/to/file.py
File Name = file.py

<Contents of file.py>

------------------------------
Directory Structure
/path/to/project
├── file.py
├── subdirectory
│   ├── file1.txt
│   └── file2.yml
└── another_file.txt
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your_username>/file-aggregator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd file-aggregator
   ```

## Requirements
- Python 3.6 or higher


