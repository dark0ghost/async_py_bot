import asyncio
import hashlib
import os
import aiohttp


class GoogleDerived:
    def __init__(self, token: str, session: aiohttp.ClientSession):
        self.token: str = token
        self.api_link = "https://www.googleapis.com/drive/v3/"
        self.session: aiohttp.ClientSession = session
        self.state_token = hashlib.sha256(os.urandom(1024)).hexdigest()
        self.session['state'] = self.state_token

    async def connect(self):
        async with self.session.get(self.api_link + "about?key={self.key}") as response:
            print(await response.json())
