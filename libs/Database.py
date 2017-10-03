import sqlite3
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

_db = SqliteExtDatabase('saved_data.db')


class BaseModel(Model):
    class Meta:
        database = _db
