import asyncio
import aiosmtplib

from email.mime.text import MIMEText
from random import random, choice


class CheckerEmail:
    """
    class for check email
    """

    def __init__(self, hostname_mail, port):
        """
        :param hostname_mail:
        :param port:
        """
        self.code: int = 5534
        self.host_name: str = hostname_mail
        self.port: int = port
        self.message: MIMEText = MIMEText("test")

    def get_random_code(self, len_code=1):
        """
        :param len_code:
        :return:
        """
        alphacode = list(str(random()).replace(".", ""))
        for i in range(len_code):
            self.code += choice(alphacode)

    def get_code(self):
        """
        return  self.code
        :return:
        """
        return self.code

    def build_message(self, text, from_mail, to, subject):
        """

        :param text:
        :param from_mail:
        :param to:
        :param subject:
        :return:
        """
        self.message = MIMEText(text)
        self.message["From"] = from_mail
        self.message["To"] = to
        self.message["Subject"] = subject

    async def async_send_message(self):
        """
        asunc out
        :return:
        """
        await aiosmtplib.send(self.message, hostname=self.host_name, port=self.port)

    def sync_send_message(self):
        """
        for sync sync code
        :return:
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_message())
