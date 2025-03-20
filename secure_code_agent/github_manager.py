import os
import logging
from git import Repo, GitCommandError

class GitHubManager:
    def __init__(self, repo_url, repo_path, branch_name, target_pr_branch):
        self.repo = Repo(repo_path)
        self.branch_name = branch_name
        self.repo_url = repo_url
        self.remote_name = "origin"
        self.target_pr_branch = target_pr_branch
        self.github_token = os.getenv("GITHUB_TOKEN")  # Fetch token from environment

    def create_pr(self, files):
        try:
            if not self.github_token:
                logging.error("GitHub token not found! Set GITHUB_TOKEN in environment variables.")
                return "GitHub token missing"

            # Modify the repo URL to include the token for authentication
            auth_repo_url = self.repo_url.replace("https://", f"https://{self.github_token}@")

            # Set authenticated URL and fetch latest changes
            remote = self.repo.remote(self.remote_name)
            remote.set_url(auth_repo_url)
            remote.fetch()

            # Ensure the branch exists before checkout
            if self.branch_name not in [h.name for h in self.repo.heads]:
                self.repo.create_head(self.branch_name)
            
            # Checkout to the branch
            self.repo.git.checkout(self.branch_name)

            # Update files after checking out
            for file_path, content in files.items():
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.repo.index.add([file_path])

            self.repo.git.add(A=True)
            # Commit changes
            commit_msg = "Auto-fix security vulnerabilities"
            self.repo.index.commit(commit_msg)

            # Push changes using the authenticated URL
            remote.push(refspec=f"{self.branch_name}:{self.branch_name}")

            # Generate PR URL
            pr_url = f"{self.repo_url}/compare/{self.target_pr_branch}...{self.branch_name}?expand=1"
            logging.info(f"Pull Request URL: {pr_url}")
            logging.info("Success: GithubManager - Code Push and PR request.")
            return pr_url
        except GitCommandError as e:
            logging.error(f"Git command failed: {e}")
            return "GitHub operation failed"
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return "GitHub operation failed"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    repo_url = "https://github.com/mr-ravin/sample_code_review_check.git"
    repo_path = "/home/sparrow/Desktop/test_repo/"
    branch_name = "secure_code_agent_fixes"
    target_pr_branch = "main"
    
    github_manager = GitHubManager(repo_url, repo_path, branch_name, target_pr_branch)
    pr_link = github_manager.create_pr({'/home/sparrow/Desktop/test_repo/ravdec.py': 'print("Unit Testing: GitHub Manager")'})

    print(f"Pull Request Link: {pr_link}")