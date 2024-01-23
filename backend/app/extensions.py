from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

directory = os.getenv('DB_PATH')
filename = 'test.db'

full_path = os.path.join(directory, filename)

engine = create_engine(f'sqlite:///{full_path}')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from .models import User
    Base.metadata.create_all(bind=engine)