from transformers import pipeline
import logging

class CodeRefactor:
    def __init__(self):
        self.refactorer = pipeline("text2text-generation", model="gemma3:1b", framework="pt")

    def refactor(self, file_content, issues):
        try:
            prompt = f"Fix security issues in the following code: {file_content}\nIssues: {issues}"
            result = self.refactorer(prompt)
            return result[0]['generated_text'] if result else file_content
        except Exception as e:
            logging.error(f"Refactoring failed: {e}")
            return file_content