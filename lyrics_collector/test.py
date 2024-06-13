from sqlalchemy import create_engine, insert, text, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from functions import request_song_url_from_artist, scrape_song_lyrics
import time

time.sleep(3)

Base = declarative_base()
engine = create_engine("postgresql+psycopg2://postgres:postgres@db:5432/DB")
conn = engine.connect()


# Define the Lyrics table schema
class Lyrics(Base):
    __tablename__ = 'lyrics'
    id = Column(Integer, primary_key=True, autoincrement=True)  #primary key
    artist = Column(String,  nullable=False)
    title = Column(String, nullable=False)
    lyrics = Column(String,  nullable=False)

# Create the table if it does not exist
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

#artist_name=var = input("Please enter the artist or band name: ")
artist_name = "tool" #os.getenv('ARTIST_NAME', 'tool')
urls=request_song_url_from_artist(artist_name, song_cap=5)

# Insert data into the table
for i, url in enumerate(urls):
    song_lyrics, song_title=scrape_song_lyrics(urls[i])
    session.add(Lyrics(artist=artist_name, title=song_title, lyrics=song_lyrics))
    print(i)
    session.commit()

# Close the session
session.close()

print('done')