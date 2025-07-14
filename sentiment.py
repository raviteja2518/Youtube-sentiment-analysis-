def analyze_sentiments(comments):
    from textblob import TextBlob
    import pandas as pd
    sentiment_data = {'Comment': [], 'Polarity': [], 'Sentiment': []}
    for comment in comments:
        polarity = TextBlob(comment).sentiment.polarity
        sentiment = 'Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral'
        sentiment_data['Comment'].append(comment)
        sentiment_data['Polarity'].append(polarity)
        sentiment_data['Sentiment'].append(sentiment)
    return pd.DataFrame(sentiment_data)