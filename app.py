from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

        # Success! New Bestbook!
        return render_template('bookPost.html', name = name, title = title, author = author, rating = rating, synopsis = synopsis, thoughts = thoughts)

    return render_template('book.html')