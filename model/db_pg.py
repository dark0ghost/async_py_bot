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


class AccessToken(db_pg.Model):
    __tablename__ = 'access_token_auth'

    chat_id = db_pg.Column(db_pg.Integer())
    token_github = db_pg.Column(db_pg.Unicode(), default='0')
    token_google = db_pg.Column(db_pg.Unicode(), default='0')


class PastebinTable(db_pg.Model):
    __tablename__ = 'PastebinTable'

    chat_id = db_pg.Column(db_pg.Integer())
    paste = db_pg.Column(db_pg.Unicode())


