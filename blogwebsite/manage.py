# always run on interpreter 3.7
from flask import Flask, render_template, request, session
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'secret-key'
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']

elif local_server:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

else:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = params['prod_uri']
db = SQLAlchemy(app)


# HERE Contacts is a table name
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    mes = db.Column(db.String(120), nullable=True)
    date = db.Column(db.String(12), nullable=False)


# HERE Blog is a table name
class Blog(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=False)


@app.route('/')
def home():
    blog = Blog.query.filter_by().all()[0:params['no_of_blogs']]
    return render_template('index.html', blog=blog, params=params)


@app.route('/blog', methods=['GET'])
def blog_main():
    blog = Blog.query.filter_by().all()
    return render_template('mainBlog.html', blog=blog, params=params)


@app.route('/blog/<string:blog_slug>', methods=['GET'])
def blog_route(blog_slug):
    blog = Blog.query.filter_by(slug=blog_slug).first()
    return render_template('blog.html', params=params, blog=blog)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, email=email, phone_num=phone, date=datetime.now(), mes=message)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)


@app.route('/about')
def about():
    return render_template('about.html', params=params)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form.get('usernm')
        userpassword = request.form.get('userpass')
        if username == params['adminuser'] and userpassword == params['adminpass']:
            session['user'] = username
            return render_template('dashboard.html', params=params)
    return render_template('login.html')


@app.route('/dashboard/add-new', methods=['GET', 'POST'])
def addnew():
    if request.method == 'POST':
        title = request.form.get('title')
        slug = request.form.get('slug')
        content = request.form.get('content')
        entry = Blog(title=title, slug=slug, date=datetime.now(), content=content)
        db.session.add(entry)
        db.session.commit()
    return render_template('dashboard.html', params=params)


if __name__ == '__main__':
    app.run(debug=True)
