from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# Configure MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/lib'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(3), nullable=False)
    pub_year = db.Column(db.Integer)

@app.route("/")
def home():
    db.create_all()

    return render_template('home.html')

@app.route("/books/")
def books():
    books = Book.query.all()
    
    return render_template('books.html', books = books)

@app.route("/add-book/")
@app.route("/add-book/<title>/<author>/<price>/<pub_year>")
def add_book(title = '', author = '', price = '', pub_year = ''):
    if title and author and price and pub_year:
        new_book = Book(title=title, author=author, price=price, pub_year=pub_year)
        db.session.add(new_book)
        db.session.commit()
    else:
        new_book = ''
    
    return render_template('add_book.html', new_book=new_book)

@app.route("/update-book/")
@app.route("/update-book/<id>/<title>/<author>/<price>/<pub_year>")
def upd_book(id = '', title = '', author = '', price = '', pub_year = ''):
    if id and title and author and price and pub_year:
        upd_book = Book.query.filter_by(id=id).first()
        upd_book.title = title
        upd_book.author = author
        upd_book.price = price
        upd_book.pub_year = pub_year
        db.session.commit()
    else:
        upd_book = ''

    return render_template('upd_book.html', upd_book=upd_book)

@app.route("/delete-book/")
@app.route("/delete-book/<id>")
def del_book(id = ''):
    deleted = False

    if id:
        del_book = Book.query.filter_by(id=id).first()
        db.session.delete(del_book)
        db.session.commit()
        deleted = True
        
    else:
        del_book = ''
    
    return render_template('del_book.html', deleted=deleted)