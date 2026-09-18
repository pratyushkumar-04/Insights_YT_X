import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from textblob import TextBlob

sys.path.append(str(Path(__file__).parent.parent))
from config import ENGAGEMENT_WEIGHTS, STOPWORDS


class DataAnalyzer:
    """Analyze YouTube data for insights."""

    def __init__(self, data: Dict = None):
        self.data = data
        self.df = None
        if data:
            self._create_dataframe()

    def _create_dataframe(self):
        rows = []
        for video_id, video_data in self.data.items():
            if 'error' in video_data:
                continue
            row = {'video_id': video_id, 'title': video_data.get('title', ''),
                     'description': video_data.get('description', ''), 'view_count': video_data.get('view_count') or 0,
                     'like_count': video_data.get('like_count') or 0, 'comment_count': video_data.get('comment_count') or 0,
                   'upload_date': video_data.get('upload_date', ''), 'uploader': video_data.get('uploader', ''),
                     'duration': video_data.get('duration') or 0, 'duration_string': video_data.get('duration_string', ''),
                   'tags': video_data.get('tags', []), 'categories': video_data.get('categories', []),
                   'comment_data': video_data.get('comments', [])}
            row['engagement_score'] = self._calculate_engagement(row)
            row['engagement_rate'] = row['engagement_score'] / row['view_count'] * 100 if row['view_count'] > 0 else 0
            rows.append(row)
        self.df = pd.DataFrame(rows)

    def _calculate_engagement(self, row: Dict) -> float:
        return row.get('like_count', 0) * ENGAGEMENT_WEIGHTS['like'] + row.get('comment_count', 0) * ENGAGEMENT_WEIGHTS['comment']

    def get_top_performers(self, n: int = 5, metric: str = 'engagement_rate') -> pd.DataFrame:
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        return self.df.sort_values(by=metric, ascending=False).head(n)[['title', 'view_count', 'like_count', 'comment_count', metric]]

    def analyze_comments(self) -> Dict:
        if self.df is None or self.df.empty:
            return {}
        comments = []
        for _, row in self.df.iterrows():
            for comment in row.get('comment_data', []):
                text = comment.get('text', '')
                if text and len(text) > 5:
                    sentiment = TextBlob(text).sentiment
                    comments.append({'text': text, 'video_title': row['title'], 'polarity': sentiment.polarity,
                                     'subjectivity': sentiment.subjectivity, 'comment_likes': comment.get('like_count', 0)})
        if not comments:
            return {'total_comments': 0}
        comment_df = pd.DataFrame(comments)
        comment_df['sentiment_category'] = comment_df['polarity'].apply(lambda value: 'positive' if value > 0.1 else ('negative' if value < -0.1 else 'neutral'))
        counts = comment_df['sentiment_category'].value_counts()
        positive = self._extract_keywords(comment_df[comment_df['sentiment_category'] == 'positive']['text'].tolist())
        negative = self._extract_keywords(comment_df[comment_df['sentiment_category'] == 'negative']['text'].tolist())
        return {'total_comments': len(comments), 'sentiment_distribution': counts.to_dict(),
                'average_polarity': comment_df['polarity'].mean(), 'average_subjectivity': comment_df['subjectivity'].mean(),
                'top_positive_keywords': positive[:10], 'top_negative_keywords': negative[:10],
                'most_liked_comments': comment_df.nlargest(5, 'comment_likes')[['text', 'comment_likes', 'video_title']].to_dict('records'),
                'most_negative_comments': comment_df.nsmallest(5, 'polarity')[['text', 'polarity', 'video_title']].to_dict('records'),
                'most_positive_comments': comment_df.nlargest(5, 'polarity')[['text', 'polarity', 'video_title']].to_dict('records')}

    def _extract_keywords(self, texts: List[str], n: int = 20) -> List[Tuple[str, int]]:
        combined = ' '.join(texts).lower()
        combined = re.sub(r'http\S+|www\S+|https\S+', '', combined)
        words = re.sub(r'[^a-zA-Z\s]', '', combined).split()
        return Counter(word for word in words if len(word) > 3 and word not in STOPWORDS).most_common(n)

    def analyze_timing_insights(self) -> Dict:
        if self.df is None or self.df.empty:
            return {}
        self.df['upload_datetime'] = pd.to_datetime(self.df['upload_date'], format='%Y%m%d', errors='coerce')
        self.df['upload_day'] = self.df['upload_datetime'].dt.day_name()
        performance = self.df.groupby('upload_day').agg({'view_count': 'mean', 'engagement_rate': 'mean'}).round(2)
        performance = performance.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        return {'best_day_for_views': performance['view_count'].idxmax() if not performance.empty else None,
                'best_day_for_engagement': performance['engagement_rate'].idxmax() if not performance.empty else None,
                'average_views_by_day': performance['view_count'].to_dict(), 'average_engagement_by_day': performance['engagement_rate'].to_dict()}

    def analyze_content_patterns(self) -> Dict:
        if self.df is None or self.df.empty:
            return {}
        self.df['title_length'] = self.df['title'].str.len()
        self.df['description_length'] = self.df['description'].str.len()
        tags = [tag for video_tags in self.df['tags'] for tag in video_tags]
        correlation = self.df[['duration', 'view_count', 'like_count', 'comment_count']].corr()
        return {'average_title_length': self.df['title_length'].mean(), 'average_description_length': self.df['description_length'].mean(),
                'common_tags': Counter(tags).most_common(10), 'duration_correlation': correlation.to_dict(),
                'best_performing_duration': self.df.loc[self.df['engagement_rate'].idxmax(), 'duration_string'] if not self.df.empty else None}

    def generate_summary_stats(self) -> Dict:
        if self.df is None or self.df.empty:
            return {}
        return {'total_videos': len(self.df), 'total_views': self.df['view_count'].sum(), 'total_likes': self.df['like_count'].sum(),
                'total_comments': self.df['comment_count'].sum(), 'average_views': self.df['view_count'].mean(),
                'average_likes': self.df['like_count'].mean(), 'average_comments': self.df['comment_count'].mean(),
                'average_engagement_rate': self.df['engagement_rate'].mean(), 'total_engagement_score': self.df['engagement_score'].sum(),
                'most_viewed_video': self.df.loc[self.df['view_count'].idxmax(), 'title'],
                'most_engaged_video': self.df.loc[self.df['engagement_rate'].idxmax(), 'title']}
