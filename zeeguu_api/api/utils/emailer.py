from smtplib import SMTP

from zeeguu_api.app import app


class ZeeguuMailer(object):

    def __init__(self, message_subject, message_body, to_email):
        self.message_body = message_body
        self.to_email = to_email
        self.message_subject = message_subject
        self.server_name = app.config.get('SMTP_SERVER')
        self.our_email = app.config.get('SMTP_USERNAME')
        self.password = app.config.get('SMTP_PASSWORD')

    def send(self):
        # Fetch SMTP info

        message = self._content_of_email()
        # Send email
        server = SMTP(self.server_name)
        server.ehlo()
        server.starttls()
        server.login(user=self.our_email, password=self.password)
        server.sendmail(from_addr=self.our_email, to_addrs=self.to_email, msg=message)
        server.quit()

    def _content_of_email(self):
        from email.mime.text import MIMEText

        message = MIMEText(self.message_body)
        message['From'] = self.our_email
        message['To'] = self.to_email
        message['Subject'] = self.message_subject

        return message.as_string()


def send_password_reset_email(to_email, code):
    body = "\r\n".join([
        "Hi there,",
        " ",
        "Please use this code to reset your password: " + str(code) + ".",
        " ",
        "Cheers,",
        "The Zeeguu Team"
    ])

    emailer = ZeeguuMailer('Reset your password', body, to_email)
    emailer.send()


def send_new_user_account_email(username, invite_code='', cohort=''):
    body = "\r\n".join([
        f"Code: {invite_code} Class: {cohort}"
        " ",
        "Cheers,",
        "The Zeeguu Server ;)"
    ])

    emailer = ZeeguuMailer(f'New Account: {username}', body, app.config.get('SMTP_USERNAME'))
    emailer.send()


def send_notification_article_feedback(feedback, username, article_title, article_url):
    body = "\r\n".join([
        f"{article_title}",
        f"https://www.zeeguu.unibe.ch/read/article?articleURL={article_url}",
        " ",
        "Cheers,",
        "The Zeeguu Server ;)"
    ])

    emailer = ZeeguuMailer(f'{feedback} By {username}', body, app.config.get('SMTP_USERNAME'))
    emailer.send()
