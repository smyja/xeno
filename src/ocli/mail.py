import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_zoho_email(sender_email, sender_password, recipient_email, subject, body):
    # Zoho SMTP server settings
    smtp_server = "smtp.zoho.com"
    smtp_port = 587  # You can also use port 465 for SSL
    
    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS
        
        # Login to the server
        server.login(sender_email, sender_password)
        
        # Send email
        server.send_message(message)
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        server.quit()

# Example usage
if __name__ == "__main__":
    # Replace these with your actual credentials and message details
    sender_email = os.getenv("sneder_email")
    sender_password = os.getenv("sender_password")  # Use an app-specific password
    recipient_email = 
    subject = "Test Email from Python"
    body = "This is a test email sent from Python using Zoho's SMTP server."
    
    send_zoho_email(sender_email, sender_password, recipient_email, subject, body)