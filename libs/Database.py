from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

_db = SqliteExtDatabase('saved_data.db')


class BaseModel(Model):
    class Meta:
        database = _db

class StatsModel(BaseModel):
    date = DateTimeField(null=False, default=datetime.datetime.now)
    mifare = CharField(null=False)
    type = CharField(null=False)
