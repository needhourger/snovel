'''
Description: 
Author: cc
Date: 2021-04-29 14:28:29
LastEditors: cc
LastEditTime: 2021-04-29 18:34:49
'''
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from snovel.config import Config

import os

Base = declarative_base()


class T_Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), default="(None)")
    author = Column(String(32), default="(None)")
    path = Column(String(128), unique=True)
    p_chapter = Column(Integer, default=0)
    p_start = Column(Integer, default=0)
    p_end = Column(Integer, default=0)

    def __repr__(self) -> str:
        return "[id]: {}\t [path]: {}".format(self.id, self.path)


class DataBase:

    engine = None
    DBsession = None
    session = None
    file_limit = None

    def __init__(self, config: Config) -> None:
        self.file_limit = config.FILE_SIZE_LIMIT
        self.engine = create_engine(config.DATABASE_URI)
        self.DBsession = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.session = self.DBsession()

    def list_books(self):
        books = self.session.query(T_Book).all()
        for b in books:
            print(b)

    def get_books_values(self):
        books = self.session.query(T_Book).all()
        if books:
            ret = []
        else:
            ret = [(None, "(None)")]
        for b in books:
            ret.append((b.id, b.name))
        return ret

    def get_book(self, bid: str):
        return self.session.query(T_Book).filter(T_Book.id == bid).first()

    def save_book(self, tbook: dict):
        self.session.query(T_Book).filter(
            T_Book.id == tbook["id"]).update(tbook)
        self.session.commit()

    def add_book(self, path: str):
        if not path.endswith(".txt"):
            return
        if os.path.getsize(path) < self.file_limit:
            return

        p = os.path.abspath(path)
        tbook = self.session.query(T_Book.path == p).first()
        if tbook:
            return
        tbook = T_Book()
        tbook.name = os.path.split(path)[1].replace(".txt", "")
        tbook.path = p
        self.session.add(tbook)
        self.session.commit()
        print("[add book]: {}]".format(p))

    def delete_book(self, ids: int):
        books = self.session.query(T_Book).filter(T_Book.id.in_(ids)).all()
        for b in books:
            self.session.delete(b)
        self.session.commit()
