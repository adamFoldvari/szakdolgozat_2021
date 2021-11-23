from dataclasses import dataclass
from healthcheck_api import db


@dataclass
class EntryModel(db.Model):
    id: int
    name: str

    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Entry {self.name}>"

