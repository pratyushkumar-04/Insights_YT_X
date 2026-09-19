export function getSentimentSummary(data) {
  let positive = 0;
  let negative = 0;
  let neutral = 0;
  let mixed = 0;

  for (const post of data.posts || []) {
    for (const comment of post.comments || []) {
      const label =
        comment.sentiment?.label?.toLowerCase();

      switch (label) {
        case "positive":
          positive++;
          break;
        case "negative":
          negative++;
          break;
        case "neutral":
          neutral++;
          break;
        case "mixed":
          mixed++;
          break;
      }
    }
  }

  const total =
    positive +
    negative +
    neutral +
    mixed;

  const percentage = (count) =>
    total === 0
      ? 0
      : Number(((count / total) * 100).toFixed(2));

  return {
    total_comments: total,

    positive: {
      count: positive,
      percentage: percentage(positive),
    },

    negative: {
      count: negative,
      percentage: percentage(negative),
    },

    neutral: {
      count: neutral,
      percentage: percentage(neutral),
    },

    mixed: {
      count: mixed,
      percentage: percentage(mixed),
    },
  };
}