import argparse
import logging
from secure_code_agent.security_check import SecurityChecker
from secure_code_agent.github_manager import GitHubManager
from secure_code_agent.email_report import EmailReporter
from secure_code_agent.utils import load_repo_files, clone_repo, extract_json_code, checkout_branch, extract_json_issue
from langchain_ollama import OllamaLLM
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType

def security_scan_tool(code: str):
    security_checker = SecurityChecker()
    return security_checker.analyze(code)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')    
    parser = argparse.ArgumentParser(description="Secure Code Agent")
    parser.add_argument("--repo_url", help="GitHub repository URL of Code (optional)")
    parser.add_argument("--repo_branch", default="main", help="Branch name of GitHub repository URL of Code (optional, but used when --repo_url is used)")
    parser.add_argument("--path", required=True, help="Path to the repository of Code")
    parser.add_argument("--agent_branch_name", default="secure_code_agent_fixes", help="Branch where AI agent will push the code")
    parser.add_argument("--pr_branch_name", default="main", help="Branch where AI agent will raise the PR request")
    parser.add_argument("--do_send_email", default="true", help="Send email report if set true")
    parser.add_argument("--receiver_email", default="", help="Recipient email (required if --do_send_email is set true)")
    parser.add_argument("--smtp_url", default="smtp.gmail.com", help="Url of SMTP Server")
    parser.add_argument("--smtp_port", default="587", help="Port number of SMTP Server")
    parser.add_argument("--ollama_model", default="gemma3:1b", help="LLM to be used from Ollama Server")
    parser.add_argument("--ollama_ip", default="localhost", help="Url of Ollama Server")
    parser.add_argument("--ollama_port", default="11434", help="Port number of Ollama Server")
    args = parser.parse_args()
    logging.info("Initiated: Task for Secure Code Agent - LLM")
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

    security_tool = Tool(
        name="Security Scan",
        func=security_scan_tool,
        description="Scans code for security vulnerabilities and issues using microsoft/codebert-base model"
    )
    
    agent = initialize_agent(
        tools=[security_tool],
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    refactored_files = {}
    findings = []
    for file, content in files.items():
            response = agent.invoke(f"""Thought: The provided code might contains security issues that need to be checked using the locally hosted microsoft/codebert-base model. Then fix all the security issues reported by locally hosted microsoft/codebert-base model. 
Additionally, improvements in readability, modularity, and maintainability might be beneficial.

Action: First perform security scan on code using only the locally hosted microsoft/codebert-base model to know the present securiy issues. Then, Refactor the code to resolve the identified security issues, if it was not Secure. If necessary, improve code readability by adding appropriate docstrings and comments. 
Consider enhancing modularity and maintainability while ensuring the original functionality remains intact.

Respond strictly in the following JSON format:
```json
{{ "updated_code": "<Your refactored code here>" "security_issues": <Detected security issues before refactor here>}}
```

### Code:
{content}
""")
            refactored_files[file] = extract_json_code(response)
            findings.append(file+" : "+ extract_json_issue(response))
    logging.info("Initiated: GithubManager - Code Push and PR request.")
    github_manager = GitHubManager(args.repo_url, repo_path, args.agent_branch_name, args.pr_branch_name)
    pr_link = github_manager.create_pr(refactored_files)
    
    if args.do_send_email.lower() in ["true", "yes"]:
        logging.info("Initiated EmailReporter.")
        reporter = EmailReporter()
        findings = ",".join(findings)
        reporter.send_report(args.receiver_email, findings, pr_link, args.smtp_url, int(args.smtp_port))
    logging.info("Success: Task for Secure Code Agent - LLM")

if __name__ == "__main__":
        main()