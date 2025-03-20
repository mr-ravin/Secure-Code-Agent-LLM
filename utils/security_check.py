import re
import logging

class SecurityChecker:
    def __init__(self):
        self.sensitive_patterns = {
            "AWS Access Key Found": r"(?i)aws_access_key_id[\s=:\"]+([A-Z0-9]{20,})",
            "AWS Secret Key Found": r"(?i)aws_secret_access_key[\s=:\"]+([A-Za-z0-9\/+=]{20,})",
            "Google Cloud Key Found": r"(?i)google_cloud_key[\s=:\"]+([A-Za-z0-9-_]{30,50})",
            "S3 Bucket Found": r"(?i)s3_bucket[\s=:\"]+([A-Za-z0-9-_.]{3,63})",
            "API Key Found": r"(?i)api_key[\s=:\'\"]+([A-Za-z0-9-_]{15,50})",
            "Password Found": r"(?i)password[\s=:\"]+([A-Za-z0-9!@#$%^&*()_+={};:'\"<>,.?\/\\|`~-]{5,})",
            "SSH Private Key Found": r"-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----[\s\S]+?-----END (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----",
            "Weak Encryption Found": r"(?i)(DES|MD5|RC4|SHA1)",
            "Lower Encryption Found": r"(?i)(AES-128|RSA-1024|3DES)"
        }

    def analyze(self, file_content):
        logging.info("Initiated: Tool - Security Scan")
        try:
            issues = []
            # Check for sensitive data patterns
            for key, pattern in self.sensitive_patterns.items():
                if re.search(pattern, file_content):
                    logging.warning(f"Potential {key} exposure detected!")
                    issues.append(key)
            if len(issues)>0:
                logging.info("Success: Tool - Security Scan")
                return f"\nIdentified Security Issues: {', '.join(issues)}\n"
            else:
                logging.info("Success: Tool - Security Scan")
                return f"\nIdentified Security Issues: No issues found\n"
        except Exception as e:
            logging.error(f"Security check failed: {e}")
            return f"Identified Issues: Security check failed"
