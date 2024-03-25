from decouple import config
from googleapiclient.discovery import build
import requests

from interest.models import Interest, Recommendation, RecommendationVideo

API_KEY=config('GOOGLE_API_KEY')
CX = config('GOOGLE_API_CX')

#add data types
def search_and_insert_recommendations(interest : Interest , max_results=5) -> None:
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    query = interest.name
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        type='playlist',
        maxResults=max_results
    ).execute()

    for search_result in search_response.get('items', []):
        playlist_id = search_result['id']['playlistId']
        playlist_title = search_result['snippet']['title']
        playlist_thumbnail = search_result['snippet']['thumbnails']['default']['url']

        try:
            recommendation = Recommendation.objects.create(
                title=playlist_title,
                playlist_id=playlist_id,
                thumbnail=playlist_thumbnail
            )

            interest.recommendations.add(recommendation)

            playlist_videos = get_playlist_videos(youtube, playlist_id)

            for video_info in playlist_videos:
                    RecommendationVideo.objects.create(
                        recommendation=recommendation,
                        title=video_info['title'],
                        video_id=video_info['video_id'],
                        source='youtube',
                        thumbnail=video_info['thumbnail_url']
                    )

        except Exception as e:
            print(f"{e}\n")
            continue



        

def get_playlist_videos(youtube, playlist_id):
    playlist_items = []
    next_page_token = None

    while True:
        playlist_response = youtube.playlistItems().list(
            playlistId=playlist_id,
            part='snippet',
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for playlist_item in playlist_response.get('items', []):
            title = str(playlist_item['snippet'].get('title', ''))
            video_id = playlist_item['snippet']['resourceId'].get('videoId', '')

            thumbnails = playlist_item['snippet'].get('thumbnails', {})
            default_thumbnail = thumbnails.get('default', {})
            thumbnail_url = default_thumbnail.get('url', '')

            video_info = {
                'title': str(title),
                'video_id': video_id,
                'thumbnail_url': thumbnail_url
            }
            playlist_items.append(video_info)

        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break

    return playlist_items


def execute():
    for interest in Interest.objects.all():
        search_and_insert_recommendations(interest=interest)