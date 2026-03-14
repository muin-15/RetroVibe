import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build

load_dotenv()

app = Flask(__name__)

# Get key from the environment
API_KEY = os.getenv("YOUTUBE_API_KEY")
if not API_KEY:
    raise ValueError("No YOUTUBE_API_KEY found in environment variables. Please check your .env file.")

youtube = build('youtube', 'v3', developerKey=API_KEY)

@app.route('/')
def loader():
    return render_template("loading.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    stats = None 
    error = None
    if request.method == 'POST':
        user_input = request.form.get('handle') 

        if not user_input:
            error = "Please enter a handle."
        else:
            if not user_input.startswith('@'):
                user_input = f"@{user_input}"

            try:
                req = youtube.channels().list(
                    part="statistics,id,contentDetails,snippet",
                    forHandle=user_input 
                )
                response = req.execute()

                if response['items']:
                    data = response['items'][0]
                    stats = {
                        'title': data['snippet']['title'],
                        'subs': f"{int(data['statistics']['subscriberCount']):,}",
                        'views': f"{int(data['statistics']['viewCount']):,}",
                        'uploads_id': data['contentDetails']['relatedPlaylists']['uploads']
                    }
                else:
                    error = "Channel not found! Did you use the @ handle?"
            except Exception as e:
                error = f"An error occurred: {e}"
    return render_template("home.html", stats=stats, error=error)

if __name__ == '__main__':
    app.run(debug=True)