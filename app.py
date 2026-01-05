import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from googleapiclient.discovery import build
from textblob import TextBlob

# Load the secret .env file
load_dotenv()

app = Flask(__name__)

# Get key from the environment (Safe way)
API_KEY = os.getenv("YOUTUBE_API_KEY")

def analyze_comments(video_id):
    if not API_KEY:
        return "Error", [{"text": "API Key missing! Please check .env file", "score": 0}]

    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100
    )
    response = request.execute()
    
    comments = []
    total_polarity = 0
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        blob = TextBlob(comment)
        polarity = blob.sentiment.polarity
        comments.append({'text': comment, 'score': round(polarity, 2)})
        total_polarity += polarity
    
    avg_polarity = total_polarity / len(comments) if comments else 0
    if avg_polarity > 0.1:
        vibe = "Positive"
    elif avg_polarity < -0.1:
        vibe = "Negative"
    else:
        vibe = "Neutral"
    
    return vibe, comments

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        # Extract video_id from URL
        if 'v=' in url:
            video_id = url.split('v=')[1].split('&')[0]
        else:
            return render_template('index.html', vibe="Error", comments=[{"text": "Invalid URL", "score": 0}])
        
        vibe, comments = analyze_comments(video_id)
        return render_template('index.html', vibe=vibe, comments=comments)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)