from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///productivity.db', echo=True)

Session = sessionmaker(bind=engine)

from models import Base

Base.metadata.create_all(engine)
