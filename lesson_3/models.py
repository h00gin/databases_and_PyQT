# -*- coding: utf8 -*-
"""Database"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ClientOnServer(Base):

    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    information = Column(String)

    def __init__(self, login, information):
        self.login = login
        self.information = information

    def __repr__(self):
        return f'<Client({self.login}, {self.information})>'


class ClientHistory(Base):

    __tablename__ = 'client_history'
    id = Column(Integer, primary_key=True)
    entry_time = Column(DateTime)
    ip_address = Column(String)

    def __init__(self, entry_time, ip_address):
        self.entry_time = entry_time
        self.ip_address = ip_address

    def __repr__(self):
        return f'<Client history({self.entry_time}, {self.ip_address})>'


