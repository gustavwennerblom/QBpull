import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import config
from creds import ses_credentials


class LogMailer(object):
    def __init__(self, from_address=ses_credentials.sender_address, to_address=config.log_email_recipient):
        self.server = smtplib.SMTP(ses_credentials.endpoint)
        self.server.starttls()
        self.server.login(user=ses_credentials.username, password=ses_credentials.password)
        self.from_address = from_address
        self.to_address = to_address

    def compose_mail(self, msg, **kwargs):
        pass

    def send_mail(self, subject_text, body_text, **kwargs):
        msg = MIMEMultipart()
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        msg['Subject'] = subject_text

        msg.attach(MIMEText(body_text, 'plain'))

        if kwargs.get("attachment_path"):
            with open(kwargs.get("attachment_path"), 'rb') as f:
                _, filename = os.path.split(f.name)
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename={}'.format(filename))
                msg.attach(part)

        # self.server.starttls()
        # self.server.login(loopia_creds.uid, loopia_creds.pwd)
        msg_stringified = msg.as_string()
        self.server.sendmail(self.from_address, self.to_address, msg_stringified)
        self.server.quit()


if __name__ == '__main__':
    mailer = LogMailer()
    mailer.send_mail("My test message subject", "When we were young", attachment_path="./logs/fetch_results.log")