import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build

# Load the secret .env file
load_dotenv()

app = Flask(__name__)

# Get key from the environment
API_KEY = os.getenv("YOUTUBE_API_KEY")
if not API_KEY:
    raise ValueError("No YOUTUBE_API_KEY found in environment variables. Please check your .env file.")

youtube = build('youtube', 'v3', developerKey=API_KEY)

@app.route('/')
def loader():
    # This is your loading screen
    return render_template("loading.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    stats = None # Start with empty stats
    error = None

    # If the user clicked the "Submit" button
    if request.method == 'POST':
        # 1. Get the text from the HTML input
        # Make sure your HTML input has name="handle"
        user_input = request.form.get('handle') 

        if not user_input:
            error = "Please enter a handle."
        else:
            # FIX: The API 'forHandle' usually expects the '@' symbol.
            # If the user forgot it, we add it automatically.
            if not user_input.startswith('@'):
                user_input = f"@{user_input}"

            try:
                # 2. Call the YouTube API
                # Added 'snippet' to part so we can get the real channel title
                req = youtube.channels().list(
                    part="statistics,id,contentDetails,snippet",
                    forHandle=user_input 
                )
                response = req.execute()

                # 3. Check if we found data
                if response['items']:
                    data = response['items'][0]
                    # Store the data in a dictionary to send to HTML
                    stats = {
                        'title': data['snippet']['title'],
                        'subs': data['statistics']['subscriberCount'],
                        'views': data['statistics']['viewCount'],
                        'uploads_id': data['contentDetails']['relatedPlaylists']['uploads']
                    }
                else:
                    error = "Channel not found! Did you use the @ handle?"
            
            except Exception as e:
                error = f"An error occurred: {e}"

    # Render the home page, passing the stats (if any) or errors
    return render_template("home.html", stats=stats, error=error)

# IMPORTANT: This must be at the BOTTOM
if __name__ == '__main__':
    app.run(debug=True)