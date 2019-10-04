import aiohttp
import re

from typing import Dict

from modules.exception_class import AuthError, NOConnect


class AuthPGU:
    def __init__(self, cfg: Dict[str, str]) -> None:
        self._cfg = cfg
        self.headers: Dict[str, str] = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",

        }
        self.session: aiohttp.ClientSession = None

    async def auth(self, url: str, referer: str) -> str:
        self.headers["referer"] = referer
        async with aiohttp.ClientSession() as self.session:
            async with self.session.post(url=url, allow_redirects=False, headrs=self.headers) as response:
                meta: re.search = re.search('<meta http-equiv="refresh" content="0;url=([^"]*)">',
                                            await response.text())
                async with self.session.get(url=meta.group(1), allow_redirects=False) as resp:
                    if resp.status != 302:
                        raise AuthError("no connect")
                    async with self.session.get(url=resp.headers["Location"], allow_redirects=False) as response_:
                        command = re.search(
                            "LoginViewModel\('/idp','','(.*)','','null','null',false, 300, 'gosuslugi.ru'\);",
                            await response_.text()
                            )
                        login_data: Dict[str, str] = {
                            "mobileOrEmail": self._cfg["login"],
                            "snils": "",
                            "password": self._cfg["password"],
                            "login": self._cfg["login"],
                            "command": command.group(1),
                            "idType": "email"
                        }

                        async with self.session.post("https://esia.gosuslugi.ru/idp/login/pwd/do",
                                                     data=login_data,
                                                     headers={"referer": "https://esia.gosuslugi.ru/idp/rlogin?cc=bp"},

                                                     allow_redirects=False) as response_pwddo:
                            if response_pwddo.status != 302:
                                raise NOConnect(f"NO connect {await response_pwddo.json()}")
                            async with self.session.post(url=response_pwddo.headers['Location'], allow_redirects=False,
                                                         headers={
                                                             "referer": "https://esia.gosuslugi.ru/idp/rlogin?cc=bp"}) as response_SSO2:
                                samlr = re.search('<input type="hidden" name="SAMLResponse" value="(.*)"/>',
                                                  await response_SSO2.text())
                                SAMLResponse = samlr.group(1)
                                post_data = {
                                    'RelayState': re.search('RelayState=([-_a-z0-9]*)', meta.group(1)).group(1),
                                    'SAMLResponse': SAMLResponse
                                }
                                async with  self.session.post(
                                        "https://esia.gosuslugi.ru/aas/oauth2/saml/SAMLAssertionConsumer",
                                        data=post_data, allow_redirects=False, headers={
                                            'referer': 'https://esia.gosuslugi.ru/idp/profile/SAML2/Redirect/SSO'}) as response_SAMLAC:
                                    if response_SAMLAC.status != 302:
                                        raise NOConnect(await response_SAMLAC.json())
                                    async with self.session.get(response_SAMLAC.headers['location'],
                                                                allow_redirects=False,
                                                                headers={
                                                                    'referer': 'https://esia.gosuslugi.ru/idp/profile/SAML2/Redirect/SSO'}) as res:
                                        return res.headers['Location']
