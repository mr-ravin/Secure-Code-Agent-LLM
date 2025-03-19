import os
import logging

def load_repo_files(repo_path):
    supported_extensions = [".py", ".js", ".ts", ".java", ".c", ".cpp"]
    files = {}
    try:
        for root, _, filenames in os.walk(repo_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if any(file_path.endswith(ext) for ext in supported_extensions):
                    with open(file_path, "r", encoding="utf-8") as f:
                        files[file_path] = f.read()
        return files
    except Exception as e:
        logging.error(f"Failed to load repository files: {e}")
        return {}