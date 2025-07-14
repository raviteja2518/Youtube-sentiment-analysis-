import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from googleapiclient.discovery import build
import re
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

# YouTube API Setup
# Replace with your actual API key
youtube = build("youtube", "v3", developerKey=API_KEY)

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def get_video_details(video_id):
    request = youtube.videos().list(part="snippet,statistics", id=video_id)
    response = request.execute()
    if response['items']:
        item = response['items'][0]
        snippet = item['snippet']
        stats = item['statistics']
        details = {
            'title': snippet['title'],
            'channel': snippet['channelTitle'],
            'published': snippet['publishedAt'][:10],
            'views': int(stats.get('viewCount', 0)),
            'likes': int(stats.get('likeCount', 0)),
            'comments': int(stats.get('commentCount', 0)),
            'description': snippet.get('description', '')
        }
        return details
    return None

def get_comments(video_id, max_comments=200):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    response = request.execute()

    while response and len(comments) < max_comments:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=response['nextPageToken'],
                maxResults=100,
                textFormat="plainText"
            )
            response = request.execute()
        else:
            break
    return comments[:max_comments]

def analyze_sentiments(comments):
    sentiment_data = {'Comment': [], 'Polarity': [], 'Sentiment': []}
    for comment in comments:
        polarity = TextBlob(comment).sentiment.polarity
        if polarity > 0:
            sentiment = 'Positive'
        elif polarity < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        sentiment_data['Comment'].append(comment)
        sentiment_data['Polarity'].append(polarity)
        sentiment_data['Sentiment'].append(sentiment)
    return pd.DataFrame(sentiment_data)

def create_wordcloud(text):
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

def display_metrics(data, video_details):
    pos = len(data[data['Sentiment'] == 'Positive'])
    neg = len(data[data['Sentiment'] == 'Negative'])
    neu = len(data[data['Sentiment'] == 'Neutral'])
    total = len(data)
    
    st.subheader("🔍 Sentiment Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("😊 Positive", pos)
    col2.metric("😐 Neutral", neu)
    col3.metric("😠 Negative", neg)

    fig, ax = plt.subplots()
    ax.pie([pos, neu, neg], labels=['Positive', 'Neutral', 'Negative'], autopct='%1.1f%%', colors=['#3adb76', '#ffae42', '#ec5840'])
    ax.axis('equal')
    st.pyplot(fig)

    # Overall Performance
    score = (pos - neg) / total * 100 if total else 0
    performance = "Excellent" if score > 60 else "Good" if score > 30 else "Average" if score > 0 else "Negative"
    st.subheader("📈 Overall Video Performance")
    st.success(f"Sentiment Score: {score:.2f}% — {performance}")

# Streamlit UI
st.set_page_config(page_title="YouTube Comment Sentiment Analyzer", layout="wide")
st.title("🎥 YouTube Comment Sentiment Analyzer")

video_url = st.text_input("Paste YouTube Video URL:")

if video_url:
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("❌ Invalid YouTube URL!")
    else:
        with st.spinner("Fetching video details..."):
            details = get_video_details(video_id)
            comments = get_comments(video_id)

        if details:
            st.markdown(f"## 📄 Video: {details['title']}")
            st.markdown(f"**Channel:** {details['channel']}")
            st.markdown(f"**Published On:** {details['published']}")
            st.markdown(f"**Views:** {details['views']:,} | 👍 Likes: {details['likes']:,} | 💬 Comments: {details['comments']:,}")

            st.markdown("---")
            st.subheader("📊 Sentiment Analysis on Comments")
            df = analyze_sentiments(comments)
            st.dataframe(df.head(10))

            display_metrics(df, details)

            st.subheader("☁️ Most Common Words")
            all_text = " ".join(df['Comment'])
            create_wordcloud(all_text)
        else:
            st.error("Failed to fetch video details. Please try a different URL.")