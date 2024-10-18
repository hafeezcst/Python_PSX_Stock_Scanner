    
from email import encoders
from email.mime.base import MIMEBase
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import configparser

def send_email(subject, body, attachment_path=None) :
    """

    :param subject:
    :param body:
    :param attachment_path:
    """
    # Email configuration
    sender_email = "hafeezcst@gmail.com"  # Replace with your email address
    receiver_emails = ["hafeezcst@gmail.com","amok3495@gmail.com" ,'tahir_inspection@yahoo.com']  # Replace with the recipient's email addresses
    # receiver_email = ", ".join(receiver_emails)
    smtp_server = "smtp.gmail.com"  # Replace with your SMTP server (e.g., smtp.gmail.com for Gmail)
    smtp_port = 587  # Replace with your SMTP port (587 is the default for TLS)
    
    # Load email credentials from config file
    config = configparser.ConfigParser ( )
    config.read ( 'config.ini' )
    username = config.get ( 'email', 'username' )
    password = config.get ( 'email', 'password' )
    
    # Create the email message
    message = MIMEMultipart ( )
    message [ "From" ] = sender_email
    message [ "To" ] = ", ".join ( receiver_emails )
    message [ "Subject" ] = subject
    message.attach ( MIMEText ( body, "plain" ) )
    
    if attachment_path :
        with open ( attachment_path, "rb" ) as attachment :
            part = MIMEBase ( "application", "octet-stream" )
            part.set_payload ( attachment.read ( ) )
        encoders.encode_base64 ( part )
        part.add_header (
            "Content-Disposition",
            f"attachment; filename= {os.path.basename ( attachment_path )}",
        )
        message.attach ( part )
    
    try :
        # Connect to the SMTP server
        server = smtplib.SMTP ( smtp_server, smtp_port )
        server.starttls ( )
        server.login ( username, password )
        
        # Send the email
        server.sendmail ( sender_email, receiver_emails, message.as_string ( ) )
        #print ( "Email sent successfully" )
    
    except Exception as e :
        error_message = f"Error sending email: {e}"
        logging.error ( f"{datetime.datetime.now ( )} - {error_message}" )
        print ( error_message )
    
    finally:
        # Disconnect from the SMTP server
        if server is not None:
            server.quit()
