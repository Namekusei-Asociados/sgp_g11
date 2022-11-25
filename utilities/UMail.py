import smtplib
import ssl
from email.message import EmailMessage


class UMail:
    """
    Esta clase permite enviar emails
    """
    @staticmethod
    def sent_email(subject, body, to):
        """
        Metodo estatico para enviar emails
        :param subject:
        :param body:
        :param to:
        :return:
        """
        email_sender = 'breideworld@gmail.com'
        email_password = 'ukhwteljlwspolns'
        # instance class email
        em = EmailMessage()

        # pass vars
        em['From'] = email_sender
        em['To'] = to
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        # sent email
        with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,to, em.as_string())
