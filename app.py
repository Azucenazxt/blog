from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from models import db
# 这里 import 具体的 Model 类是为了给 migrate 用
# 如果不 import 那么无法迁移
# 这是 SQLAlchemy 的机制

from models.user import User
from models.blog import Blog



app = Flask(__name__)
db_path = 'blog.sqlite'
manager = Manager(app)

def register_routes(app):
    from routes.user import main as routes_user
    from routes.blog import main as routes_blog

    app.register_blueprint(routes_blog, url_prefix='/blog')
    app.register_blueprint(routes_user)


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    db.init_app(app)
    register_routes(app)

def configured_app():
    configure_app()
    return app


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=4000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()
