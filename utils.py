def create_wordcloud(text):
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    import streamlit as st
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

def display_metrics(data):
    import matplotlib.pyplot as plt
    import streamlit as st
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
    ax.pie([pos, neu, neg], labels=['Positive', 'Neutral', 'Negative'],
           autopct='%1.1f%%', colors=['#3adb76', '#ffae42', '#ec5840'])
    ax.axis('equal')
    st.pyplot(fig)

    score = (pos - neg) / total * 100 if total else 0
    performance = "Excellent" if score > 60 else "Good" if score > 30 else "Average" if score > 0 else "Negative"
    st.subheader("📈 Overall Video Performance")
    st.success(f"Sentiment Score: {score:.2f}% — {performance}")