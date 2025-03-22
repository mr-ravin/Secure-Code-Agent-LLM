# Secure Code Tool - LLM 🤖

## Overview
Secure Code Tool is a **LangChain-powered** LLM based automated code review and refactoring tool that:

✅ Scans for **security vulnerabilities** in source code files

✅ Supports **Python, JavaScript, TypeScript, Java, C, and C++** (Depends on which LLM one is using, we are using `gemma3:12b`)

✅ Refactors code to improve quality and maintainability based on detected security issues

✅ Creates a **new GitHub branch and pull request (PR)** with improvements  

✅ **Optionally sends an email report** with findings and PR link  

## Features
- **Security Analysis**: Detects hardcoded credentials, weak cryptography, and insecure patterns.
- **Context-Aware Code Refactoring**: Improves structure, readability, and performance while fixing security vulnerabilities using `gemma3:12b`.
- **AI-Powered Code Suggestions**: Uses `gemma3:12b` LLM model for intelligent security fixes and best-practice improvements.
- **GitHub Integration**: Automatically creates a new branch and submits a PR with fixes.
- **Email Report**: Sends findings and PR details (if enabled).
- **Command-Line Interface**: Simple and easy to use.
- **Multi-Language Support**: Supports Python, JavaScript, TypeScript, Java, C, and C++.
- **Configurable Rules**: Custom regex patterns for detecting secrets and insecure practices.
- **Logging & Auditing**: Generates logs for audit trails and compliance tracking.
- **Auto-Commit & Push**: Automatically commits refactored code and security fixes before PR creation.
- **Extensibility**: Easy to add new security rules and language support.

---
## 🔧 **Development Details**
- **👨‍💻 Developer:** [Ravin Kumar](https://mr-ravin.github.io)  
- **📂 GitHub Repository:** [https://github.com/mr-ravin/Secure-Code-Tool-LLM](https://github.com/mr-ravin/Secure-Code-Tool-LLM)

---
#### Important: 

Secure-Code-Tool-LLM utilized approximately 12GB of GPU memory and 9GB of RAM. It's Git repository was first cloned into the Lightning.ai environment, after which the Ollama server was launched with `gemma3:12b` model on the GPU.

In case one have better hardware resources available, can try with more powerful LLMs available on `Ollama` like: `gemma3:27b`, `llama3:8b`, `llama3:70b`, `mistral` etc. A model can be easily changed with `--ollama_model` flag in `main.py` once it is pulled on Ollama Server `ollama pull < model name:<version> >`. Or, 

Use any other LLM library (but, might need API Access) and some changes in `main.py` file based on prompt template and API.

---
## File Structure
```
|── main.py                        # Entry point (LLM)
│── requirements.txt               # Dependencies
|
│──utils/
|      │── config.sh               # Configurations and Credentials (GitHub, Email, etc.)
|      │── security_check.py       # Security vulnerability detection (rule-based)
|      │── github_manager.py       # GitHub authentication & PR creation
|      │── email_report.py         # Email functionality
|      │── operations.py           # Helper functions
|
│── README.md                      # Documentation
```

---
## Supported Languages for Code review and Security Analysis (Depends on which LLM one uses)

✅ Python (`.py`)

✅ JavaScript (`.js`)

✅ TypeScript (`.ts`)

✅ Java (`.java`)

✅ C (`.c`)

✅ C++ (`.cpp`)

---
## Security Analysis
The tool detects:
- Hardcoded **AWS & Google Cloud keys**
- **GitHub secrets**
- **SSH keys**
- **Weak cryptography & insecure coding practices**

## Security-Aware Refactoring
- **Fixes detected vulnerabilities** in the code automatically
- **Uses insights from SecurityChecker** to guide gemma3:12b for smart fixes
- **Enhances code maintainability** while keeping it secure

---
## Installation
Ensure you have **Python 3.8+** installed. Then, clone the repository and install dependencies:

```bash
# Clone the repository
git clone -b main https://github.com/mr-ravin/Secure-Code-Tool-LLM.git
cd Secure-Code-Tool-LLM

# Install dependencies
pip install -r requirements.txt
```

### Installing and running Ollama Server (ollama version is 0.6.1)
- Install Ollama Server:
```sh
curl -fsSL https://ollama.com/install.sh | sh
```
- Ensure the LLM is present inside the Ollama Server:
```sh
ollama pull gemma3:12b
```

```sh
ollama serve &
```

---
## Usage
- Initialise the login credentials in environment variables:

```bash
source ./utils/config.sh 
```

- Run the tool with the following command:

```bash
python main.py --path < LocalPath > --repo_url < RepoOfCodeToBeReviewed.git >  --receiver_email < RecipientEmail >
```

### Arguments

- `--path <repo_path>`: **(Required)** Local path to the code repository to be  reviewed and fixed by AI Tool
- `--repo_url`: **(Optional)** GitHub repository URL of Code repository to be reviewed and fixed by AI Tool. After performing `git clone` this repository will get stored at the location specified in `--path`
- `--repo_branch`: **(Optional)** Branch name of GitHub repository URL of the code to be reviewed and refactored. Default value is `main`
- `--tool_branch_name`: **(Optional)** GitHub branch where AI tool will push the code (in the same repository)
- `--pr_branch_name`: **(Optional)** GitHub branch where AI tool will raise the PR request. Default value is `main`
- `--do_send_email`: **(Optional)** Send an email report when set `true`. Default value is `true`
- `--receiver_email <recipient>`: **(Optional)** Email recipient for the report (required if `--do_send_email` is `true`)
- `--smtp_url`: **(Optional)** Url of SMTP Server. Default value is `smtp.gmail.com`
- `--smtp_port`: **(Optional)** Port number of SMTP Server. Default value is `587`
- `--ollama_model`: **(Optional)** LLM to be used from Ollama Server. Default is `gemma3:12b`
- `--ollama_ip`: **(Optional)** Url of Ollama Server. Default value is `localhost`
- `--ollama_port`: **(Optional)** Port number of Ollama Server. Default value is `11434`

### Example
```bash
python main.py --path /path/to/repo --receiver_email user@example.com
```
Or,
```bash
python main.py --path /teamspace/studios/this_studio/test/ --repo_url https://github.com/mr-ravin/code_testing.git --do_send_email true --receiver_email < UseReceiverEmail@website.com > --ollama_model gemma3:12b
```

## License
```sh
Copyright (c) 2025 Ravin Kumar
Website: https://mr-ravin.github.io

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the 
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
