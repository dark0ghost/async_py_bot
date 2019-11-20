import asyncio
from aiogoogle import Aiogoogle
from typing import Dict


class GoogleDerivedBot:
    user_creds = {'access_token': ''}

    async def list_files(self):
        async with Aiogoogle(user_creds=self.user_creds) as aiogoogle:
            drive_v3 = await aiogoogle.discover('drive', 'v3')
            full_res = await aiogoogle.as_user(
                drive_v3.files.list(),
                full_res=True
            )

        async for page in full_res:
            for file in page['files']:
                print(file['name'])