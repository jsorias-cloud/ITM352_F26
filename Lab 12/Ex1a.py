"""test Flask with this"""

from flask import Flask
app = Flask(__name__)

@app.route('/hey')
def hello():
    return '<strong>Welcome to Jorryns web site!</strong>'