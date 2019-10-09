from gino.declarative import declarative_base


class Base(declarative_base()):
    __abstract__ = True

    @classmethod
    def get(cls, session, whereclause):
        return session.query(cls).filter(whereclause).first()
