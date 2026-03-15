from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import Base from your models module
from models.models import Base



class DatabaseManager:
    def __init__(self, db_path):
        self.engine = create_engine(db_path)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # This line will create all tables that don't exist yet
        Base.metadata.create_all(self.engine)