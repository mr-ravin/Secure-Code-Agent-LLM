import smtplib
import logging
from email.mime.text import MIMEText
import os

class EmailReporter:
    def send_report(self, recipient_email, findings, pr_link, smtp_url, smtp_port):
        try:
            if os.getenv("EMAIL_SENDER") is None:
                logging.error(f"Failed to fetch email address from environment variables.")
                return
            content = f"Security scan completed.\nFindings: {findings}\nPull Request: {pr_link}"
            msg = MIMEText(content)
            msg["Subject"] = "Secure Code Agent Report"
            msg["From"] = os.getenv("EMAIL_SENDER")
            msg["To"] = recipient_email
            logging.info("Initiating email sending.")
            with smtplib.SMTP(smtp_url, smtp_port) as server:
                server.starttls()
                server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
                server.sendmail(msg["From"], [recipient_email], msg.as_string())
            logging.info("Success: Email sent.")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")