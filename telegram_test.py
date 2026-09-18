import asyncio
import json
from datetime import datetime, timedelta, timezone

from telethon import TelegramClient, functions


API_ID = 31920252
API_HASH = "6244bb0e034408e82714dff8a4790d5e"

client = TelegramClient("telegram_session", API_ID, API_HASH)

MAX_POSTS = 20
MAX_POPULAR_POSTS = 5
MAX_COMMENTS = 100
MONTHS = 6


def engagement_score(post):
    views = post.get("views") or 0
    forwards = post.get("forwards") or 0
    comments = len(post.get("comments", []))

    return (
        views * 1.0
        + forwards * 15.0
        + comments * 25.0
    )


async def get_comments(channel, post):
    if not post.replies or not post.replies.replies:
        return []

    try:
        discussion = await client(
            functions.messages.GetDiscussionMessageRequest(
                peer=channel,
                msg_id=post.id
            )
        )

        if not discussion.messages or not discussion.chats:
            return []

        discussion_message = discussion.messages[0]
        discussion_chat = discussion.chats[0]

        comments = await client.get_messages(
            discussion_chat,
            reply_to=discussion_message.id,
            limit=MAX_COMMENTS
        )

        result = []

        for comment in comments:
            sender = await comment.get_sender()

            result.append({
                "id": comment.id,
                "date": comment.date.isoformat()
                if comment.date else None,
                "author": {
                    "username": getattr(sender, "username", None),
                    "first_name": getattr(sender, "first_name", None),
                    "last_name": getattr(sender, "last_name", None)
                },
                "text": comment.text
            })

        return result

    except Exception as e:
        print(f"Error getting comments for post {post.id}: {e}")
        return []


async def main():
    channel_url = input("Enter Telegram channel URL: ").strip()

    channel = await client.get_entity(channel_url)

    print(f"\nChannel: {channel.title}")
    print(f"Username: @{channel.username}")
    print("Fetching latest posts...\n")

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=MONTHS * 30)

    posts = []

    async for post in client.iter_messages(
        channel,
        limit=MAX_POSTS
    ):
        if not post.date:
            continue

        post_date = post.date

        if post_date.tzinfo is None:
            post_date = post_date.replace(tzinfo=timezone.utc)

        if post_date < cutoff_date:
            break

        print(f"Processing post {len(posts) + 1}/{MAX_POSTS}...")

        comments = await get_comments(channel, post)

        post_data = {
            "id": post.id,
            "date": post.date.isoformat(),
            "text": post.text,
            "views": post.views or 0,
            "forwards": post.forwards or 0,
            "comments": comments
        }

        post_data["popularity_score"] = engagement_score(post_data)

        posts.append(post_data)

        if len(posts) >= MAX_POSTS:
            break

    popular_posts = sorted(
        posts,
        key=lambda post: post["popularity_score"],
        reverse=True
    )[:MAX_POPULAR_POSTS]

    data = {
        "posts": posts,
        "popular_posts": popular_posts
    }

    with open("telegram_data.json", "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"\nExtracted {len(posts)} posts.")
    print(f"Selected {len(popular_posts)} popular posts.")
    print("Saved to telegram_data.json")


async def run():
    await client.start()
    await main()


asyncio.run(run())