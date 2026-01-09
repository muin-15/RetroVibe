import os
from dotenv import load_dotenv
from flask import Flask, render_template #request
#from googleapiclient.discovery import build
#from textblob import TextBlob

# Load the secret .env file
load_dotenv()

app = Flask(__name__)

# Get key from the environment (Safe way)
API_KEY = os.getenv("YOUTUBE_API_KEY")
@app.route('/')
def hello():
    return render_template("loading.html")
@app.route('/home')
def home():
    return render_template("home.html")
if __name__ == '__main__':
    app.run(debug=True)