import contextlib

from sqlalchemy.orm import sessionmaker, scoped_session


from modules.db_pg import Postgres

session_factory = sessionmaker(bind=Postgres.db_pg)
Session_db = scoped_session(session_factory)



@contextlib.contextmanager
def db_session():
    session = Session_db()
    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        Session_db.remove()
