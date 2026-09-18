import json
import csv

input_file = "telegram_data.json"
output_file = "comments.csv"

# Read JSON
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Append comments to CSV
with open(output_file, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    for post in data.get("posts", []):
        for comment in post.get("comments", []):
            comment_text = comment.get("text", "")

            # Only append non-empty comments
            if comment_text.strip():
                writer.writerow([comment_text])

print("Comments appended successfully.")