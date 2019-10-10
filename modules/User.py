from aiogram import types
from aiogram.types import User


from modules.Base import Base
from modules.db_pg import Postgres
from modules.db_session import db_session
from modules.utils import aiowrap


class User(Base):
    __tablename__ = 'users'
    id = Postgres.db_pg.Column(Postgres.db_pg.Integer, unique=True, nullable=False, primary_key=True)
    locale = Postgres.db_pg.Column(Postgres.db_pg.String(length=2), default=None)
    # TODO add is_admin, is_stoped

    @classmethod
    @aiowrap
    def get_user(cls, tg_user: types.User) -> (bool, 'User'):
        with db_session() as session:
            user = cls.get(session, cls.id == tg_user.id)
            is_new = False
            if user is None:
                user = cls(id=tg_user.id)
                session.add(user)
                session.commit()
                user = cls(id=user.id)
                is_new = True

            return is_new, user

    @aiowrap
    def set_language(self, language: str):
        with db_session() as session:
            user = User.get(session, User.id == self.id)
            user.locale = language
            session.commit()

    @classmethod
    @aiowrap
    def count(cls):
        with db_session() as session:
            return session.query(Postgres.bind.func.count(cls.id)).scalar()
