import argparse
import logging
from utils.security_check import SecurityChecker
from utils.github_manager import GitHubManager
from utils.email_report import EmailReporter
from utils.operations import load_repo_files, clone_repo, extract_json_code, checkout_branch, extract_json_issue, extract_json_solution, extract_json_summary, llm_output_json
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
    parser.add_argument("--ollama_model", default="gemma3:12b", help="LLM to be used from Ollama Server")
    parser.add_argument("--ollama_ip", default="localhost", help="Url of Ollama Server")
    parser.add_argument("--ollama_port", default="11434", help="Port number of Ollama Server")
    args = parser.parse_args()
    logging.info("Initiated: Task for Secure Code Tool - LLM")
    if args.do_send_email.lower() in ["true", "yes"] and len(args.receiver_email) == 0:
        logging.error("Error: --receiver_email argument is required when --do_send_email is set true")
        return
    format_schema = {
        "type": "object",
        "properties": {
            "updated_code": {"type": "string"},
            "security_issue": {"type": "string"},
            "security_solution": {"type": "string"}
        },
        "required": ["updated_code", "security_issue", "security_solution"]
    }

    summary_schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
        },
        "required": ["summary"]
    }

    # Initialize LLM
    llm = OllamaLLM(model=args.ollama_model, base_url="http://"+args.ollama_ip+":"+args.ollama_port, temperature=0.0)

    if args.repo_url:
        clone_repo(args.repo_url, args.path, args.repo_branch)

    repo_path = args.path
    
    checkout_branch(repo_path, args.repo_branch)  # Checkout to the specified branch before reading files
    files = load_repo_files(repo_path)   
    findings_collection = []
    commit_collection = []
    github_manager = GitHubManager(repo_url=args.repo_url, repo_path=repo_path, branch_name=args.tool_branch_name)
    for file, content in files.items():
        # Step 1: First, invoke the Security Scan tool directly
        security_issues = security_scan_tool(content)
        response = llm.invoke(f"""
Thought: Given the Identified Security Issues and the code, We must fix the given Security Issues and refactor the code. 


{security_issues}


Action:
1. If Identified Security Issues is not 'No issues found', then fix the Security Issues in the code. 
2. Refactor the code while maintaining all the existing functionalities of the code.
3. Improve readability of the code by adding appropriate docstrings and comments (if necessary).           
4. Enhance modularity and maintainability of the code.

**Respond ONLY in valid JSON format. Do not use Markdown (` ```json `), No explanations, no markdown, no additional text.**  

Instruction:             
1. **The value of "updated_code must be the complete source code without any Markdown ``` and DO not replace any part with ellipses (`...`)""**
2. **Respond strictly in JSON format** — do not include any Markdown, explanations, or extra text.  
3. **Ensure all three keys ("updated_code", "security_issue", and "security_solution") are present in the final response.**  
4. **If any key is missing is your response then regenerate the response till you get all the three keys i.e. "updated_code", "security_issue" and "security_solution".**  
5. **JSON must contain the exact same keys and structure as mentioned below**. 

{{
    "updated_code": "<your code here, DO not replace any part with ellipses (`...`)>",
    "security_issue": "<your one line detail_of the code vulnerability and issues here>",
    "security_solution": "<your one line short-detail of the code fixes here>"
}}


### Code:
{content}
""", format=format_schema)
        # Clean response: Remove Markdown formatting if present
        response = llm_output_json(response)
        security_issues = extract_json_issue(response)
        commit_message = extract_json_solution(response)
        commit_collection.append(commit_message)
        refactored_file_content = extract_json_code(response)
        findings_collection.append("File: "+file+"\nSecurity Issue: "+security_issues+"\n\nDetails: "+commit_message+"\n\n-----\n\n")
        # Perform local git commit for each file.
        github_manager.local_commit({file: refactored_file_content}, commit_message)
    findings_string = "\n".join(findings_collection)
    commit_string = "\n".join(commit_collection)
    logging.info("Initiated: GithubManager - Code Push and PR request.")
    generated_summary_json = llm.invoke(f"""
Thought: Given the DESCRIPTION, generate a precise one line <summary> of it.

Action: Read Descrption and generate its precise <summary> in one line. 
    
**Respond ONLY in valid JSON format mentioned below. No explanations, No description, No markdown, No additional text. Respond back only in the JSON Structure. Final code should be put in JSON only. No need for any other detail.** 

{{
        "summary": "<Mention your summary unambiguously and precisely in one line.>"
}}


### DESCRIPTION:
{commit_string}
""", format=summary_schema)
    generated_summary_json = llm_output_json(generated_summary_json)
    generated_summary = extract_json_summary(generated_summary_json)
    # Perform git commit and get link of PR
    pr_link = github_manager.do_push_and_pr(args.pr_branch_name)
    if args.do_send_email.lower() in ["true", "yes"]:
        logging.info("Initiated EmailReporter.")
        reporter = EmailReporter()
        
        reporter.send_report(args.receiver_email, generated_summary, findings_string, pr_link, args.smtp_url, int(args.smtp_port))
    logging.info("Success: Task for Secure Code Tool - LLM")

if __name__ == "__main__":
        main()