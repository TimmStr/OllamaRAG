import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils import mail_config, MAIL_HOST, MAIL_PORT, MAIL_PASSWORD, MAIL_USER
from utils.logging_config import exception_handling


class EmailService:
    def __init__(self):
        self.config_dict = mail_config()
        self.mailserver_conn = smtplib.SMTP(self.config_dict[MAIL_HOST], int(self.config_dict[MAIL_PORT]))
        self.mailserver_conn.starttls()
        self.mailserver_conn.login(self.config_dict[MAIL_USER], self.config_dict[MAIL_PASSWORD])

    @exception_handling
    def send_mail(self, betreff="Important", text="Hello dear friend.", to="t.straub@xyz.de"):
        msg = MIMEMultipart()
        msg['From'] = self.config_dict["email_from"]
        msg['To'] = to
        msg['Subject'] = betreff

        msg.attach(MIMEText(text, 'plain'))
        if to.endswith("@xyz.de"):
            self.mailserver_conn.sendmail(msg['From'], msg['To'], msg.as_string())
        else:
            print("wrong email")

    def __del__(self):
        if hasattr(self, 'mailserver_conn') and self.mailserver_conn:
            self.mailserver_conn.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self, 'mailserver_conn') and self.mailserver_conn:
            self.mailserver_conn.quit()


if __name__ == "__main__":
    try:
        mail_service = EmailService()
        mail_service.send_mail()
    except Exception as e:
        raise e
    finally:
        del mail_service
