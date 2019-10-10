from gino.declarative import Model


class Base(Model):
    __abstract__ = True

    @classmethod
    def get(cls, session, whereclause):
        return session.query(cls).filter(whereclause).first()
