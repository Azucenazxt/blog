import hashlib
import os

from . import ModelMixin
from . import db
from . import timestamp
from flask import session

class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    avatar = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    blogs = db.relationship('Blog', backref='user_b')


    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.avatar = form.get('avatar', '')
        self.created_time = timestamp()

    # 验证注册用户的合法性的
    def valid_register(self):
        valid_username = User.query.filter_by(username=self.username).first() == None
        valid_username_len = len(self.username) >= 3
        valid_password_len = len(self.password) >= 3
        if not valid_username:
            message = '用户名已经存在'
        elif not valid_username_len:
            message = '用户名长度必须大于等于 3'
        elif not valid_password_len:
            message = '密码长度必须大于等于 3'
        else:
            message = '注册成功'
        if self.avatar == '':
            self.avatar = 'http://vip.cocode.cc/uploads/avatar/default.png'
        status = valid_username and valid_username_len and valid_password_len
        return status, message

    def valid_login(self):
        u = User.query.filter_by(username=self.username).first()
        valid_username = (u is not None)
        if not valid_username:
            message = '用户名不存在'
        else:
            valid_password = self.password == u.password
            if not valid_password:
                message = '用户名或密码错误'
            else:
                session['user_id'] = u.id
                message = ''

        status = valid_username and valid_password
        return status, message
