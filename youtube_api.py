def extract_video_id(url):
    import re
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def get_video_details(video_id, youtube):
    request = youtube.videos().list(part="snippet,statistics", id=video_id)
    response = request.execute()
    if response['items']:
        item = response['items'][0]
        snippet = item['snippet']
        stats = item['statistics']
        return {
            'title': snippet['title'],
            'channel': snippet['channelTitle'],
            'published': snippet['publishedAt'][:10],
            'views': int(stats.get('viewCount', 0)),
            'likes': int(stats.get('likeCount', 0)),
            'comments': int(stats.get('commentCount', 0)),
            'description': snippet.get('description', '')
        }
    return None

def get_comments(video_id, youtube, max_comments=200):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet", videoId=video_id, maxResults=100, textFormat="plainText")
    response = request.execute()
    while response and len(comments) < max_comments:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet", videoId=video_id, maxResults=100,
                pageToken=response['nextPageToken'], textFormat="plainText")
            response = request.execute()
        else:
            break
    return comments[:max_comments]