from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_moment import Moment
from datetime import datetime
import forgery_py
from slugify import slugify

app = Flask(__name__)
app.debug = True

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

moment = Moment(app)
manager = Manager(app)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    slug = db.Column(db.String(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blog/')
def blog():
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Post).order_by(-Post.id).paginate()
    posts = pagination.items
    return render_template('blog.html', pagination=pagination, posts=posts)


@app.route('/blog/<post_id>/<post_slug>/')
def post(post_id, post_slug):
    post = db.session.query(Post).filter(Post.id == post_id).first_or_404()    
    return render_template('single_post.html', post=post)


if __name__ == '__main__':
    manager.run()