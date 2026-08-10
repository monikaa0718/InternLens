from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY


def get_video_comments(youtube, video_id, max_comments=5):
    comments = []

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_comments,
            textFormat="plainText"
        )

        response = request.execute()

        for item in response.get("items", []):
            text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(text)

    except Exception:
        pass

    return comments


def search_youtube(company_name, max_results=5):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    query = f"{company_name} internship experience"

    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results
    )

    response = request.execute()

    results = []

    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]

        comments = get_video_comments(youtube, video_id)

        results.append({
            "platform": "youtube",
            "title": snippet["title"],
            "body": snippet.get("description", "") + " " + " ".join(comments),
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "author": snippet.get("channelTitle", ""),
            "date_posted": snippet.get("publishedAt", ""),
            "raw_score": None
        })

    return results