from sqlalchemy import create_engine, Column, String, Integer, func
from sqlalchemy.orm import declarative_base, sessionmaker

def get_number_songs():

    # PostgreSQL database URL
    database_url = "postgresql+psycopg2://postgres:postgres@db:5432/DB"

    engine = create_engine(database_url)

    Base=declarative_base()

    # Define the Lyrics table schema with an ID column as primary key
    class Lyrics(Base):
        __tablename__ = 'lyrics'
        id = Column(Integer, primary_key=True, autoincrement=True)
        artist = Column(String, nullable=False)
        title = Column(String, nullable=False)
        lyrics = Column(String, nullable=False)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query to count the number of rows in the lyrics table
    row_count = session.query(func.count(Lyrics.id)).scalar()

    # Print the count of rows
    return row_count
