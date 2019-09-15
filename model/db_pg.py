import asyncio
from gino import Gino

db_pg = Gino()


class User(db_pg.Model):
    __tablename__ = 'users_bot'
    id = db_pg.Column(db_pg.Integer(), primary_key=True)
    nickname = db_pg.Column(db_pg.Unicode(), default='noname')
    email = db_pg.Column(db_pg.Unicode())
    _meta = db_pg.Column(db_pg.Unicode(), default="none")


class UserLang(db_pg.Model):
    __tablename__ = 'users_lang'
    id = db_pg.Column(db_pg.Integer(), primary_key=True)
    lang = db_pg.Column(db_pg.Unicode())
