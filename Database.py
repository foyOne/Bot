from datetime import date
from sqlalchemy import create_engine, Table, Column, String, Float, MetaData, or_, and_
from sqlalchemy.sql import select, delete
from sqlalchemy.orm import sessionmaker, Session, relationship
import os
from Model import *

class SQLiteDataBase:
    def __init__(self, connection: str):
        self.Connection = connection
        self.Name = connection.split('/')[-1]

    def init(self, base):
        exists = os.path.isfile(self.Name)
        self.Engine = create_engine(self.Connection, connect_args={'check_same_thread': False})
        if not exists:
            base.metadata.create_all(self.Engine)
    
    def GetSession(self):
        return sessionmaker(bind=self.Engine)()
    
    def Dispose(self):
        self.Engine.dispose()
