import express from "express";
import cors from "cors";
import axios from "axios";

import {
  extractTwitterData,
  extractYouTubeData,
  extractTelegramData,
} from "./helper/refactor.js";

const app = express();

const PORT = 8001;

// ============================================================
// Middleware
// ============================================================

app.use(express.json());

app.use(
  cors({
    origin: "http://localhost:5173",
    credentials: true,
  })
);

// ============================================================
// Upstream API URLs
// ============================================================

const TWITTER_API =
  "http://localhost:8000/twitter/user";

const YOUTUBE_CHANNEL_API =
  "http://localhost:8000/youtube/channel";

const YOUTUBE_VIDEO_API =
  "http://localhost:8000/youtube/video";

const TELEGRAM_API =
  "http://localhost:8000/telegram/channel";

// ============================================================
// Twitter
// ============================================================

async function fetchTwitterPosts(username) {
  console.log(
    `\n[Twitter] Fetching posts for: ${username}`
  );

  const response = await axios.post(
    TWITTER_API,
    {
      username,
      include_posts: true,
      max_posts: 5,
    }
  );

  const posts =
    response.data?.posts || [];

  console.log(
    `[Twitter] Received ${posts.length} posts`
  );

  return posts;
}

// ============================================================
// YouTube - Fetch channel videos
// ============================================================

async function fetchYouTubeVideos(channelUsername) {
  const channelUrl =
    `https://www.youtube.com/@${channelUsername}`;

  console.log(
    `\n[YouTube] Fetching channel: ${channelUrl}`
  );

  const response = await axios.post(
    YOUTUBE_CHANNEL_API,
    {
      channel_url: channelUrl,
      max_videos: 5,
      include_comments: true,
    }
  );

  const videos =
    response.data?.videos || [];

  console.log(
    `[YouTube] Channel API returned ${videos.length} videos`
  );

  return videos;
}

// ============================================================
// YouTube - Fetch individual video details
// ============================================================

async function fetchYouTubeVideoDetails(video) {
  const videoUrl =
    `https://www.youtube.com/watch?v=${video.video_id}`;

  console.log(
    `[YouTube] Fetching details for video: ${video.video_id}`
  );

  const response = await axios.post(
    YOUTUBE_VIDEO_API,
    {
      video_url: videoUrl,
      include_comments: true,
      include_transcript: true,
    }
  );

  return response.data;
}

// ============================================================
// Telegram
// ============================================================

async function fetchTelegramPosts(channelUrl) {
  console.log(
    `\n[Telegram] Fetching posts for: ${channelUrl}`
  );

  const response = await axios.post(
    TELEGRAM_API,
    {
      
        channel_name: channelUrl,
        limit: 20
      
    }
  );

  console.log(
    `[Telegram] Received ${
      response.data?.messages?.length || 0
    } messages`
  );

  return response.data;
}

// ============================================================
// Axios Error Logger
// ============================================================

function logAxiosError(error) {
  console.error("\n========== API ERROR ==========");

  console.error(
    "Message:",
    error.message
  );

  if (axios.isAxiosError(error)) {
    console.error(
      "Axios error code:",
      error.code
    );

    console.error(
      "Method:",
      error.config?.method
    );

    console.error(
      "URL:",
      error.config?.url
    );

    if (error.response) {
      console.error(
        "Status:",
        error.response.status
      );

      console.error(
        "Response data:",
        error.response.data
      );

      console.error(
        "Response headers:",
        error.response.headers
      );
    } else if (error.request) {
      console.error(
        "No response received from upstream API"
      );

      console.error(
        "Request:",
        error.request
      );
    } else {
      console.error(
        "Request setup error:",
        error.message
      );
    }
  }

  console.error(
    "Full error:",
    error
  );

  console.error(
    "================================\n"
  );
}

// ============================================================
// Main Controller
// ============================================================

export async function getSocialMediaData(req, res) {
  try {
    const {
      twitter_username,
      youtube_username,
      telegram_channel,
    } = req.body;

    console.log(
      "\n========================================"
    );

    console.log(
      "Starting social media data collection"
    );

    console.log(
      "========================================"
    );

    // ========================================================
    // Create an array of requests that actually exist
    // ========================================================

    const requests = [];

    // --------------------------------------------------------
    // Twitter
    // --------------------------------------------------------

    if (twitter_username) {
      requests.push(
        fetchTwitterPosts(
          twitter_username
        )
          .then((posts) => ({
            platform: "twitter",
            data: posts,
          }))
      );
    }

    // --------------------------------------------------------
    // YouTube
    // --------------------------------------------------------

    if (youtube_username) {
      requests.push(
        fetchYouTubeVideos(
          youtube_username
        )
          .then((videos) => ({
            platform: "youtube",
            data: videos,
          }))
      );
    }

    // --------------------------------------------------------
    // Telegram
    // --------------------------------------------------------

    if (telegram_channel) {
      requests.push(
        fetchTelegramPosts(
          telegram_channel
        )
          .then((data) => ({
            platform: "telegram",
            data,
          }))
      );
    }

    // ========================================================
    // Execute available platform requests concurrently
    // ========================================================

    const results =
      await Promise.all(requests);

    // ========================================================
    // Find each platform's result
    // ========================================================

    const twitterResult =
      results.find(
        (result) =>
          result.platform === "twitter"
      );

    const youtubeResult =
      results.find(
        (result) =>
          result.platform === "youtube"
      );

    const telegramResult =
      results.find(
        (result) =>
          result.platform === "telegram"
      );

    // ========================================================
    // Normalize Twitter
    // ========================================================

    let normalizedTwitterData = [];

    if (twitterResult) {
      normalizedTwitterData =
        extractTwitterData(
          twitterResult.data
        );

      console.log(
        `[Twitter] Normalized ${normalizedTwitterData.length} posts`
      );
    }

    // ========================================================
    // Normalize YouTube
    // ========================================================

    let normalizedYouTubeData = [];

    if (youtubeResult) {
      const youtubeVideos =
        youtubeResult.data;

      // ------------------------------------------------------
      // Fetch details for every YouTube video concurrently
      // ------------------------------------------------------

      const detailedVideos =
        await Promise.all(
          youtubeVideos.map(
            (video) =>
              fetchYouTubeVideoDetails(
                video
              )
          )
        );

      console.log(
        `[YouTube] Fetched details for ${detailedVideos.length} videos`
      );

      normalizedYouTubeData =
        extractYouTubeData(
          detailedVideos
        );

      console.log(
        `[YouTube] Normalized ${normalizedYouTubeData.length} posts`
      );
    }

    // ========================================================
    // Normalize Telegram
    // ========================================================

    let normalizedTelegramData = [];

    if (telegramResult) {
      const telegramData =
        telegramResult.data;

      /*
       * Telegram API returns:
       *
       * {
       *   messages: [...]
       * }
       *
       * But extractTelegramData() expects:
       *
       * {
       *   posts: [...]
       * }
       *
       * So convert messages -> posts before
       * passing the data to the helper.
       */

      const telegramHelperData = {
        posts:
          telegramData?.messages || [],
      };

      normalizedTelegramData =
        extractTelegramData(
          telegramHelperData
        );

      console.log(
        `[Telegram] Normalized ${normalizedTelegramData.length} posts`
      );
    }

    // ========================================================
    // Combine ALL platforms
    // ========================================================

    const normalizedData = [
      ...normalizedTwitterData,
      ...normalizedYouTubeData,
      ...normalizedTelegramData,
    ];

    // ========================================================
    // Final response
    // ========================================================

    console.log(
      `\n[Main] Total normalized posts: ${normalizedData.length}`
    );

    console.log(
      "========================================\n"
    );

    return res
      .status(200)
      .json(normalizedData);

  } catch (error) {
    logAxiosError(error);

    return res
      .status(500)
      .json({
        error:
          "Failed to fetch social media data",

        message:
          error.message,

        details:
          axios.isAxiosError(error)
            ? error.response?.data
            : undefined,
      });
  }
}

// ============================================================
// Route
// ============================================================

app.post(
  "/details",
  getSocialMediaData
);

// ============================================================
// Start server
// ============================================================

app.listen(
  PORT,
  () => {
    console.log(
      `Backend API listening on http://localhost:${PORT}`
    );
  }
);