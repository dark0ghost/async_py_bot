import asyncio
from aiogoogle import Aiogoogle
from typing import Dict


class GoogleDerivedBot:

    async def list_files(self, user_data: Dict[str, str]):
        """

        :type user_data: object
        """
        async with Aiogoogle(user_creds=user_data) as aio_google:
            drive_v3 = await aio_google.discover('drive', 'v3')
            full_res = await aio_google.as_user(
                drive_v3.files.list(),
                full_res=True
            )
        async for page in full_res:
            for file in page['files']:
                print(file['name'])


