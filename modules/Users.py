import typing
from aiogram import types
from aiogram.types import User

import helps
from modules.db_pg import UserLang, Postgres

postgres = Postgres

class Users:
    @staticmethod
    async def get_user(tg_user: types.User) -> typing.Tuple[bool, typing.Union[User, typing.Any]]:
        await postgres.connect(postgres,url=helps.POSTGRES)
        user = await UserLang.query.where(UserLang.id == tg_user["id"]).gino.first()
        is_new = False
        if user is None:
            await UserLang.create(id=tg_user["id"], lang=tg_user["language_code"])
            is_new = True
        return is_new, user

    @staticmethod
    async def set_language(language: str, tg_user: types.User):
        user = await UserLang.query.where(UserLang.id == tg_user["id"]).gino.scalar()
        await UserLang.update(id=tg_user["id"], lang=language)
