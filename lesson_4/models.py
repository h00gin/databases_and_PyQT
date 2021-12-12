# -*- coding: utf8 -*-
"""Database"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ClientOnServer(Base):

    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True, nullable=False)
    information = Column(String)
    history = relationship('ClientHistory', cascade='all, delete-orphan')

    def __init__(self, login, information):
        self.login = login
        self.information = information

    def __repr__(self):
        return f'<Client({self.login}, {self.information})>'


class ClientHistory(Base):

    __tablename__ = 'client_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_time = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('client.id'))
    ip_address = Column(String)

    def __init__(self, entry_time, ip_address):
        self.entry_time = entry_time
        self.ip_address = ip_address

    def __repr__(self):
        return f'<Client history({self.entry_time}, {self.ip_address})>'


class Contacts(Base):

    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('client.id'))
    client_id = Column(Integer, ForeignKey('client.id'))




