import aiofiles
import aiohttp


class CatApi:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        """

        :param session:
        """
        self.session: aiohttp.ClientSession = session

    async def get_photo(self) -> str:
        """

        :return:
        """
        async with self.session.get(
                "https://api.thecatapi.com/v1/images/search?limit=5&page=10&order=Desc") as response:
            json = await response.json()

            async with self.session.get(json[0]["url"]) as response_photo:
                if "jpg" in json[1]["url"]:
                    async with aiofiles.open("./staticfile/cat.jpg", "wb") as f:
                        await f.write(await response_photo.read())
                    return "jpg"

                elif "png" in json[1]["url"]:
                    async with aiofiles.open("./staticfile/cat.png", "wb") as f:
                        await f.write(await response_photo.read())
                    return "png"
                else:
                    async with aiofiles.open("./staticfile/cat.gif", "wb") as f:
                        await f.write(await response_photo.read())
                    return "gif"
