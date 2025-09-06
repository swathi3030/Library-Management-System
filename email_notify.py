import smtplib
from email.message import EmailMessage
from logger import get_logger

logger = get_logger(__name__)

def send_new_book_email(book_title, recipient):
    try:
        msg = EmailMessage()
        msg.set_content(f"New book '{book_title}' added to the library.")
        msg["Subject"] = "Library Notification: New Book"
        msg["From"] = "swathimanjappa9@example.com"
        msg["To"] = recipient

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("swathimanjappa9@example.com", "app-password")
            server.send_message(msg)
        logger.info(f"Email sent for {book_title} to {recipient}")
    except Exception as e:
        logger.error(f"Email send failed: {e}")
