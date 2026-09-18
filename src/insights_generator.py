import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

sys.path.append(str(Path(__file__).parent.parent))
from src.data_analyzer import DataAnalyzer


class InsightsGenerator:
    """Generate actionable growth insights for creators."""

    def __init__(self, data: Dict):
        self.data = data
        self.analyzer = DataAnalyzer(data)
        self.insights = {}

    def generate_all_insights(self) -> Dict:
        print("\nGenerating insights...\n")
        self.insights['summary'] = self.analyzer.generate_summary_stats()
        self.insights['top_performers'] = self.analyzer.get_top_performers(5).to_dict('records')
        self.insights['comment_analysis'] = self.analyzer.analyze_comments()
        self.insights['timing_insights'] = self.analyzer.analyze_timing_insights()
        self.insights['content_patterns'] = self.analyzer.analyze_content_patterns()
        self.insights['recommendations'] = self._generate_recommendations()
        return self.insights

    def _generate_recommendations(self) -> List[Dict]:
        recommendations = []
        duration = self.insights.get('content_patterns', {}).get('best_performing_duration')
        if duration:
            recommendations.append({'category': 'content', 'priority': 'high', 'title': 'Optimal Video Duration',
                                    'description': f'Your best-performing videos are around {duration} long.', 'action': f'Target video length: {duration}'})
        best_day = self.insights.get('timing_insights', {}).get('best_day_for_engagement')
        if best_day:
            recommendations.append({'category': 'timing', 'priority': 'medium', 'title': 'Best Posting Day',
                                    'description': f'Your videos get the highest engagement when posted on {best_day}.', 'action': f'Schedule your next video for {best_day}'})
        sentiment = self.insights.get('comment_analysis', {})
        positive = sentiment.get('top_positive_keywords', [])
        if positive:
            keywords = ', '.join(word for word, _ in positive[:5])
            recommendations.append({'category': 'audience', 'priority': 'high', 'title': 'What Your Audience Loves',
                                    'description': f'Your audience responds positively to content about: {keywords}', 'action': f'Include these topics more often: {keywords}'})
        negative = sentiment.get('top_negative_keywords', [])
        if negative:
            keywords = ', '.join(word for word, _ in negative[:3])
            recommendations.append({'category': 'improvement', 'priority': 'medium', 'title': 'Areas for Improvement',
                                    'description': f'Some viewers have concerns about: {keywords}', 'action': f'Address these topics in future videos: {keywords}'})
        liked = sentiment.get('most_liked_comments', [])
        if liked:
            top = liked[0]
            recommendations.append({'category': 'engagement', 'priority': 'medium', 'title': 'Most Engaging Comment',
                                    'description': f"Top comment with {top['comment_likes']} likes: '{top['text'][:100]}...'", 'action': 'Pin this comment or create content addressing it'})
        average_rate = self.insights.get('summary', {}).get('average_engagement_rate', 0)
        if average_rate < 5:
            recommendations.append({'category': 'engagement', 'priority': 'high', 'title': 'Boost Your Engagement',
                                    'description': f'Your current engagement rate is {average_rate:.2f}%.', 'action': 'Add calls-to-action and ask viewers to comment'})
        elif average_rate > 10:
            recommendations.append({'category': 'engagement', 'priority': 'low', 'title': 'Great Engagement!',
                                    'description': f'Your engagement rate of {average_rate:.2f}% is above industry average!', 'action': 'Keep engaging with your community'})
        return recommendations

    def export_insights(self, filename: str = None):
        filename = filename or f"insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = Path(__file__).parent.parent / 'data' / filename
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(self.insights, file, indent=2, ensure_ascii=False,
                      default=lambda value: value.item() if hasattr(value, 'item') else str(value))
        print(f"\nInsights exported to: {filepath}")
        return filepath

    def print_summary(self):
        print("\n" + "=" * 60 + "\nYOUTUBE CREATOR INSIGHTS SUMMARY\n" + "=" * 60)
        summary = self.insights.get('summary', {})
        if summary:
            print(f"\nOverall Performance:\n  Videos analyzed: {summary.get('total_videos', 0)}\n  Total views: {summary.get('total_views', 0):,}\n  Average views: {summary.get('average_views', 0):,.0f}\n  Average engagement rate: {summary.get('average_engagement_rate', 0):.2f}%")
        for index, video in enumerate(self.insights.get('top_performers', [])[:3], 1):
            print(f"\n{index}. {video.get('title', 'N/A')[:50]}...\n   Views: {video.get('view_count', 0):,} | Engagement: {video.get('engagement_rate', 0):.2f}%")
        high_priority = [item for item in self.insights.get('recommendations', []) if item.get('priority') == 'high']
        if high_priority:
            print("\nActionable Recommendations:")
            for item in high_priority[:3]:
                print(f"\n{item.get('title', '')}\n  {item.get('description', '')}\n  Action: {item.get('action', '')}")
        print("\n" + "=" * 60)
