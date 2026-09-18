#!/usr/bin/env python3
"""
YouTube Creator Growth Insights Tool
A complete tool for analyzing YouTube videos and generating growth insights
"""

import os
import sys
import time
from pathlib import Path
from src.twitter_scraper import TwitterScraper
from src.youtube_extractor import YouTubeExtractor
from src.utils import get_video_id_from_url
from colorama import init, Fore, Style

# Import the new function
from src.youtube_extractor import get_channel_video_urls

init(autoreset=True)

def main():
    print("\n" + "="*60)
    print(f"{Fore.CYAN}🚀 YOUTUBE CREATOR GROWTH INSIGHTS TOOL")
    print("="*60 + "\n")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Extract data from a single video")
        print("2. Extract data from a channel (by handle)")
        print("3. Extract data from Twitter/X")
        print("4. Exit")
        
        choice = input(f"\n{Fore.YELLOW}Enter your choice (1-4): {Style.RESET_ALL}")
        
        if choice == '1':
            extract_single_video()
        elif choice == '2':
            extract_channel_videos()
        elif choice == '3':
            extract_twitter_data()
        elif choice == '4':
            print(f"\n{Fore.GREEN}👋 Goodbye!")
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice. Please enter 1, 2, 3, or 4.")

def extract_single_video():
    """Extract data from a single YouTube video"""
    extractor = YouTubeExtractor()
    
    print(f"\n{Fore.CYAN}📹 Single Video Extraction")
    print("-" * 40)
    
    # Get video URL or ID
    video_input = input("\n📎 Enter YouTube URL or Video ID: ").strip().strip('"\'')
    
    if not video_input:
        print(f"{Fore.RED}❌ No input provided.")
        return
    
    video_id = get_video_id_from_url(video_input)
    if not video_id:
        print(f"{Fore.RED}❌ Invalid YouTube URL or Video ID.")
        return
    
    # Ask for comments
    fetch_comments = input(f"\n{Fore.YELLOW}Fetch comments? (y/n, default: y): {Style.RESET_ALL}").strip().lower() != 'n'
    
    # Extract data
    print(f"\n{Fore.CYAN}🔍 Processing video {video_id}...")
    data = extractor.get_video_data(video_id, fetch_comments)
    
    if 'error' in data:
        print(f"{Fore.RED}❌ Error: {data['error']}")
        return
    
    # Save the data
    extractor.save_results({video_id: data})
    
    print(f"\n{Fore.GREEN}✅ Extraction complete!")
    print(f"📊 Video: {data.get('title')}")
    print(f"   Views: {(data.get('view_count') or 0):,}")
    print(f"   Likes: {(data.get('like_count') or 0):,}")
    print(f"   Comments: {(data.get('comment_count') or 0):,}")

def extract_channel_videos():
    """Extract all videos from a YouTube channel by handle or URL"""
    extractor = YouTubeExtractor()
    
    print(f"\n{Fore.CYAN}📺 Channel Video Extraction")
    print("-" * 40)
    
    # Get channel handle or URL
    channel_input = input("\n📎 Enter YouTube channel handle or URL (e.g., @MrBeast or https://www.youtube.com/@MrBeast): ").strip().strip('"\'')
    
    if not channel_input:
        print(f"{Fore.RED}❌ No input provided.")
        return
    
    # Get max videos
    max_videos_input = input(f"\n{Fore.YELLOW}Maximum videos to fetch? (default: all, or enter number): {Style.RESET_ALL}").strip()
    max_videos = None
    if max_videos_input.isdigit() and int(max_videos_input) > 0:
        max_videos = int(max_videos_input)
        print(f"   Will fetch up to {max_videos} videos")
    else:
        print("   Will fetch ALL videos from the channel")
    
    # Fetch video URLs from channel
    print(f"\n{Fore.CYAN}🔍 Fetching video list from {channel_input}...")
    video_urls = get_channel_video_urls(channel_input, max_videos)
    
    if not video_urls:
        print(f"{Fore.RED}❌ No videos found for channel: {channel_input}")
        return
    
    print(f"\n{Fore.GREEN}✅ Found {len(video_urls)} videos")
    
    # Ask for comments
    fetch_comments = input(f"\n{Fore.YELLOW}Fetch comments for each video? (y/n, default: n - slower): {Style.RESET_ALL}").strip().lower() == 'y'
    
    # Ask for batch processing
    print(f"\n{Fore.YELLOW}⚠️  This will process {len(video_urls)} videos and may take time.")
    confirm = input(f"Continue? (y/n): {Style.RESET_ALL}").strip().lower()
    
    if confirm != 'y':
        print(f"{Fore.RED}❌ Operation cancelled.")
        return
    
    # Process all videos
    print(f"\n{Fore.CYAN}🚀 Starting batch extraction for {len(video_urls)} videos...")
    
    # Convert URLs to video IDs
    video_ids = []
    for url in video_urls:
        video_id = get_video_id_from_url(url)
        if video_id:
            video_ids.append(video_id)
    
    # Extract data in batches
    results = extractor.batch_extract(video_ids, fetch_comments)
    
    # Show summary
    print(f"\n{Fore.GREEN}✅ Extraction complete!")
    successful = sum(1 for v in results.values() if 'error' not in v)
    failed = len(results) - successful
    print(f"📊 Processed {len(results)} videos")
    print(f"✅ Successful: {successful}")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    
    print(f"\n{Fore.GREEN}Raw data saved.")


def extract_twitter_data():
    """Extract raw Twitter/X data through the terminal menu."""
    print(f"\n{Fore.CYAN}🐦 Twitter/X Data Extraction")
    print("-" * 40)

    auth_token = input(f"\n{Fore.YELLOW}Enter Twitter/X auth token (required): {Style.RESET_ALL}").strip().strip('"\'')
    if not auth_token:
        auth_token = os.getenv("TWITTER_AUTH_TOKEN")

    if not auth_token:
        print(f"{Fore.RED}❌ Twitter/X auth token is required. Please provide one and try again.")
        return

    print(f"{Fore.GREEN}Auth token received. Proceeding with authenticated requests.")

    scraper = TwitterScraper(auth_token=auth_token)
    try:
        while True:
            print("\nTwitter/X options:")
            print("1. Get user profile")
            print("2. Get recent posts for a user")
            print("3. Get tweet by URL or ID")
            print("4. Search tweets")
            print("5. Back")

            twitter_choice = input(f"\n{Fore.YELLOW}Choose an action (1-5): {Style.RESET_ALL}").strip()

            try:
                if twitter_choice == '1':
                    username = input("Enter Twitter/X username: ").strip().strip('"\'').lstrip('@')
                    if not username:
                        print(f"{Fore.RED}❌ Username cannot be empty.")
                        continue
                    print(f"\n{Fore.CYAN}🔍 Fetching profile for @{username}...")
                    result = scraper.get_profile(username)
                    out_path = Path(f"data/twitter/{username}_profile.json")
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    scraper.export(result, out_path, "json")
                    print(f"\n{Fore.GREEN}✅ Profile saved to: {out_path}")
                    print(f"👤 @{result.get('username') or username} ({result.get('display_name') or 'N/A'})")
                    print(f"   Followers: {(result.get('followers') or 0):,}")
                    print(f"   Following: {(result.get('following') or 0):,}")
                    print(f"   Tweets: {(result.get('tweet_count') or 0):,}")
                    if result.get('bio'):
                        print(f"   Bio: {result.get('bio')}")

                elif twitter_choice == '2':
                    username = input("Enter Twitter/X username: ").strip().strip('"\'').lstrip('@')
                    if not username:
                        print(f"{Fore.RED}❌ Username cannot be empty.")
                        continue
                    count_input = input("How many posts? (default: 20): ").strip()
                    count = int(count_input) if count_input.isdigit() and int(count_input) > 0 else 20
                    print(f"\n{Fore.CYAN}🔍 Fetching up to {count} posts for @{username}...")
                    posts = scraper.get_user_posts(username, count)
                    out_path = Path(f"data/twitter/{username}_posts.json")
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    scraper.export(posts, out_path, "json")
                    print(f"\n{Fore.GREEN}✅ Saved {len(posts)} posts to: {out_path}")
                    if posts:
                        print(f"   Latest post: \"{posts[0].get('text', '')[:70]}...\"")

                elif twitter_choice == '3':
                    value = input("Enter tweet URL or tweet ID: ").strip().strip('"\'')
                    if not value:
                        print(f"{Fore.RED}❌ Tweet URL or ID cannot be empty.")
                        continue
                    fetch_comments = input(f"\n{Fore.YELLOW}Fetch comments/replies for this tweet? (y/n, default: y): {Style.RESET_ALL}").strip().lower() != 'n'
                    print(f"\n{Fore.CYAN}🔍 Extracting tweet and comments...")
                    tweet = scraper.extract_post(value, fetch_replies=fetch_comments, max_replies=50)
                    out_path = Path("data/twitter/tweet.json")
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    scraper.export(tweet, out_path, "json")
                    print(f"\n{Fore.GREEN}✅ Tweet saved to: {out_path}")
                    print(f"💬 Author: @{tweet.get('author_username') or 'N/A'}")
                    print(f"   Text: \"{tweet.get('text', '')[:100]}\"")
                    print(f"   Likes: {(tweet.get('likes') or 0):,}")
                    print(f"   Retweets: {(tweet.get('retweets') or 0):,}")
                    print(f"   Replies count (total): {(tweet.get('replies') or 0):,}")
                    if fetch_comments:
                        print(f"   Comments fetched: {len(tweet.get('replies_data', []))}")

                elif twitter_choice == '4':
                    query = input("Enter search query: ").strip().strip('"\'')
                    if not query:
                        print(f"{Fore.RED}❌ Search query cannot be empty.")
                        continue
                    count_input = input("How many results? (default: 20): ").strip()
                    count = int(count_input) if count_input.isdigit() and int(count_input) > 0 else 20
                    print(f"\n{Fore.CYAN}🔍 Searching for \"{query}\"...")
                    results = scraper.search_tweets(query, count=count)
                    out_path = Path("data/twitter/search_results.json")
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    scraper.export(results, out_path, "json")
                    print(f"\n{Fore.GREEN}✅ Saved {len(results)} search results to: {out_path}")
                    if results:
                        print(f"   Top result from @{results[0].get('author_username') or 'N/A'}: \"{results[0].get('text', '')[:70]}...\"")

                elif twitter_choice == '5':
                    print(f"\n{Fore.GREEN}Returning to the main menu.")
                    return

                else:
                    print(f"{Fore.RED}❌ Invalid choice. Please enter 1, 2, 3, 4, or 5.")
            except Exception as exc:
                print(f"{Fore.RED}❌ Twitter/X request failed: {exc}")
                print(f"{Fore.YELLOW}Please verify the username/URL or check your auth token.")
                continue
    finally:
        scraper.close()

if __name__ == "__main__":
    main()