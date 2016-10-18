import hashlib
import os

from . import ModelMixin
from . import db
from . import timestamp

class Blog(db.Model, ModelMixin):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    created_time = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.created_time = timestamp()

    def update(self, form):
        self.content = form.get('content', '')
        self.save()
