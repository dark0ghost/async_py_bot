import asyncio
import aiosmtplib

from email.mime.text import MIMEText
from random import random, choice


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

    def __init__(self, hostname_mail, port) -> None:
        """
        :param hostname_mail:
        :param port:
        """
        self.code: str = ""
        self.host_name: str = hostname_mail
        self.port: int = port
        self.message: MIMEText = MIMEText("test")
        self.len_code: int = 1

    def change_len_code(self, new_len_code) -> None:
        self.len_code = new_len_code

    def get_random_code(self) -> None:
        """
        :return:
        """
        alphacode = list(str(random()).replace(".", ""))
        for i in range(self.len_code):
            self.code += str(choice(alphacode))

    def get_code(self) -> int:
        """
        return  self.code
        :return:
        """
        return self.code

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

    async def async_send_message(self) -> None:
        """
        asunc out
        :return:
        """
        await aiosmtplib.send(self.message, hostname=self.host_name, port=self.port)

    def sync_send_message(self) -> None:
        """
        for sync sync code
        :return:
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_send_message())


