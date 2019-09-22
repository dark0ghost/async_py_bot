import aiohttp
import ujson
import string
import random

from typing import Dict
from aiohttp import FormData
from model.exception_class import FaceAppException


class FaceApp:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        """

        :param session:
        """
        self.URL = 'https://ph-x-p.faceapp.io'
        self.USER_AGENT = 'FaceApp/1.0.229 (Linux; Android 4.4)'
        self.DEVICE_ID = self.get_code()
        self.file: open
        self.session: aiohttp.ClientSession = session

    @staticmethod
    def gen(size=8, chars=string.ascii_lowercase + string.digits) -> str:
        """
        this function generates a 8 chars string that will be used as DEVICE_ID
        :param size:
        :param chars:
        :return:
        """

        return ''.join(random.choice(chars) for _ in range(size))

    async def get_code(self, path_file_photo: str = "") -> str:
        """
        get photo code
        :param path_file_photo: photo's file path
        :return: photo code
        """

        if path_file_photo != "":
            data = FormData()
            data.add_field("file", open(path_file_photo))
            async with self.session.post(self.URL + '/api/v2.3/photos', data=data,
                                         headers={'User-Agent': self.USER_AGENT,
                                                  'X-FaceApp-DeviceID': self.DEVICE_ID}) as response:
                rb: Dict[str, str] = ujson.loads(ujson.dumps(await response.json()))
                if response.status not in [200, 201, 202]:
                    raise FaceAppException("Error: {}\nDescription:{}".format(rb['err'], rb['err']['desc']))
                else:
                    return rb['code']
        raise FaceAppException("file not found")

    async def make_img(self, code, filter_name) -> str:
        """
        Apply filter to the image
        :param code: the photo code you can get with get_code
        :param filter_name: the filter you want to apply
        :return: byte image
        """

        if filter_name in ['smile', 'smile_2', 'hot', 'old', 'young', 'female', 'male']:
            async with self.session.post(self.URL + f"/api/v2.3/photos/{code}/filters/{filter_name}?cropped=true",
                                         headers={'User-Agent': self.USER_AGENT,
                                                  'X-FaceApp-DeviceID': self.DEVICE_ID}) as response:
                if response.status == 200:
                    content = response.content.read()
                    return content
                else:
                    raise FaceAppException(f"Error {response.status}")
        raise FaceAppException('invalid filter')


import asyncio


async def h():
    s = aiohttp.ClientSession()
    a = FaceApp(s)
    print(await a.get_code("./static/1.jpg"))
    await s.close()


asyncio.run(h())
