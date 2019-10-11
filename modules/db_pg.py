from gino import Gino


class Postgres:
    db_pg = Gino()

    def __init__(self) -> None:
        """
           :return:
        """
        self.db_pg: Gino = Postgres.db_pg
        self.bind: Gino.set_bind = None

    async def connect(self, url: str) -> Gino:
        """

        :param url:
        :return:
        """
        self.bind = await self.db_pg.set_bind(url)
        return self.bind

    async def make_migrate(self) -> Gino:
        return await self.db_pg.gino.create_all()

    def return_bind(self) -> Gino:
        """

        :return:
        """
        return self.bind


class UserLang(Postgres.db_pg.Model):
    __tablename__ = 'users_lang'

    id = Postgres.db_pg.Column(Postgres.db_pg.Integer(), unique=True, nullable=False, primary_key=True)
    lang = Postgres.db_pg.Column(Postgres.db_pg.String(length=2), default=None)


class AccessToken(Postgres.db_pg.Model):
    __tablename__ = 'access_token_auth'

    chat_id = Postgres.db_pg.Column(Postgres.db_pg.Integer())
    token_github = Postgres.db_pg.Column(Postgres.db_pg.Unicode(), default='0')
    token_google = Postgres.db_pg.Column(Postgres.db_pg.Unicode(), default='0')


class PastebinTable(Postgres.db_pg.Model):
    __tablename__ = 'PastebinTable'

    chat_id = Postgres.db_pg.Column(Postgres.db_pg.Integer())
    paste = Postgres.db_pg.Column(Postgres.db_pg.Unicode())
