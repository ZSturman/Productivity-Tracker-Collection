from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_session():
    engine = create_engine('sqlite:///productivity.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine
