import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg["From"] = "you@example.com"
    msg["To"] = to
    msg["Subject"] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("you@example.com", "PASSWORD")
        server.send_message(msg)

if __name__ == "__main__":
    send_email("test@example.com", "Hello", "This is automated.")