import sqlalchemy.engine.base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy_utils import database_exists, create_database
from config import postgres_settings
from models import db


def get_engine(user, pwd, host, port, db_name):
    url = f"postgresql://{user}:{pwd}@{host}:{port}/{db_name}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url)
    db.metadata.create_all(engine)
    return engine


def get_engine_from_settings(settings: dict) -> sqlalchemy.engine.base.Engine:
    keys = ["pguser", "pgpassword", "pghost", "pgport", "pgdb"]
    for key in keys:
        if key not in settings.keys():
            return "Bad settings"
    return get_engine(settings["pguser"], settings["pgpassword"], settings["pghost"], settings["pgport"],
                      settings["pgdb"])


def get_session(engine):
    # engine = get_engine_from_settings(postgres_settings)
    session = Session(engine)
    return session
