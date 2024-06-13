#import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from functions_etl import get_number_songs
from sqlalchemy import create_engine, Column, String, Integer, func
from sqlalchemy.orm import declarative_base, sessionmaker
import random
import time

time.sleep(3)

def extract():

    num_songs=get_number_songs()
    song_id=random.randint(1, num_songs)

    # sqlalchemy psql definitions
    Base = declarative_base()
    engine = create_engine("postgresql+psycopg2://postgres:postgres@db:5432/DB")
    conn = engine.connect()
    time.sleep(1)
    class Lyrics(Base):
        __tablename__ = 'lyrics'
        id = Column(Integer, primary_key=True)
        artist = Column(String)
        title = Column(String)
        lyrics = Column(String)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    item = session.query(Lyrics).filter_by(id=song_id).first()
    if item:
        title=  item.title
        lyrics = item.lyrics
        id= item.id
    else:
        print(f"Item with {song_id} not found")
    session.close()
    
    return lyrics, title, id


def transform(lyrics: str):
    # Generate a word cloud from the song lyrics
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(lyrics)
    return wordcloud


def load(wordcloud: WordCloud):
    # Plot the word cloud
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.savefig("./lyric_cloud.png")


lyrics, title, id=extract()
print("extract, done")
wordcloud=transform(lyrics)
print("trasform, done")
load(wordcloud)
print("it's working!!!!")

