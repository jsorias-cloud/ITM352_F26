# Skeleton of a quiz game using mock-up pages (Method 1)
# Home -> Quiz -> Result -> High Score, with links to navigate between them

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/highscore')
def highscore():
    return render_template('highscore.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)