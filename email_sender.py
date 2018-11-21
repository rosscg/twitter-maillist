import smtplib
from email.mime.text import MIMEText

from credentials import USERNAME, PASSWORD, ACCOUNT_NAME

# Targets as either a list of strings, or single string.
# Currently no error handling. Eg. length of subject, email formatting...
def send_email(targets, subject, message):
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    sender = USERNAME
    # Turn single target into list:
    if type(targets) == str:
        t = targets
        targets = [t]
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = ACCOUNT_NAME
    msg['To'] = ', '.join(targets)

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(USERNAME, PASSWORD)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()


if __name__ == '__main__':
    send_email('raeynn@gmail.com', 'subject name', 'test message')
