from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Date, Boolean
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///cinema.db', echo=False)

Base = declarative_base()


class Cinema(Base):
    __tablename__ = 'cinema'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    genre_id = Column(String(255), ForeignKey('genre.id'), nullable=False)
    director_id = Column(String(100), ForeignKey('director.id'))
    year_of_issue = Column(String(4), nullable=False)
    country = Column(String(50))
    is_viewed = Column(Boolean, nullable=False)


    def __init__(self, title, genre, year_of_issue, director, country):
        self.title = title
        self.genre_id = genre
        self.year_of_issue = year_of_issue
        self.director_id = director
        self.country = country
        self.is_viewed = False

    def __repr__(self):
        return "<Cinema('%s','%s', '%s', '%s', '%s')>" % (self.title, self.genre_id, self.director_id, self.country, self.is_viewed)


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    cinemas = relationship('Cinema', backref='genre', lazy='dynamic')

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Genre('%s')>" % (self.title)

class Director(Base):
    __tablename__ = 'director'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    cinemas = relationship('Cinema', backref='director', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Director('%s')>" % (self.name)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
first_director = Director('Cameron')
first_genre = Genre('action')
first_cinema1 = Cinema('terminator', 1, '1983', 1, "USA")
first_cinema2 = Cinema('terminator2', 1, '1985', 1, "USA")
session.add(first_director)
session.add(first_genre)
session.add(first_cinema1)
session.add(first_cinema2)
print(first_cinema1.title)
print(first_genre.cinemas.all())
print(first_director.cinemas.all())
for cinema in first_director.cinemas.all():
    print(cinema.title)

