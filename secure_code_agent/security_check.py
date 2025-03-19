import re
from transformers import pipeline
import logging

class SecurityChecker:
    def __init__(self):
        self.detector = pipeline("text-classification", model="microsoft/codebert-base")
        self.sensitive_patterns = {
            "AWS Access Key": r"(?i)aws_access_key_id[\s=:\"]+([A-Z0-9]{20})",
            "AWS Secret Key": r"(?i)aws_secret_access_key[\s=:\"]+([A-Za-z0-9\/+=]{40})",
            "Google Cloud Key": r"(?i)google_cloud_key[\s=:\"]+([A-Za-z0-9-_]{30,50})",
            "S3 Bucket": r"(?i)s3_bucket[\s=:\"]+([A-Za-z0-9-_.]{3,63})",
            "API Key": r"(?i)api_key[\s=:\"]+([A-Za-z0-9-_]{20,50})",
            "Password": r"(?i)password[\s=:\"]+([A-Za-z0-9!@#$%^&*()_+={};:'\"<>,.?\/\\|`~-]{6,})",
            "Weak Encryption": r"(?i)(DES|MD5|RC4|SHA1)",
            "Lower Encryption Used": r"(?i)(AES-128|RSA-1024|3DES)"
        }

    def analyze(self, file_content):
        try:
            result = self.detector(file_content)
            classified_label = result[0]['label'] if result else "secure"
            # Check for sensitive data patterns
            issues = []
            for key, pattern in self.sensitive_patterns.items():
                if re.search(pattern, file_content):
                    logging.warning(f"Potential {key} exposure detected!")
                    issues.append(key)
            if issues:
                return f"Security issues detected: {', '.join(issues)}"
            return classified_label
        except Exception as e:
            logging.error(f"Security check failed: {e}")
            return "Error"