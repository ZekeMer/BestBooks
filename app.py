from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BestBooks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(50), nullable = False)
    synopsis = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable = False)
    thoughts = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc))

with app.app_context():
    db.create_all()

# This should be book.html
@app.route("/")
def mainpage():
    return redirect(url_for('book'))

@app.route('/book', methods = ['GET', 'POST'])
def book():
    if request.method =="POST":
        name = request.form.get('name', '').strip()
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        synopsis = request.form.get('synopsis', '').strip()
        rating = request.form.get('rating', '').strip()
        thoughts = request.form.get('thoughts', '').strip()

        if not name or not rating or not title or not synopsis:
            msgOfDoom = "Error of Doom! Make sure all required fields are filled in!"
            return render_template('book.html', error = msgOfDoom)

        try:
            new_book = Book(name=name, title = title, author = author, synopsis = synopsis, rating = int(rating), thoughts = thoughts)
            db.session.add(new_book)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = "Your book couldn't be saved due to an error! Try again please."
            return render_template('book.html', error = error)

        # Success! New Bestbook!
        return render_template('bookPost.html', name = name, title = title, author = author, rating = rating, synopsis = synopsis, thoughts = thoughts)

    return render_template('book.html')

# This is the admin page from which to view the database!

@app.route('/admin/book')
def admin_book():
    books = Book.query.all()
    return render_template('admin_books.html', books = books)

@app.route('/admin/book/highRating')
def admin_book_highRating():
    try:
        book_rec = Book.query.filter(Book.rating >= 8).all()

        for book in book_rec:
            if "READ THIS" not in book.title:
                book.title += " - READ THIS"
        
        db.session.commit()

        return redirect(url_for('admin_book'))
    
    except Exception as e:
        db.session.rollback()
        uperror = f"Error updating BestBooks: {str(e)}"
        books = Book.query.all()
        return render_template('admin_books.html', books = books, error = uperror)