import smtplib
import os
import csv
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def create_email(to, subject, body, html=False, attachments=None):
    """Create a MIME email message with optional HTML and attachments."""
    msg = MIMEMultipart()
    msg["From"] = formataddr(("Sender Name", EMAIL_ADDRESS))
    msg["To"] = ", ".join(to) if isinstance(to, list) else to
    msg["Subject"] = subject

    if html:
        msg.attach(MIMEText(body, "html"))
    else:
        msg.attach(MIMEText(body, "plain"))

    if attachments:
        for file_path in attachments:
            try:
                with open(file_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                msg.attach(part)
            except Exception as e:
                logging.warning(f"Failed to attach {file_path}: {e}")

    return msg

def send_email(to, subject, body, html=False, attachments=None):
    """Send an email via SMTP with retries and logging."""
    msg = create_email(to, subject, body, html, attachments)
    for attempt in range(3):
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            logging.info(f"Email sent to {to}")
            return True
        except smtplib.SMTPException as e:
            logging.warning(f"Attempt {attempt+1} failed: {e}")
    logging.error(f"Failed to send email to {to} after 3 attempts")
    return False

def send_bulk_from_csv(csv_file):
    """Send emails to multiple recipients from a CSV with columns: email, subject, body"""
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            send_email(row["email"], row["subject"], row["body"])

if __name__ == "__main__":
    send_email(
        to=["test@example.com"],
        subject="Hello from Automation",
        body="<h2>This is an automated HTML email!</h2>",
        html=True,
        attachments=["example.pdf"]
    )
