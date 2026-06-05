from app.db.database import SessionLocal, engine, get_db_session


def get_session():
    yield from get_db_session()
