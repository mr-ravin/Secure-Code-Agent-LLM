import os
import logging
from git import Repo

class GitHubManager:
    def __init__(self, repo_path, branch_name):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        self.branch_name = branch_name

    def create_pr(self, files):
        try:
            if self.branch_name in self.repo.heads:
                branch = self.repo.heads[self.branch_name]
            else:
                branch = self.repo.create_head(self.branch_name)
            
            branch.checkout()

            for file_path, content in files.items():
                with open(file_path, "w") as f:
                    f.write(content)
                self.repo.index.add([file_path])
            
            commit_msg = "Auto-fix security vulnerabilities"
            self.repo.index.commit(commit_msg)
            self.repo.remote().push(refspec=f"{self.branch_name}:{self.branch_name}")
            
            repo_url = os.getenv("GITHUB_REPO_URL", f"https://github.com/{os.getenv('GITHUB_USER', 'user')}/{os.getenv('GITHUB_REPO', 'repo')}")
            return f"{repo_url}/compare/main...{self.branch_name}?expand=1"
        except Exception as e:
            logging.error(f"GitHub operation failed: {e}")
            return "GitHub operation failed"