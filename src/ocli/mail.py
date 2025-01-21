import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from .env
SENDER_EMAIL = os.getenv("ZOHO_EMAIL")
SENDER_PASSWORD = os.getenv("ZOHO_PASSWORD")

def send_zoho_email(recipient_email: str, subject: str, body: str) -> str:
    """
    Sends an email using Zoho's SMTP server with pre-configured sender credentials.
    
    Args:
        recipient_email (str): Recipient's email address.
        subject (str): Email subject.
        body (str): Email body.
    
    Returns:
        str: A success message or an error message if the email fails to send.
    """
    smtp_server = "smtp.zoho.com"
    smtp_port = 587  # You can also use port 465 for SSL
    
    # Create the email message
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS
        
        # Login to the server
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send email
        server.send_message(message)
        return f"Email sent successfully to {recipient_email}!"
    
    except Exception as e:
        return f"An error occurred: {e}"
    
    finally:
        server.quit()




