# 🎥 YouTube Comment Sentiment Analyzer

A Streamlit web app that analyzes YouTube video comments to provide sentiment insights and performance metrics using AI and data visualization. Just paste a video link and get detailed results!
## 🔍 Features

 ✅ Fetch video details (title, channel, views, likes, comments)
 ✅ Analyze sentiments (Positive, Negative, Neutral)
 ✅ Display summary metrics and pie charts
 ✅ Generate word clouds from comment text
 ✅ Overall video performance based on sentiment score
 ✅ Clean and interactive UI built with Streamlit
 ✅ API key stored securely using `.env` (not hardcoded)

## 🧠 Tech Stack

**Frontend**: Streamlit
**Backend**: Python
**APIs**: YouTube Data API v3
**NLP**: TextBlob
**Visualization**: Matplotlib, WordCloud

## 🚀 Demo

📺 Paste a YouTube video link and get:
 📊 Sentiment analysis of comments
 ☁️ Word cloud of commonly used words
 📈 Overall performance rating

## 📦 Project Structure

youtube_sentiment_analyzer/
│
├── app.py # Streamlit UI logic
├── youtube_api.py # YouTube API interaction
├── sentiment.py # Sentiment analysis with TextBlob
├── utils.py # Charts, metrics, word cloud
├── .env # API key (not committed)
├── .gitignore # Ignores .env and other sensitive files
├── requirements.txt # All dependencies
└── README.md # This file

## ✅ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/youtube-sentiment-analyzer.git
   cd youtube-sentiment-analyzer
2.Install dependencies

pip install -r requirements.txt

3.Create .env file (for your API key)

YOUTUBE_API_KEY=your_api_key_here

4.Run the app

streamlit run app.py

Check out the video:-
https://github.com/user-attachments/assets/259b1533-eed9-4f2a-b893-92e044d18776


