import logging
import smtplib
from email.mime.text import MIMEText

class NotificationSender:

    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password, email_sender, email_recipients):
        self.logger = logging.getLogger(__name__)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.email_sender = email_sender
        self.email_recipients = email_recipients

    def send_incident_notification(self, incident):
        try:
            message = MIMEText(f"A security incident has been detected: {incident}")
            message['Subject'] = f"Incident Notification - {incident.id}"
            message['From'] = self.email_sender
            message['To'] = ', '.join(self.email_recipients)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.email_sender, self.email_recipients, message.as_string())

            self.logger.info('Incident notification sent successfully.')
        except Exception as e:
            self.logger.error('Failed to send incident notification:', e)

    def send_incident_handling_failure_notification(self, incident):
        try:
            message = MIMEText(f"Failed to handle incident: {incident}")
            message['Subject'] = f"Incident Handling Failure Notification - {incident.id}"
            message['From'] = self.email_sender
            message['To'] = ', '.join(self.email_recipients)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.email_sender, self.email_recipients, message.as_string())

            self.logger.info('Incident handling failure notification sent successfully.')
        except Exception as e:
            self.logger.error('Failed to send incident handling failure notification:', e)

if __name__ == '__main__':
    # Replace with your actual SMTP server settings and email addresses
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_username = 'your_email@example.com'
    smtp_password = 'your_password'
    email_sender = 'your_email@example.com'
    email_recipients = ['recipient1@example.com', 'recipient2@example.com']

    # Create an instance of the NotificationSender class
    notification_sender = NotificationSender(smtp_server, smtp_port, smtp_username, smtp_password, email_sender, email_recipients)

    # Send a mock incident notification
    incident = Incident('ID-12345', 'High', 'Malware infection')
    notification_sender.send_incident_notification(incident)

    # Send a mock incident handling failure notification
    notification_sender.send_incident_handling_failure_notification(incident)
