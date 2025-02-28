from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd
import os
from typing import List, Dict
from dateutil.parser import parse

class YouTubeAnalyzer:
    def __init__(self, api_key: str):
        """Initialize the YouTube API client."""
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
    def _get_date_range(self) -> tuple:
        """Get date range for the last month."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        return start_date.isoformat('T') + 'Z', end_date.isoformat('T') + 'Z'

    def _load_keywords(self) -> List[str]:
        """Load keywords from config file."""
        keywords = []
        try:
            with open('config/keywords.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        keywords.append(line)
        except Exception as e:
            print(f"Error loading keywords: {str(e)}")
        return keywords

    def _process_video_data(self, item: dict, query: str = "") -> dict:
        """Process video data from API response."""
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Get video statistics
        video_response = self.youtube.videos().list(
            part='statistics,contentDetails',
            id=video_id
        ).execute()
        
        if video_response['items']:
            stats = video_response['items'][0]['statistics']
            
            return {
                'video_id': video_id,
                'url': video_url,
                'title': item['snippet']['title'],
                'channel_title': item['snippet']['channelTitle'],
                'published_at': parse(item['snippet']['publishedAt']),
                'view_count': int(stats.get('viewCount', 0)),
                'like_count': int(stats.get('likeCount', 0)),
                'comment_count': int(stats.get('commentCount', 0)),
                'search_query': query
            }
        return None

    def search_videos(self, query: str = "", use_keywords: bool = False, max_results: int = 50) -> pd.DataFrame:
        """Search for videos using query and/or predefined keywords."""
        start_date, end_date = self._get_date_range()
        all_videos = []

        # If use_keywords is True, search using predefined keywords
        if use_keywords:
            keywords = self._load_keywords()
            for keyword in keywords:
                try:
                    request = self.youtube.search().list(
                        q=keyword,
                        part='snippet',
                        type='video',
                        order='viewCount',
                        regionCode='US',
                        publishedAfter=start_date,
                        publishedBefore=end_date,
                        maxResults=max_results
                    )
                    response = request.execute()

                    for item in response.get('items', []):
                        video_data = self._process_video_data(item, keyword)
                        if video_data:
                            all_videos.append(video_data)
                            
                except Exception as e:
                    print(f"Error processing keyword '{keyword}': {str(e)}")
                    continue

        # If query is provided, search using the custom query
        elif query:
            try:
                request = self.youtube.search().list(
                    q=query,
                    part='snippet',
                    type='video',
                    order='viewCount',
                    regionCode='US',
                    publishedAfter=start_date,
                    publishedBefore=end_date,
                    maxResults=max_results
                )
                response = request.execute()

                for item in response.get('items', []):
                    video_data = self._process_video_data(item, query)
                    if video_data:
                        all_videos.append(video_data)
                        
            except Exception as e:
                print(f"Error processing query '{query}': {str(e)}")

        if not all_videos:
            return pd.DataFrame()

        df = pd.DataFrame(all_videos)
        df = df.sort_values('view_count', ascending=False)
        return df

    def analyze_trends(self, df: pd.DataFrame) -> Dict:
        """Analyze trends in the collected video data."""
        if df.empty:
            return {}

        analysis = {
            'total_videos': len(df),
            'total_views': df['view_count'].sum(),
            'avg_views': df['view_count'].mean(),
            'avg_likes': df['like_count'].mean(),
            'avg_comments': df['comment_count'].mean(),
            'top_channels': df['channel_title'].value_counts().head(10).to_dict(),
            'most_engaging_videos': df.nlargest(10, 'view_count')[['title', 'view_count', 'channel_title']].to_dict('records')
        }
        
        return analysis
