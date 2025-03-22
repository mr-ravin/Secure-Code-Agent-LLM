import requests
import os
import logging
from git import Repo, GitCommandError

class GitHubManager:
    def __init__(self, repo_url, repo_path, branch_name):
        self.repo = Repo(repo_path)
        self.branch_name = branch_name
        self.repo_url = repo_url.removesuffix(".git")
        self.remote_name = "origin"
        self.remote = None
        self.github_token = os.getenv("GITHUB_TOKEN")  # Fetch token from environment

    def local_commit(self, files, commit_message, message_clip_len=50):
        try:
            if not self.github_token:
                logging.error("GitHub token not found! Set GITHUB_TOKEN in environment variables.")
                return "GitHub token missing"
            if commit_message is None or len(commit_message)==0:
                commit_message = "Code Fixes done by Secure Code Tool"
            else:
                commit_message = commit_message[:message_clip_len]
            # Modify the repo URL to include the token for authentication
            auth_repo_url = self.repo_url.replace("https://", f"https://{self.github_token}@")

            # Set authenticated URL and fetch latest changes
            self.remote = self.repo.remote(self.remote_name)
            self.remote.set_url(auth_repo_url)
            self.remote.fetch()

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
            self.repo.index.commit(commit_message)

        except GitCommandError as e:
            logging.error(f"Git command failed: {e}")
            return "GitHub operation failed"
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return "GitHub operation failed"
    
    def do_push_and_pr(self, target_pr_branch):
        # Push changes to remote branch
        self.remote.push(refspec=f"{self.branch_name}:{self.branch_name}")

        # GitHub API to create PR
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        pr_data = {
            "title": f"PR: Merge {self.branch_name} into {target_pr_branch}",
            "head": self.branch_name,
            "base": target_pr_branch,
            "body": "This PR was created automatically.",
        }
        
        repo_name = self.repo_url.replace("https://github.com/", "").removesuffix(".git")  # Extract "owner/repo"
        pr_url = f"https://api.github.com/repos/{repo_name}/pulls"

        response = requests.post(pr_url, json=pr_data, headers=headers)

        if response.status_code == 201:
            logging.info(f"Pull Request created: {response.json()['html_url']}")
            return response.json()["html_url"]
        else:
            logging.error(f"Failed to create PR: {response.text}")
            return response.text