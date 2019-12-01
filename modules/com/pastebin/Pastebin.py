import aiohttp
import typing

from aiohttp_socks import SocksConnector


class Pastebin:
    lang: typing.Dict[str, str] = {
        "4cs": "4CS",
        "6502acme": "6502 ACME Cross Assembler",
        "6502kickass": "6502 Kick Assembler",
        "6502tasm": "6502 TASM/64TASS",
        "abap": "ABAP",
        "‘actionscript’": "ActionScript",
        "actionscript3": "ActionScript 3",
        "ada": "Ada",
        "algol68": "ALGOL 68",
        "apache": "Apache Log",
        "applescript": "AppleScript",
        "apt_sources": "APT Sources",
        "asm": "ASM (NASM)",
        "asp": "ASP",
        "autoconf": "autoconf",
        "autohotkey": "Autohotkey",
        "autoit": "Autoit",
        "avisynth": "Avisynth",
        "awk": "Awk",
        "bascomavr": "BASCOM AVR",
        "bash": "Bash",
        "basic4gl": "Basic4GL",
        "bibtex": "BibTeX",
        "blitzbasic": "Blitz Basic",
        "bnf": "BNF",
        "boo": "BOO",
        "bf": "BrainFuck",
        "c": "C",
        "c_mac": "C for Macs",
        "cil": "C Intermediate Language",
        "csharp’": "C#",
        "cpp": "C++",
        "cpp-qt": "C++ (with QT extensions)",
        "c_loadrunner": "C: Loadrunner",
        "caddcl": "CAD DCL",
        "cadlisp": "CAD Lisp",
        "cfdg": "CFDG",
        "chaiscript": "ChaiScript",
        "clojure": "Clojure",
        "klonec": " Clone C",
        "klonecpp": "Clone C + + ",
        "cmake": "CMake"
    }

    def __init__(self, token: str, session: typing.Optional[aiohttp.ClientSession] = None) -> None:
        """
        :param token:
        :param session:
        """
        self.api_url: str = 'http://pastebin.com/api/api_post.php'
        self.api_dev_key: str = token
        self.session: aiohttp.ClientSession = session
        self.paste_no_paste_object = -1
        self.paste_no_data_in_object = -2
        self.data: typing.Dict[str, str] = {}

    def generate_data(self, paste: str, paste_name: str = None, language: str = "python", paste_date: str = 'N',
                      is_private: str = "0") -> typing.Dict[str, str]:
        """

        :param paste:
        :param paste_name:
        :param language:
        :param paste_date:
        :param is_private:
        :return:
        """
        self.data: typing.Dict[str, str] = {'api_option': "paste",
                                            'api_dev_key': self.api_dev_key,
                                            'api_paste_private': is_private,
                                            'api_paste_name': paste_name,
                                            'api_paste_expire_date': paste_date,
                                            'api_paste_format': language,
                                            'api_user_key': self.api_dev_key,
                                            'api_paste_code': paste
                                            }
        return self.data

    async def send_paste(self, data: typing.Dict[str, str] = None) -> str:
        """

        :param data:
        :return:
        """
        if data is not None:
            async with self.session.post(url=self.api_url, data=self.data) as response:
                return await response.text(encoding="UTF-8")
        else:
            async with self.session.post(url=self.api_url, data=data) as response:
                return await response.text(encoding="UTF-8")

    async def open_session(self, proxy: str = None) -> aiohttp.ClientSession:
        """

        :param proxy:
        :return:
        """
        if proxy is None:
            self.session = aiohttp.ClientSession()
            return self.session
        connector = SocksConnector.from_url(proxy)
        self.session = aiohttp.ClientSession(connector=connector)
        return self.session

    async def close(self) -> None:
        """

        :return:
        """
        await self.session.close()
        return


