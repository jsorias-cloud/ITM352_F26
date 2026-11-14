# Create a simple Flask application to retrieve da wholesome memes

import requests
from flask import Flask, render_template

app = Flask(__name__)

MEME_API_URL = "https://meme-api.com/gimme/wholesomememes"

@app.route('/')
def memes():
    try:
        response = requests.request("GET", MEME_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        meme_url = data["url"]
        subreddit = data["subreddit"]
        return render_template('memes.html', meme_url=meme_url, subreddit=subreddit)
    except (requests.RequestException, KeyError, ValueError):
        # Network problem or unexpected data from the API
        return render_template('memes.html', error="Couldn't load your meme. Trying again soon my bad..."), 502

if __name__ == '__main__':
    app.run(debug=True, port=5000)