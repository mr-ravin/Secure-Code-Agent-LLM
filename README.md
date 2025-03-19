# Secure Code Agent 🤖 [Work in Progress]

## Overview
Secure Code Agent is a **LangChain-powered** LLM based automated code review and refactoring tool that:

✅ Scans for **security vulnerabilities** in source code files  
✅ Supports **Python, JavaScript, TypeScript, Java, C, and C++**  
✅ Refactors code to improve quality and maintainability based on detected security issues  
✅ Creates a **new GitHub branch and pull request (PR)** with improvements  
✅ **Optionally sends an email report** with findings and PR link  

## Features
- **Security Analysis**: Detects hardcoded credentials, weak cryptography, and insecure patterns using **Microsoft CodeBERT-Base**
- **Context-Aware Code Refactoring**: Improves structure, readability, and performance, fixing security vulnerabilities using **Gemma3:1B**
- **GitHub Integration**: Creates a new branch and submits a PR
- **Email Report**: Sends findings and PR details (if enabled)
- **Command-Line Interface**: Simple and easy to use

---
## 🔧 **Development Details**
- **👨‍💻 Developer:** [Ravin Kumar](https://mr-ravin.github.io)  
- **📂 GitHub Repository:** [https://github.com/mr-ravin/Secure-Code-Agent-LLM](https://github.com/mr-ravin/Secure-Code-Agent-LLM)

---
## File Structure
```
│──secure_code_agent/
|      │── config.sh               # Configurations and Credentials (GitHub, Email, etc.)
|      │── security_check.py       # Security vulnerability detection (uses CodeBERT-Base)
|      │── refactor.py             # Context-aware code refactoring (uses Gemma3:1B)
|      │── github_manager.py       # GitHub authentication & PR creation
|      │── email_report.py         # Email functionality
|      │── utils.py                # Helper functions
|
|── main.py                 # Entry point
│── requirements.txt        # Dependencies
│── README.md               # Documentation
```

## Supported Languages for Code review and Security Analysis
✅ Python (`.py`)
✅ JavaScript (`.js`)
✅ TypeScript (`.ts`)
✅ Java (`.java`)
✅ C (`.c`)
✅ C++ (`.cpp`)

## Security Analysis
The agent detects:
- Hardcoded **AWS & Google Cloud keys**
- **GitHub secrets**
- **SSH keys**
- **Weak cryptography & insecure coding practices**

## Security-Aware Refactoring
- **Fixes detected vulnerabilities** in the code automatically
- **Uses insights from CodeBERT** to guide Gemma3:1B for smart fixes
- **Enhances code maintainability** while keeping it secure

---
## Installation
Ensure you have **Python 3.8+** installed. Then, clone the repository and install dependencies:

```bash
# Clone the repository
git clone -b main https://github.com/mr-ravin/Secure-Code-Agent-LLM.git
cd Secure-Code-Agent-LLM

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
ollama pull gemma3:1b
```

```sh
ollama serve &
```

---
## Usage
Run the agent with the following command:

```bash
python main.py --path <repo_path> [--receiver_email <recipient>]
```

### Arguments
- `--path <repo_path>`: **(Required)** Path to the repository to analyze
- `--repo_url`: **(Optional)** GitHub repository URL, After `git clone` it will get stored at --path location
- `--branch_name`: **(Optional)** GitHub branch where AI agent will push the code (in the same repository)
- `--do_send_email`: **(Optional)** Send an email report when set `true`
- `--receiver_email <recipient>`: **(Optional)** Email recipient for the report (required if `--do_send_email` is `true`)

### Example
```bash
python main.py --path /path/to/repo --receiver_email user@example.com
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