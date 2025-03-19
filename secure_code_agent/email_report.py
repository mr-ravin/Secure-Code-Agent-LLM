import smtplib
import logging
from email.mime.text import MIMEText
import os

class EmailReporter:
    def send_report(self, recipient_email, findings, pr_link):
        try:
            content = f"Security scan completed.\nFindings: {findings}\nPull Request: {pr_link}"
            msg = MIMEText(content)
            msg["Subject"] = "Secure Code Agent Report"
            msg["From"] = os.getenv("EMAIL_SENDER")
            msg["To"] = recipient_email
            
            with smtplib.SMTP("smtp.example.com", 587) as server:
                server.starttls()
                server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
                server.sendmail(msg["From"], [recipient_email], msg.as_string())
            
            logging.info("Email sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")