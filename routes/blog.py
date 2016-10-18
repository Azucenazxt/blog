from models.blog import Blog
from routes import *


main = Blueprint('blog', __name__)


Model = Blog

@main.route('/')
@login_required
def index():
    u = current_user()
    return render_template('blog_index.html', user=u)



@main.route('/edit/<id>')
def edit(id):
    m = Model.query.filter_by(id=id).first()
    return render_template('blog_edit.html', m=m)


@main.route('/new')
def new():
    u = current_user()
    return render_template('blog_new.html', user=u)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Model(form)
    m.user_id = int(form.get('user_id'))
    m.save()
    return redirect(url_for('.index'))


@main.route('/update/<id>', methods=['POST'])
def update(id):
    form = request.form
    m = Model.query.filter_by(id=id).first()
    m.update(form)
    return redirect(url_for('.index'))
#
#
@main.route('/delete/<id>')
def delete(id):
    m = Model.query.filter_by(id=id).first()
    m.delete()
    return redirect(url_for('.index'))
