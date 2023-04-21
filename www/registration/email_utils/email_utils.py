from dataclasses import dataclass
from smtplib import SMTP_SSL
from email.message import EmailMessage
from enum import Enum, auto
import os.path
import string
import typing
import logging

EMAIL_TEMPLATES = os.path.join('email_utils', 'templates')

class EmailTemplate(Enum):
    REGISTRATION = auto()
    REGISTRATION_WITHOUT_PAYMENT_LINK = auto()
    RECEIPT = auto()

template_map: typing.Dict[EmailTemplate, str] = {
    EmailTemplate.REGISTRATION: 'registration-confirmation.txt',
    EmailTemplate.REGISTRATION_WITHOUT_PAYMENT_LINK: 'registration-confirmation-without-payment.txt',
    EmailTemplate.RECEIPT: 'receipt.txt',
}

subject_map: typing.Dict[EmailTemplate, str] = {
    EmailTemplate.REGISTRATION: 'Registration confirmation',
    EmailTemplate.RECEIPT: 'Registration fee receipt',
}

@dataclass
class Emailer:
    """
    Email utilities.
    """
    server: str
    port: int
    username: str
    password: str
    from_addr: str
    subj_prefix: str
    enabled: bool = False

    def send_email_from_template(
        self,
        to_addr: str,
        name: str,
        surname: str,
        template_type: EmailTemplate,
        subst: typing.Dict[str, str]
    ):
        global EMAIL_TEMPLATES
        global subject_map
        global template_map

        email_body = self.read_template(
            to_addr,
            f'{self.subj_prefix} {subject_map[template_type]}',
            name,
            surname,
            subst,
            template_type,
        )

        self.send_email(email_body)

    def send_email(self, mail: EmailMessage):
        if not self.enabled:
            return

        try:
            smtp = SMTP_SSL(self.server, self.port)
            smtp.login(self.username, self.password)
            smtp.send_message(mail)
        except Exception as e:
            logging.error('Could not send email to "{}". Message: "{}".'.format(mail['To'], e))

    def read_template(
            self,
            to_addr: str,
            subject: str,
            name: str,
            surname: str,
            subst: typing.Dict[str, str],
            template_type: EmailTemplate,
    ) -> EmailMessage:
        msg = EmailMessage()
        try:
            fp = open(os.path.join(EMAIL_TEMPLATES, template_map[template_type]))
        except Exception as e:
            logging.error(f'Could not open registration email template. Message: "{e.__class__.__name__} {e}".')
            raise e
        else:
            template = string.Template(fp.read())

        msg_content = template.template
        try:
            msg_content = template.substitute({'name': name, 'surname': surname} | subst)
        except:
            logging.warn(f'Message "{template_type} to "{to_addr}" was not fully substituted')

        msg.set_content(msg_content)
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = to_addr
        return msg
