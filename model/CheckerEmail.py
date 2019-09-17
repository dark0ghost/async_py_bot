import asyncio
import aiosmtplib

from email.mime.text import MIMEText
from random import random, choice

from aiosmtplib import SMTP


class CheckerEmail:
    """
    class for check email
    use :
      check:CheckerEmail = CheckerEmail(hostname_mail="smt.com", port=93)
      check.change_len_code(new_len_code=5)
      check.get_random_code()
      code: int = check.get_code()
      await check.async_send_message # in async def
      # or sync code
      check.sync_send_message
    """

    def __init__(self, hostname_mail: str, port: int, login: str, password: str, loop=None) -> None:
        """

        :param hostname_mail:
        :param port:
        :param login:
        :param password:
        """
        if loop is None:
            loop = asyncio.get_event_loop()
        self.host_name: str = hostname_mail
        self.port: int = port
        self.message: MIMEText = MIMEText("test")
        self.len_code: int = 1
        self.client = SMTP(password=password, username=login, loop=loop)

    def change_len_code(self, new_len_code) -> None:
        """

        :param new_len_code:
        :return:
        """
        self.len_code = new_len_code

    def get_random_code(self) -> None:
        """
        :return:
        """
        code = ""
        alphacode = list(str(random()).replace(".", ""))
        for i in range(self.len_code):
            code += str(choice(alphacode))
        return code

    def build_message(self, text, from_mail, to, subject) -> None:
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

    async def async_send_message(self, start_tls=True, use_tls=False) -> None:
        """
        asunc out
        :return:
        """

        await self.client.connect(hostname=self.host_name, port=self.port, use_tls=use_tls, start_tls=start_tls)

        if self.port == 587:
            await self.client.starttls()

        async with self.client:
            await self.client.send_message(self.message, )

    def sync_send_message(self, start_tls=True, use_tls=False) -> None:
        """
        for sync sync code

        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_send_message(start_tls, use_tls))
