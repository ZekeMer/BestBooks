from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# This should be book.html
@app.route("/")
def mainpage():
    return redirect(url_for('book'))

@app.route('/book', methods = ['GET', 'POST'])
def book():
        return render_template('book.html')