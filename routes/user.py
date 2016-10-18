from models.user import User
from routes import *


main = Blueprint('user', __name__)

Model = User

@main.route('/')
def login_index(msgs=''):
    return render_template('user_login.html', msgs=msgs)


@main.route('/register')
def registe_index(msgs=''):
    return render_template('user_register.html', msgs=msgs)


@main.route('/user/register', methods=['POST'])
def register():
    form = request.form
    m = Model(form)
    message = m.valid_register()
    if message[0]:
        m.save()
    msgs = message[1]
    return render_template('user_login.html', msgs=msgs)


@main.route('/user/login', methods=['POST'])
def login():
    form = request.form
    m = Model(form)
    message = m.valid_login()
    if message[0]:
        return redirect(url_for('blog.index'))
    else:
        msgs = message[1]
    return render_template('user_login.html', msgs=msgs)
