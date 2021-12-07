from datetime import datetime

from peewee import *

from .engine import db


class BaseModel(Model):
    created_at = DateTimeField(default=f'{datetime.now()}')
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = f'{datetime.now()}'
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        database = db


class Callback(BaseModel):
    callback = CharField()
    abbreviation = CharField()
    use_counter = IntegerField(default=0)
