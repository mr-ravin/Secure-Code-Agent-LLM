import argparse
import logging
from utils.security_check import SecurityChecker
from utils.github_manager import GitHubManager
from utils.email_report import EmailReporter
from utils.operations import load_repo_files, clone_repo, extract_json_code, checkout_branch, extract_json_issue, llm_output_json
from langchain_ollama import OllamaLLM

def security_scan_tool(code: str):
    security_checker = SecurityChecker()
    return security_checker.analyze(code)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    
    parser = argparse.ArgumentParser(description="Secure Code Tool")
    parser.add_argument("--repo_url", help="GitHub repository URL of Code (optional)")
    parser.add_argument("--repo_branch", default="main", help="Branch name of GitHub repository URL of Code (optional, but used when --repo_url is used)")
    parser.add_argument("--path", required=True, help="Path to the repository of Code")
    parser.add_argument("--tool_branch_name", default="secure_code_tool_fixes", help="Branch where AI tool will push the code")
    parser.add_argument("--pr_branch_name", default="main", help="Branch where AI tool will raise the PR request")
    parser.add_argument("--do_send_email", default="true", help="Send email report if set true")
    parser.add_argument("--receiver_email", default="", help="Recipient email (required if --do_send_email is set true)")
    parser.add_argument("--smtp_url", default="smtp.gmail.com", help="Url of SMTP Server")
    parser.add_argument("--smtp_port", default="587", help="Port number of SMTP Server")
    parser.add_argument("--ollama_model", default="gemma3:1b", help="LLM to be used from Ollama Server")
    parser.add_argument("--ollama_ip", default="localhost", help="Url of Ollama Server")
    parser.add_argument("--ollama_port", default="11434", help="Port number of Ollama Server")
    args = parser.parse_args()
    logging.info("Initiated: Task for Secure Code Tool - LLM")
    if args.do_send_email.lower() in ["true", "yes"] and len(args.receiver_email) == 0:
        logging.error("Error: --receiver_email argument is required when --do_send_email is set true")
        return

    # Initialize LLM
    llm = OllamaLLM(model=args.ollama_model, base_url="http://"+args.ollama_ip+":"+args.ollama_port)

    if args.repo_url:
        clone_repo(args.repo_url, args.path, args.repo_branch)

    repo_path = args.path
    
    checkout_branch(repo_path, args.repo_branch)  # Checkout to the specified branch before reading files
    files = load_repo_files(repo_path)
    
    refactored_files = {}
    findings = []
    for file, content in files.items():
        # Step 1: First, invoke the Security Scan tool directly
        security_issues = security_scan_tool(content)
        response = llm.invoke(f"""
Thought: Given the Identified Security Issues and the code, We must fix the given Security Issues and refactor the code. 

{security_issues}

Action: 
1. If Identified Security Issues is not 'No issues found', then fix the Security Issues in the code. 
2. Refactor the code while maintaining the functionality in the code.
2. Improve readability of the code by adding appropriate docstrings and comments (if necessary).           
3. Enhance modularity and maintainability of the code.            
             
**Respond ONLY in valid JSON format. Do not use Markdown (` ```json `), No explanations, no markdown, no additional text.**  

{{
    "updated_code": "<Your refactored code here>",
    "security_issues": "<Given Identified Security Issues before refactoring step>"
}}


### Code:
{content}
""")
        # Clean response: Remove Markdown formatting if present
        response = llm_output_json(response)
        security_issues = extract_json_issue(response)
        refactored_files[file] = extract_json_code(response)
        findings.append(file+" : "+ "fixed: "+security_issues)
    logging.info("Initiated: GithubManager - Code Push and PR request.")
    github_manager = GitHubManager(args.repo_url, repo_path, args.tool_branch_name, args.pr_branch_name)
    pr_link = github_manager.create_pr(refactored_files)
    
    if args.do_send_email.lower() in ["true", "yes"]:
        logging.info("Initiated EmailReporter.")
        reporter = EmailReporter()
        findings = "\n".join(findings)
        reporter.send_report(args.receiver_email, findings, pr_link, args.smtp_url, int(args.smtp_port))
    logging.info("Success: Task for Secure Code Tool - LLM")

if __name__ == "__main__":
        main()