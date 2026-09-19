from transformers import pipeline

MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

sentiment_task = pipeline(
    "sentiment-analysis",
    model=MODEL,
    tokenizer=MODEL,
    truncation=True,
    max_length=128,
)

texts = [
    "Good night 😊",
    "I absolutely hate this.",
    "It's okay, nothing special.",
]

results = sentiment_task(texts, batch_size=8)
for text, r in zip(texts, results):
    print(f"{text!r:40} -> {r['label']:9} ({r['score']:.4f})")