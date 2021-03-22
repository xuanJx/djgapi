import re
import requests

from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import sessionmaker

NAME_URL = '<a href="/author/(.*).html"'
BOOK_NAME_URL = '<a href="/book/(.*).html"'
BRIEF = r'<p>(.*)</p>'
AUTHOR = r'<h1>(.*)</h1>'
AUTHOR_URL = 'http://www.kehuan.net.cn/author.html'
BOOK_AUTHOR = '<a href="/author/[\S]*.html">(.*)</a>'

book_engine = create_engine('mysql+pymysql://root:@localhost/books')
Base = declarative_base()

class BooksPageView(Base):
    __tablename__ = 'djgapp_bookspageview'
    id = Column(Integer, primary_key=True)
    read_num = Column(Integer)
    comment_num = Column(Integer)
    book_id = Column(Integer, ForeignKey('djgapp_bookspageview.id'))

    def __init__(self, read_num, comment_num, book_id):
        self.read_num = read_num
        self.comment_num = comment_num
        self.book_id = book_id

    def __repr__(self):
        return "<bookspageview('%s', '%s', '%s')>" % (self.read_num, self.comment_num, self.book_id)

class ScienceBooksPageView(Base):
    __tablename__ = 'djgapp_sciencebookspageview'
    id = Column(Integer, primary_key=True)
    read_num = Column(Integer)
    comment_num = Column(Integer)
    book_id = Column(Integer, ForeignKey('djgapp_sciencebookspageview.id'))

    def __init__(self, read_num, comment_num, book_id):
        self.read_num = read_num
        self.comment_num = comment_num
        self.book_id = book_id

    def __repr__(self):
        return "<sciencebookspageview('%s', '%s', '%s')>" % (self.read_num, self.comment_num, self.book_id)

class ScienceBooks(Base):
    __tablename__ = 'djgapp_sciencebooks'
    id = Column(Integer, primary_key=True)
    book_name = Column(String(32))
    brief = Column(Text)
    author_id = Column(Integer, ForeignKey('djgapp_scienceauthor.id'))

    def __init__(self, book_name, brief, author_id):
        self.book_name = book_name
        self.brief = brief
        self.author_id = author_id

    def __repr__(self):
        return "<sciencebooks('%s', '%s', '%s')>" % (self.book_name, self.brief, self.author_id)

class ScienceAuthor(Base):
    __tablename__ = 'djgapp_scienceauthor'
    id = Column(Integer, primary_key=True)
    author = Column(String(32))
    brief = Column(Text)

    def __init__(self, author, brief):
        self.author = author
        self.brief = brief

    def __repr__(self):
        return "<scienceauthor('%s', '%s')>" % (self.author, self.brief)

Base.metadata.create_all(book_engine)

Book_session = sessionmaker(bind=book_engine)
session = Book_session()

def page_view_sql():
    for i in range(1, 306):
        add = ScienceBooksPageView(0, 0, i)
        session.add(add)
        session.commit()
        session.close()
page_view_sql()
