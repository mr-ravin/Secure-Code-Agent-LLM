import os
import logging
import subprocess

def checkout_branch(repo_path, branch_name):
    try:
        subprocess.run(["git", "-C", repo_path, "checkout", branch_name], check=True)
        logging.info(f"Checked out to branch {branch_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to checkout branch {branch_name}: {e}")

def extract_json_code(response):
    """Extracts the refactored code from the JSON response."""
    try:
        return response.get("updated_code", "").strip()
    except Exception as e:
        logging.error(f"Failed to read refactored code.")
    
def extract_json_issue(response):
    """Extracts the security issues from the JSON response."""
    try:
        return response.get("security_issues", "").strip()
    except Exception as e:
        logging.error(f"Failed to read security issue.")  

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

def clone_repo(repo_url, repo_path, repo_branch="main"):
    if os.path.exists(repo_path):
        logging.info(f"Repository already exists at {repo_path}. Skipping clone.")
    else:
        logging.info(f"Cloning repository from {repo_url} to {repo_path}...")
        repo_url = repo_url.replace("https://", f"https://{os.getenv("GITHUB_TOKEN")}@")
        subprocess.run(["git", "clone", "-b", repo_branch, repo_url, repo_path], check=True)