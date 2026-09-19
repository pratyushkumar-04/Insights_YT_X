export function extractYouTubeData(posts) {
  return posts.map((video) => {
    const rawComments =
      video.comments ||
      video.raw_data?.comments ||
      [];

    const comments = rawComments.map((comment) => ({
      author: comment.author ?? 0,

      text: comment.text ?? 0,

      like_count: comment.like_count ?? 0,

      timestamp: comment.timestamp ?? 0,

      reply_count: comment.reply_count ?? 0,
    }));

    return {
      title: video.title ?? 0,

      view_count: video.view_count ?? 0,

      like_count: video.like_count ?? 0,

      comment_count:
        video.comment_count ?? comments.length,

      upload_date: video.upload_date ?? 0,

      comments,
    };
  });
}

const video = {
  "FHAtZQA0uBo": {
    "video_id": "FHAtZQA0uBo",
    "title": "The Art Of Lying ft. Srikant Tiwari | The Family Man S3 | Manoj Bajpayee, Sharib Hashmi, Priyamani",
    "description": "Watch the web series The Family Man starring Manoj Bajpayee, Jaideep Ahlawat, Nimrat Kaur, Priyamani, Sharib Hashmi, Shreya Dhanwanthary, Harman Singha, Ashlesha Thakur, Vedant Sinha, Darshan Kumaar, Seema Biswas, Gul Panag, Vipin Sharma, Jugal Hansraj, Aditya Srivastava, Paalin Kabak, available only on Prime Video India.\n\nWatch Now - https://bit.ly/TheFamilyManS3OnPrime \n\nAbout:\nOn a personal mission to avenge an assassination, Srikant Tiwari unravels a devious conspiracy that threatens to send India to the brink of war.\n\nFollow us on:\nInstagram: https://www.instagram.com/primevideoin/\nFacebook: https://www.facebook.com/PrimeVideoIN/\nX: https://x.com/PrimeVideoIN\n\nABOUT PRIME VIDEO\nPrime Video is a one-stop entertainment destination offering customers a vast collection of premium programming in one application available across several devices. On Prime Video, customers can find their favourite Indian and international original series, movies, TV shows, and more, across multiple languages – including Indian-produced Original series like Mirzapur, Farzi, Panchayat, The Family Man, Dhootha, Jubilee, Dahaad, Made in Heaven, Suzhal – The Vortex, Inspector Rishi, Poacher, Indian Police Force, Paatal Lok, Rainbow Rishta, Wedding.con; Original movies like Maja Ma, Ammu, Mast Mein Rehne Ka; popular global Originals like Citadel, The Lord of The Rings: The Rings of Power, Fallout, Reacher, The Boys, The Wheel of Time, Road House, The Idea of You; some of the biggest post-theatrical films; direct-to-service films such as Shershaah, Soorarai Pottru, Sardar Udham, Bawaal, Gehraiyaan, Jai Bhim, Jalsa, Sherni, Narappa, Sarpatta Parambarai, Kuruthi, Joji, Malik, Pippa, HOME, Sharmajee Ki Beti, and many more of such titles. Additionally, Prime Video’s video entertainment marketplace, offers customers programming from partners such as Lionsgate Play, Discovery+ Crunchyroll, BBC Player, Sony Pictures – Stream, MGM+, FanCode, Chaupal, Manorama Max, Eros Now, Hoichoi, Anime Times, to name a few, via Prime Video add-on-subscriptions, as well as the option to rent movies, regardless of whether customers have a Prime membership or not. Customers can also go behind the scenes of their favorite movies and series with exclusive X-Ray access. Prime Video is one benefit among many that provides savings, convenience, and entertainment as part of the Prime membership. For more info visit www.amazon.com/primevideo.\n\n#thefamilyman #manojbajpayee #sharibhashmi #priyamani #thefamilymanonprime #thefamilymanseason3 #series #webseries #comedy #funny #primevideoindia",
    "view_count": 545179,
    "like_count": 4811,
    "dislike_count": 0,
    "comment_count": 94,
    "upload_date": "20251207",
    "uploader": "Prime Video India",
    "channel_id": "UC4zWG9LccdWGUlF77LZ8toA",
    "channel_url": "https://www.youtube.com/channel/UC4zWG9LccdWGUlF77LZ8toA",
    "duration": 200,
    "duration_string": "03:20",
    "tags": [
      "the family man",
      "the family man season 3",
      "the family man season 3 trailer",
      "the family man season 3 review",
      "the family man trailer",
      "the family man 3",
      "the family man season 3 scene",
      "the family man season 3 webseries",
      "the family man season 3 release date",
      "new web series",
      "hindi web series",
      "manoj bajpayee",
      "priyamani",
      "prime video",
      "prime video india",
      "amazon prime",
      "comedy scene",
      "manoj bajpayee movies",
      "manoj bajpayee web series",
      "family man",
      "family man season 3",
      "comedy",
      "funny scene"
    ],
    "categories": [
      "Entertainment"
    ],
    "thumbnail": "https://i.ytimg.com/vi/FHAtZQA0uBo/maxresdefault.jpg",
    "webpage_url": "https://www.youtube.com/watch?v=FHAtZQA0uBo",
    "subtitles_available": [
      "en"
    ],
    "automatic_captions": [
      "en",
      "ab",
      "aa",
      "af",
      "ak",
      "sq",
      "am",
      "ar",
      "hy",
      "as",
      "ay",
      "az",
      "bn",
      "ba",
      "eu",
      "be",
      "bho",
      "bs",
      "br",
      "bg",
      "my",
      "ca",
      "ceb",
      "zh-Hans",
      "zh-Hant",
      "co",
      "hr",
      "cs",
      "da",
      "dv",
      "nl",
      "dz",
      "eo",
      "et",
      "ee",
      "fo",
      "fj",
      "fil",
      "fi",
      "fr",
      "gaa",
      "gl",
      "lg",
      "ka",
      "de",
      "el",
      "gn",
      "gu",
      "ht",
      "ha",
      "haw",
      "iw",
      "hi-orig",
      "hi",
      "hmn",
      "hu",
      "is",
      "ig",
      "id",
      "iu",
      "ga",
      "it",
      "ja",
      "jv",
      "kl",
      "kn",
      "kk",
      "kha",
      "km",
      "rw",
      "ko",
      "kri",
      "ku",
      "ky",
      "lo",
      "la",
      "lv",
      "ln",
      "lt",
      "lua",
      "luo",
      "lb",
      "mk",
      "mg",
      "ms",
      "ml",
      "mt",
      "gv",
      "mi",
      "mr",
      "mn",
      "mfe",
      "ne",
      "new",
      "nso",
      "no",
      "ny",
      "oc",
      "or",
      "om",
      "os",
      "pam",
      "ps",
      "fa",
      "pl",
      "pt",
      "pt-PT",
      "pa",
      "qu",
      "ro",
      "rn",
      "ru",
      "sm",
      "sg",
      "sa",
      "gd",
      "sr",
      "crs",
      "sn",
      "sd",
      "si",
      "sk",
      "sl",
      "so",
      "st",
      "es",
      "su",
      "sw",
      "ss",
      "sv",
      "tg",
      "ta",
      "tt",
      "te",
      "th",
      "bo",
      "ti",
      "to",
      "ts",
      "tn",
      "tum",
      "tr",
      "tk",
      "uk",
      "ur",
      "ug",
      "uz",
      "ve",
      "vi",
      "war",
      "cy",
      "fy",
      "wo",
      "xh",
      "yi",
      "yo",
      "zu"
    ],
    "average_rating": null,
    "age_limit": 0,
    "is_live": false,
    "was_live": false,
    "comments": [
      {
        "author": "@stockbuffer",
        "author_id": "UC0WCH2ME3d8toyG6GnjnfAw",
        "text": "छीनाल घरवाली है श्रीकांत की 😢😢",
        "like_count": 0,
        "timestamp": 1787011200,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@tigermahesh7573",
        "author_id": "UCmBj4f-KZrFZQvkuJwaIh2Q",
        "text": "main 20 saal se bolron was epic 😂😂😂😂😂😂👌👌👌👌👌👌",
        "like_count": 0,
        "timestamp": 1787011200,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@assss4s",
        "author_id": "UCKgaLPYXf8lCVZZaswW35UA",
        "text": "The biggest problem of a man is handling 2 lives at once and the other life never understands 😢",
        "like_count": 0,
        "timestamp": 1787011200,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Naughty-jq2gg",
        "author_id": "UCiA4CPHWelng-Nk1C05ru4g",
        "text": "Thank you ❤🙏",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@bikramjeetsingh185",
        "author_id": "UCOqhaDUC8l83sFM9WiIuufw",
        "text": "Mai 20 saal se bol raha hu😂😂😂",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@shaikhsalman9464",
        "author_id": "UCgwBufvP-W3UqjEHh9pTVLg",
        "text": "jhoot bolnay mai apun ka 20 saal ka tajurba hai - belongs to Srikant Tiwari",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@ashutosh_shrivastav",
        "author_id": "UCam28Rp3_6Bt_DcjMwKtmFQ",
        "text": "Bht der lga di 2nd se 3rd season p aane mai",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@iftikharhussain8004",
        "author_id": "UClIZdmQLWWA2RYG-XGovaww",
        "text": "And rhen she kills it 😅",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@priconnects",
        "author_id": "UClFxzJqmMLnWYIEyt8WqDvA",
        "text": "This is the actual love life looks after marriage 💕 no official I love you, I miss you.. it is all implied in the tone and silences.",
        "like_count": 1,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@truthseeker127khan8",
        "author_id": "UCIKbhul05kWI9imHrc_orwA",
        "text": "Life of a true  man 😢",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@vaibhavpatil8696",
        "author_id": "UCcqIqevvNfTcgDUf2MeL6Kw",
        "text": "3:00 mai bees saal se bol raha hu😂😂 \nthe pain in his eyes😅",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@manas-y9l",
        "author_id": "UCZvVcM7QlNPe7qQO2MKQcNg",
        "text": "Season 3 of family man was trash",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@AfridiAnsari-dg6ok",
        "author_id": "UCDGKF5bNB18nSM2QyAkER8g",
        "text": "mein 20 saal se bol raha hun 😂",
        "like_count": 0,
        "timestamp": 1781740800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Shuvam_11",
        "author_id": "UCaXE2OsWgkO0c_KDlEGgMcA",
        "text": "Multiple father syndrome 😂😂😂😂",
        "like_count": 0,
        "timestamp": 1773792000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@ChinmayiHegde-n4f",
        "author_id": "UCgeXhjo0Ngv7ugJ5MXbJ3oA",
        "text": "Episode no?",
        "like_count": 0,
        "timestamp": 1771372800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Raisali1994",
        "author_id": "UCu6FuzQDqDEuGc6e7CzY1tQ",
        "text": "He is in Dimapur",
        "like_count": 0,
        "timestamp": 1771372800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@narendergade5343",
        "author_id": "UCYv2I_ytgj9EWVA0lqNS1nw",
        "text": "Great action of Manoj and Priya",
        "like_count": 5,
        "timestamp": 1768694400,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@AmanGaming-ms5hr",
        "author_id": "UCXdGiGSXuenj37vZUcXKJ_w",
        "text": "She cheated on him and keeps playing victim card all over the seasons !",
        "like_count": 0,
        "timestamp": 1768694400,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Shuvam_11",
        "author_id": "UCaXE2OsWgkO0c_KDlEGgMcA",
        "text": "Be a family man and a spy not easy",
        "like_count": 5,
        "timestamp": 1768694400,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@RitikSingh.youtube",
        "author_id": "UCjUABRjFQepkqLDUK5tdg7Q",
        "text": "jk vibhisan 😅",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@dholbegins",
        "author_id": "UCNVhIqDAKRALKtav1BiA82g",
        "text": "ऐसे झूठ बोलने का मेरा 20 साल का तजुर्बा है।😂",
        "like_count": 7,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Asima331",
        "author_id": "UCL1qQsz4owHKwRBJt6O-DoA",
        "text": "Both just want love hugs and miss u ..but they just can't say it...They both are guilty about their mistakes and Suchi really loves shree but for that mistake she just can't face shree just vending her frustrations",
        "like_count": 29,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@aaodekheincinema",
        "author_id": "UCEWxNlxj34Jn2fC0Z9KXZuQ",
        "text": "Suchi cheated him physically with someone else, there is no apology for cheating😢",
        "like_count": 3,
        "timestamp": 1781740800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@kk6106",
        "author_id": "UCwefn5knAebOkKhbQgN_SUQ",
        "text": "She cheated with a colleague and now it's shown that she cares for him , what poop is this",
        "like_count": 1,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Adicharya18",
        "author_id": "UCfJbIdyGFvEAKEvUQFkX-yA",
        "text": "This also happen in real life when later realised either how sinful it is so forgiving is best as she has guilt which should be😢 praised and dharma",
        "like_count": 0,
        "timestamp": 1768694400,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@PankajKaushik",
        "author_id": "UCeWA-r9qdFCppAi8f8bgFng",
        "text": "Dushman mile hazar pr Bivi ma mile chhinar. 🫥",
        "like_count": 4,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@ashishnix45",
        "author_id": "UCo1Lhy4TSPsmUmaGJFk5N_A",
        "text": "😂",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@AdarshTripathi-hv4lz",
        "author_id": "UCUDg0iM_lKrKNNAjWp7uYqQ",
        "text": "Mai 20 saal se bol rha hu...😅😅😅😅👌👌👌👌",
        "like_count": 4,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@arvindbalavinayagam4510",
        "author_id": "UC9s7LrhO4MH0ssyXbzcMoQQ",
        "text": "This scene shows how well they understand each other and knows every action before they make",
        "like_count": 22,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Pavan.konapala",
        "author_id": "UCBWmeFk92qMzkkzDcgYMr2w",
        "text": "ye konse epesode ka hai",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@stillsprouting5633",
        "author_id": "UCb82Pp0d6vRXt6h46-oDXlQ",
        "text": "Sach bolun to yeh season acha nhi lga😢",
        "like_count": 1,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@rupalipandey3336",
        "author_id": "UCj-kjCgeak_NsRIg3gwrkvA",
        "text": "\"Mai 20 Saal se bol raha hu\" but suchi ko toh Pata hi hota Hai jhuth ka 😂",
        "like_count": 1,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Siddharth-l9r9r",
        "author_id": "UCmCvWOblL_mI6qf4QndgWNw",
        "text": "Sab pata tha to kyu chilla rahi thi BKL😅",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@IshanBajpayee-j7u",
        "author_id": "UCvk1FLnzOAip1lJ3eXno1eA",
        "text": "yaar iska ek aur episode hoga vo bhi daal do 🥲🥲",
        "like_count": 7,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@ImranHussain-yf8un",
        "author_id": "UCaKwu4z9sv18AHocHk6Es5A",
        "text": "Aisa series banao mat,, totally wasted in the name of Family Man. S3 was the worst i would say",
        "like_count": 4,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@RAILWAYreal",
        "author_id": "UCgGyioj2RsB_O4CgYkjs0_g",
        "text": "Tujhe jake cartoon dekhna chahiye",
        "like_count": 4,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@ImranHussain-yf8un",
        "author_id": "UCaKwu4z9sv18AHocHk6Es5A",
        "text": " @RAILWAYreal  Seriously tum big boss walo  kuch bhi kachra dekhar kar acha comments karne lag jate ho. NA kuch naya wahi ghisa pita stoyline bht pasand atey hain tumhe.",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@RAILWAYreal",
        "author_id": "UCgGyioj2RsB_O4CgYkjs0_g",
        "text": "​ @ImranHussain-yf8un Abe to dekha kyu chhor de",
        "like_count": 1,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Nimesh.",
        "author_id": "UCRQz7CJ4wHkszg4zv7PATBQ",
        "text": "​ @ImranHussain-yf8un sidha bol n tum logo k kuch agenda exposed ho rahe h to Mirchi lag rahi.. varna agar pasand nhi to skip kro.. Rona kyu ro rahe",
        "like_count": 2,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@ImranHussain-yf8un",
        "author_id": "UCaKwu4z9sv18AHocHk6Es5A",
        "text": " @RAILWAYreal  Areh bhai ajeeb prani ho, dekhar kar agar kuch acha nahi lagey to bolu bhi naa??  S1 aur S2 dekhar acha laga isliye to S3 dekha usme prev Seasons ke comapre mein acha nahi isilye bola. Gajab chutiya ho bhai.",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@ImranHussain-yf8un",
        "author_id": "UCaKwu4z9sv18AHocHk6Es5A",
        "text": " @Nimesh.  Isiliye Ajit Doval ne khud bola ki Hindu larko se jyada Muslim ladke desh ko bachane mein jyada lage huwe hain. Aur BC tumi bhi Gobar kahte ho kya?? Series shuru honese pehle ye bol diya jata hai ki ye dharawahik karyakram hai. REal lie se kuch bhi lena dena nahi hai.",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@sgt_chyang2487",
        "author_id": "UCEEnMnklyAe8GAKDZYHL5-A",
        "text": "Tu negative hi soch bencho",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@akashsinku9983",
        "author_id": "UC36y1LBmYW6997S3WA5yi8w",
        "text": "It was hilarious and emotional 😂😢❤❤....",
        "like_count": 6,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Hind72Tours",
        "author_id": "UCEC-DYa6Fs8sxKQh9W_pN1A",
        "text": "Thumbnail me Om Puri sa lga M B",
        "like_count": 1,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@DeepikaAswani-t6w",
        "author_id": "UCI9u2IsmdSrSsin4CnEsFUQ",
        "text": "Line mein kutti khadi hogi suchi ke baad isliye",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@supratimroy2977",
        "author_id": "UC58wTPZlG1j-x0i38OAsVDw",
        "text": "😂😂😂😂😂😂😂😂😂",
        "like_count": 1,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@mahalaya13",
        "author_id": "UC7i67SA1HYjY4bNvHTy22Mg",
        "text": "20th comment form me..",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@AkshayNagar-t6p",
        "author_id": "UC8FSfco5ELVBUboaCPGhsag",
        "text": "The caption doesn't match the video.",
        "like_count": 90,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Divyaaaaansh",
        "author_id": "UCUQbDzYLySYgg90zpfe0qFw",
        "text": "Captions(closed captioning) and subtitles are often different and intended for different purposes. Find out yourself",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@KurkureCreations",
        "author_id": "UCTfvyyNcWNJa9TojuCT3I3w",
        "text": "@Divyaaaaansh video title it is",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@ReviewsYoutubeChannel-x6q",
        "author_id": "UCNFJk4USpLnqiDKnRyhGJEQ",
        "text": "He's been an amazing father! 😄❤",
        "like_count": 14,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@satishkamtikar958",
        "author_id": "UC5PUVj7st5z4XFiaaFbbliw",
        "text": "Srikant had a choice of continuing to work in the soft ware company. He manhandled the boss and left the job.",
        "like_count": 16,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@arun5875",
        "author_id": "UC_RRH4Vzs5BDJWCf7aIJE3Q",
        "text": "He did something what most employees wishes to do to their bosses.",
        "like_count": 2,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@satishkamtikar958",
        "author_id": "UC5PUVj7st5z4XFiaaFbbliw",
        "text": "​ @arun5875 Will Srikant do the same to his bosses in TASK. No. Because the IT cell boss was a weak person with no support. But Srikant would not dare do such a thing to his bosses in TASK as they will then return the favour. These govt employees especially those in org dealing with security have the arrogance that they are above the law. Like they are saving the country and have a superiority feeling especially while dealing with civilians.",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@shivashankar5344",
        "author_id": "UCtmh6r7jJQA7gARnFhRM3lg",
        "text": "​ @satishkamtikar958 not exactly.  Srikanth was passionate about Nation's security.",
        "like_count": 2,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Zekr0_",
        "author_id": "UCKWFug_yvNTXivazhgSGq8g",
        "text": "​ @satishkamtikar958  stop larping . You are literally projecting rn",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@ramn4041",
        "author_id": "UCpXFBGj7bZBw3aBeLKH0dhA",
        "text": "​ @satishkamtikar958 It's simple. He likes TASK job..it gives him the kick. It's the kind of job that he thinks is worth taking a bullet for.",
        "like_count": 1,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@venkyprakashmcc",
        "author_id": "UCuXTnP5LZHvnTPULNEVvlXg",
        "text": "He didn't manhandle his boss..he handled him like a man !",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@ramn4041",
        "author_id": "UCpXFBGj7bZBw3aBeLKH0dhA",
        "text": "It's simple. He likes TASK job..it gives him the kick. It's the kind of job that he thinks is worth taking a bullet for.",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@satishkamtikar958",
        "author_id": "UC5PUVj7st5z4XFiaaFbbliw",
        "text": "What a great house. Lovely balcony",
        "like_count": 21,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@lavatr8321",
        "author_id": "UCKQdDASvGZdd8wCDPfXEfDQ",
        "text": "The dialogues were Rushing with scenes.... Entire season.\n\nJust to conclude towards \"Mei 20 Saal se bol raha hoon\"\n\nThey added \"Chaila Suchi ko jhoot bolna difficult hai\"\nSo JK character was Just There for Srikant to talk in Punch lines...\nIt was very  Artificial.\n\nI don't even know what the Season was about, what the sequence was... Very Scattered.",
        "like_count": 5,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@tomcruise4745",
        "author_id": "UC8Yp7d9u_HRpZB-MEFD90uQ",
        "text": "Everything would have made sense if there was a proper ending but for now it's all scattered till next season",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@lavatr8321",
        "author_id": "UCKQdDASvGZdd8wCDPfXEfDQ",
        "text": "​@tomcruise4745 To even reach that hanging Ending... What kind of build up was that 😂\nRukma is nothing whatever they portrayed in 1st episode. English Boss lady is is just chuffing here and there.\n\nWhat's going on.",
        "like_count": 3,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@DivyanshuSoni7",
        "author_id": "UCKTA3AkpxErXuypleoK3Dbw",
        "text": "Each and every dialogue feels so Real \nThis where you see peak acting ❤❤\nHats off to Manoj Bajpayee's skills 🙌",
        "like_count": 2,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@lavatr8321",
        "author_id": "UCKQdDASvGZdd8wCDPfXEfDQ",
        "text": "Exam ki Padhai karle",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@siddharthapaul1",
        "author_id": "UCIC3gwNba8-pp-wnsvT2RNA",
        "text": "2:56 Isiliye Shrikant Tiwari Is An Experienced Man Jhooth Blne Mein 20 Years! 🗿👏😂 JK Being JK Things! 🙊😅",
        "like_count": 76,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@abhijeetm29",
        "author_id": "UCsaTuwZWo4PzfE8RMYDwbcg",
        "text": "Please release season 4 now.",
        "like_count": 16,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@AkshayChavan-pb2ss",
        "author_id": "UCwIdLE81E8XZ3nv2lO1257Q",
        "text": "You have to wait till 1-2 years",
        "like_count": 0,
        "timestamp": 1768694400,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@TerraceCricketers",
        "author_id": "UC9aq2H23ifwtwC8hU_5Hslw",
        "text": "This scene shows that yet their marriage is not doing well but still they care for each other 🫠",
        "like_count": 242,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@PrimeVideoIN",
        "author_id": "UC4zWG9LccdWGUlF77LZ8toA",
        "text": "he's a family man for a reason 🥹",
        "like_count": 39,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Nimesh.",
        "author_id": "UCRQz7CJ4wHkszg4zv7PATBQ",
        "text": "Wife caring for her security, husband care for family😂",
        "like_count": 23,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@FunViralhappinesslovesnaps",
        "author_id": "UCcOzb6JYK9ySwmL0LgHkUDQ",
        "text": "​ @Nimesh. That's ryt . Sometimes I think how can a person stay with another just for his own selfish reason. DON'T use another person.",
        "like_count": 2,
        "timestamp": 1771372800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Adicharya18",
        "author_id": "UCfJbIdyGFvEAKEvUQFkX-yA",
        "text": "​ @Nimesh. Victim card mt khel wife independent alimony bhi mang skti but still se not choose male ego thoda side me",
        "like_count": 0,
        "timestamp": 1768694400,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Sthithpragnya",
        "author_id": "UCxRjJMEwtFJYHs_s0lRqQnQ",
        "text": "​ @Nimesh. She knows that he is absent for a reason, he isn't cheating.\nShe hated his lies!!!!!\n\nMind it it's a Hindi Tamil inter cultural marriage between them,",
        "like_count": 0,
        "timestamp": 1781740800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@RUPESH_G01",
        "author_id": "UCVVl-tvWOXmrgK6ppm6JAng",
        "text": "Wife is a cheater",
        "like_count": 3,
        "timestamp": 1781740800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@GeoMatrixx",
        "author_id": "UCiQBpOqqvyd1eZrooy_uJ0A",
        "text": "​ @RUPESH_G01  she never cheated btw",
        "like_count": 0,
        "timestamp": 1781740800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@DocAB2022",
        "author_id": "UCj8nI2k4fTvdStf2R-t6itQ",
        "text": "​ @GeoMatrixx S1\nWith her colleague",
        "like_count": 1,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@GeoMatrixx",
        "author_id": "UCiQBpOqqvyd1eZrooy_uJ0A",
        "text": "​@DocAB2022 when ?",
        "like_count": 0,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@DocAB2022",
        "author_id": "UCj8nI2k4fTvdStf2R-t6itQ",
        "text": "​ @GeoMatrixx there was a scene when they went on a trip, she was in the room, the colleague on the sofa, she opened the door slightly after chatting... \nI can't remember the episode no. exactly",
        "like_count": 1,
        "timestamp": 1784332800,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Joshya-t8w",
        "author_id": "UCK81rbJvlq7auBeISynwosg",
        "text": "0:51 isliye security clearance se bahar jata hai JK 😂😂",
        "like_count": 120,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@PrimeVideoIN",
        "author_id": "UC4zWG9LccdWGUlF77LZ8toA",
        "text": "poor JK 😂",
        "like_count": 9,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@AnkitYadav-ei1mt",
        "author_id": "UCOc5rllrarYNUrVDVwGXULQ",
        "text": "Phone paani me gir gaya tha is PERMANENT 😂😂😂",
        "like_count": 301,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@PrimeVideoIN",
        "author_id": "UC4zWG9LccdWGUlF77LZ8toA",
        "text": "this is too real 😂",
        "like_count": 11,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@041sharadsingh8",
        "author_id": "UCDGTgJOK-Uoc_Bfh_1BkRCg",
        "text": "Right 😂",
        "like_count": 0,
        "timestamp": 1787011200,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@washyourhands2879",
        "author_id": "UC_t_x18icQu7bAjD7QXU7mA",
        "text": "Hum 3rd",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@hasanibnamonowara2994",
        "author_id": "UCZOiBWcn27xL0TftecEgDCQ",
        "text": "Dear Prime Video\nWe The Audiences Desperately Want\nAn Hindi Remake Of\nCulpa Mia ( My Fault Franchise) \nWith Only & Only Emraan Hashmi In The Lead\n&\nFor The Female Lead\nKindly Cast Anyone Among These Ones\nIleana D.Cruz / Disha Patani / Tripti Dimri",
        "like_count": 9,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@athithim023",
        "author_id": "UCzdUsQT9No6SffPqweahcVg",
        "text": "No...",
        "like_count": 2,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@hasanibnamonowara2994",
        "author_id": "UCZOiBWcn27xL0TftecEgDCQ",
        "text": "​ @athithim023 \nAbbey Hata Sawan Ki Ghata\nKha Khuja\nBatti Bujha Ke Soja Chal",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@ShowingUpEverySingleday",
        "author_id": "UChjvbqt5-vkHveXfD3EShog",
        "text": " @hasanibnamonowara2994  who the hell would remake a Spanish film \n\nAnd ur cast is very ba",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@lavatr8321",
        "author_id": "UCKQdDASvGZdd8wCDPfXEfDQ",
        "text": "Chiii🤮",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@basyunhichaltechalte7195",
        "author_id": "UCnbF40mvjcWBQnvZGUOxKBw",
        "text": "Pagal ho kya bhai",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@not_ultimate",
        "author_id": "UCCw9FUR6dYkyTJ-zRQlPMMw",
        "text": "Yr ye maine Filmyzilla se download krke dekha I want to complain that The last episode is not in that. Pls help those.",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@Agentalpha-s1x",
        "author_id": "UCVAxCQdE0hAS08lBx9z3VNw",
        "text": "Ham second",
        "like_count": 0,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      },
      {
        "author": "@bhaumikdhanakagemerz2778",
        "author_id": "UCHuXDX0PpF8OQBZYN9u8NFQ",
        "text": "First comment please pin who who like The family man s3",
        "like_count": 1,
        "timestamp": 1766016000,
        "time_text": "N/A",
        "is_pinned": false,
        "is_hearted": false,
        "reply_count": 0
      }
    ]
  }
}

//console.log(extractYtData(Object.values(video)[0]));

export function extractTelegramData(data) {
  return data.posts.map((post) => {
    const uploadDate = new Date(post.date);

    const comments = (post.comments || []).map((comment) => ({
      author: comment.author?.username
        ? `@${comment.author.username}`
        : 0,

      text: comment.text ?? 0,

      like_count: 0,

      timestamp: Math.floor(
        new Date(comment.date).getTime() / 1000
      ),

      reply_count: 0,
    }));

    return {
      title: post.text ?? 0,

      view_count: post.raw_data.views ?? 0,

      // 1 forward = 8 likes
      like_count: (post.raw_data.forwards ?? 0) * 8,

      comment_count: comments.length,

      upload_date:
        uploadDate.getUTCFullYear().toString() +
        String(uploadDate.getUTCMonth() + 1).padStart(2, "0") +
        String(uploadDate.getUTCDate()).padStart(2, "0"),

      comments,
    };
  });
}

const video2 = {
  "posts": [
    {
      "id": 5446,
      "date": "2026-09-18T11:51:31+00:00",
      "text": "🚀 **Standby Clock is NOW AVAILABLE** ✨\n\nMeet Standby Clock (FREE) — turn your Android phone into a beautiful desk clock, bedside clock & smart display while it charges. 📱⏰\n\n👉 Download Now, It's FREE\nhttps://play.google.com/store/apps/details?id=com.standby.clock.dock\n\n✨ Beautiful clock faces\n🌙 Minimal standby experience\n🔋 Perfect for your desk or bedside\n🎨 Designed to make your phone useful even while charging\n\n🎁 10 Pro Version Giveaway\n[Giveaway Link](https://x.com/justnewdesigns/status/2100915407209341432)\n\nYour phone with A whole new purpose. 🚀\n\n#StandbyClock #JustNewDesigns #AndroidApps #Android #DeskClock #WallpaperApps",
      "views": 1316,
      "forwards": 0,
      "comments": [
        {
          "id": 26920,
          "date": "2026-09-18T12:30:04+00:00",
          "author": {
            "username": "ravidevn7355",
            "first_name": "Ravi",
            "last_name": "Yadav"
          },
          "text": "Link"
        },
        {
          "id": 26919,
          "date": "2026-09-18T11:52:22+00:00",
          "author": {
            "username": "LANDING_CIGARETTE",
            "first_name": "Janet",
            "last_name": null
          },
          "text": "Cute, you actually need an app."
        }
      ],
      "popularity_score": 1366.0
    },
    {
      "id": 5444,
      "date": "2026-09-17T07:05:58+00:00",
      "text": "",
      "views": 5622,
      "forwards": 11,
      "comments": [],
      "popularity_score": 5787.0
    },
    {
      "id": 5443,
      "date": "2026-09-17T07:05:58+00:00",
      "text": "",
      "views": 5608,
      "forwards": 15,
      "comments": [],
      "popularity_score": 5833.0
    },
    {
      "id": 5442,
      "date": "2026-09-17T07:05:58+00:00",
      "text": "",
      "views": 5595,
      "forwards": 13,
      "comments": [],
      "popularity_score": 5790.0
    },
    {
      "id": 5441,
      "date": "2026-09-17T07:05:58+00:00",
      "text": "",
      "views": 5600,
      "forwards": 13,
      "comments": [],
      "popularity_score": 5795.0
    },
    {
      "id": 5440,
      "date": "2026-09-17T07:05:58+00:00",
      "text": "",
      "views": 5669,
      "forwards": 18,
      "comments": [],
      "popularity_score": 5939.0
    },
    {
      "id": 5439,
      "date": "2026-09-17T06:51:58+00:00",
      "text": "",
      "views": 5686,
      "forwards": 1,
      "comments": [],
      "popularity_score": 5701.0
    },
    {
      "id": 5438,
      "date": "2026-09-17T06:51:58+00:00",
      "text": "",
      "views": 5690,
      "forwards": 1,
      "comments": [],
      "popularity_score": 5705.0
    },
    {
      "id": 5437,
      "date": "2026-09-17T06:51:58+00:00",
      "text": "",
      "views": 5689,
      "forwards": 1,
      "comments": [],
      "popularity_score": 5704.0
    },
    {
      "id": 5436,
      "date": "2026-09-17T06:51:58+00:00",
      "text": "",
      "views": 5619,
      "forwards": 1,
      "comments": [],
      "popularity_score": 5634.0
    },
    {
      "id": 5435,
      "date": "2026-09-17T06:51:58+00:00",
      "text": "",
      "views": 5673,
      "forwards": 1,
      "comments": [],
      "popularity_score": 5688.0
    },
    {
      "id": 5434,
      "date": "2026-09-15T06:51:58+00:00",
      "text": "",
      "views": 8945,
      "forwards": 27,
      "comments": [],
      "popularity_score": 9350.0
    },
    {
      "id": 5433,
      "date": "2026-09-15T06:51:58+00:00",
      "text": "",
      "views": 8868,
      "forwards": 26,
      "comments": [],
      "popularity_score": 9258.0
    },
    {
      "id": 5432,
      "date": "2026-09-15T06:51:58+00:00",
      "text": "",
      "views": 8791,
      "forwards": 23,
      "comments": [],
      "popularity_score": 9136.0
    },
    {
      "id": 5431,
      "date": "2026-09-15T06:51:58+00:00",
      "text": "",
      "views": 8532,
      "forwards": 30,
      "comments": [],
      "popularity_score": 8982.0
    },
    {
      "id": 5430,
      "date": "2026-09-15T06:51:58+00:00",
      "text": "",
      "views": 8534,
      "forwards": 25,
      "comments": [],
      "popularity_score": 8909.0
    },
    {
      "id": 5429,
      "date": "2026-09-15T06:49:58+00:00",
      "text": "",
      "views": 8317,
      "forwards": 8,
      "comments": [],
      "popularity_score": 8437.0
    },
    {
      "id": 5428,
      "date": "2026-09-15T06:49:58+00:00",
      "text": "",
      "views": 8330,
      "forwards": 8,
      "comments": [],
      "popularity_score": 8450.0
    },
    {
      "id": 5427,
      "date": "2026-09-15T06:49:58+00:00",
      "text": "",
      "views": 8264,
      "forwards": 8,
      "comments": [],
      "popularity_score": 8384.0
    },
    {
      "id": 5426,
      "date": "2026-09-15T06:49:58+00:00",
      "text": "",
      "views": 8011,
      "forwards": 9,
      "comments": [],
      "popularity_score": 8146.0
    }
  ],
  "popular_posts": [
    {
      "id": 5434,
      "date": "2026-09-15T06:51:58+00:00",
      "text": "",
      "views": 8945,
      "forwards": 27,
      "comments": [],
      "popularity_score": 9350.0
    },
    {
      "id": 5433,
      "date": "2026-09-15T06:51:58+00:00",
      "text": "",
      "views": 8868,
      "forwards": 26,
      "comments": [],
      "popularity_score": 9258.0
    },
    {
      "id": 5432,
      "date": "2026-09-15T06:51:58+00:00",
      "text": "",
      "views": 8791,
      "forwards": 23,
      "comments": [],
      "popularity_score": 9136.0
    },
    {
      "id": 5431,
      "date": "2026-09-15T06:51:58+00:00",
      "text": "",
      "views": 8532,
      "forwards": 30,
      "comments": [],
      "popularity_score": 8982.0
    },
    {
      "id": 5430,
      "date": "2026-09-15T06:51:58+00:00",
      "text": "",
      "views": 8534,
      "forwards": 25,
      "comments": [],
      "popularity_score": 8909.0
    }
  ]
}

//console.log(extractTelegramData(video2))

export function extractTwitterData(posts) {
  return posts.map((post) => {
    const comments = (post.comments || []).map((comment) => ({
      author: comment.author_username
        ? `@${comment.author_username}`
        : 0,

      text: comment.text ?? 0,

      like_count: comment.likes ?? 0,

      timestamp: comment.timestamp
        ? Math.floor(new Date(comment.timestamp).getTime() / 1000)
        : 0,

      reply_count: comment.replies ?? 0,
    }));

    const date = post.created_at
      ? new Date(post.created_at)
      : null;

    const uploadDate = date
      ? date.getUTCFullYear().toString() +
        String(date.getUTCMonth() + 1).padStart(2, "0") +
        String(date.getUTCDate()).padStart(2, "0")
      : 0;

    return {
      title: post.text ?? 0,

      view_count: post.views ?? 0,

      // 1 retweet = 10 likes
      like_count: (post.retweets ?? 0) * 10,

      comment_count: post.replies ?? 0,

      upload_date: uploadDate,

      comments,
    };
  });
}

const video3 = {
  "id": "2100962703796039707",
  "text": "Key takeaways from the AGM 📝\n\n🎥 BCCI Honorary Secretary Mr. Devajit Saikia (@lonsaikia) sheds light on the major discussions held during the 95th Annual General Meeting 🙌 https://t.co/Xki706IrEh",
  "author": "BCCI",
  "author_id": null,
  "created_at": "Fri Sep 18 14:58:37 +0000 2026",
  "likes": 1256,
  "retweets": 28,
  "replies": 25,
  "comments": [
    {
      "tweet_id": "2101129990830198909",
      "text": "@BCCI @lonsaikia The commercial scale of the BCCI now rivals major global leagues, but managing that growth while balancing domestic structure remains a massive test. What's your take? 🏏",
      "author_username": "TheWorldEye_",
      "author_display_name": "The World Eye",
      "timestamp": "Sat Sep 19 02:03:21 +0000 2026",
      "likes": 0,
      "retweets": 0,
      "replies": 0,
      "views": 0,
      "hashtags": [],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/TheWorldEye_/status/2101129990830198909",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100964755771211849",
      "text": "@BCCI @lonsaikia Any dicussion on women team captaincy change?",
      "author_username": "kundudilip",
      "author_display_name": "ourINDIAourPRIDE🏹",
      "timestamp": "Fri Sep 18 15:06:46 +0000 2026",
      "likes": 2,
      "retweets": 0,
      "replies": 0,
      "views": 0,
      "hashtags": [],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/kundudilip/status/2100964755771211849",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100969770535604426",
      "text": "@BCCI @lonsaikia Regulate Skill-Based fantasy sports [RMG]\n#RegulateSkillGames \n#RMG",
      "author_username": "darkhorse3456",
      "author_display_name": "DarkHorse",
      "timestamp": "Fri Sep 18 15:26:42 +0000 2026",
      "likes": 3,
      "retweets": 2,
      "replies": 0,
      "views": 0,
      "hashtags": [
        "RegulateSkillGames",
        "RMG"
      ],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/darkhorse3456/status/2100969770535604426",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100980814863622191",
      "text": "@BCCI @lonsaikia “Eexar paatil vice captain”\nFamous line",
      "author_username": "MukeshGarg0771",
      "author_display_name": "Police911💀",
      "timestamp": "Fri Sep 18 16:10:35 +0000 2026",
      "likes": 0,
      "retweets": 0,
      "replies": 0,
      "views": 0,
      "hashtags": [],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/MukeshGarg0771/status/2100980814863622191",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100963168122179600",
      "text": "@BCCI @lonsaikia Great",
      "author_username": "nikitashivam88",
      "author_display_name": "Nikita राजस्थानी 💕",
      "timestamp": "Fri Sep 18 15:00:27 +0000 2026",
      "likes": 0,
      "retweets": 0,
      "replies": 0,
      "views": 0,
      "hashtags": [],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/nikitashivam88/status/2100963168122179600",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100990307072344535",
      "text": "@BCCI @lonsaikia Bro had the whole room nodding until the mic cut out. What was the real debate behind closed doors?",
      "author_username": "petrov74940",
      "author_display_name": "John Petrov",
      "timestamp": "Fri Sep 18 16:48:18 +0000 2026",
      "likes": 0,
      "retweets": 0,
      "replies": 0,
      "views": 0,
      "hashtags": [],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/petrov74940/status/2100990307072344535",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100965795065135537",
      "text": "@BCCI @lonsaikia \" We Want Back a Real Money Skill Gaming Industry in India #Dream11 🏟️🏌🏼\"",
      "author_username": "Manishchouhan__",
      "author_display_name": "The Third Eye View",
      "timestamp": "Fri Sep 18 15:10:54 +0000 2026",
      "likes": 2,
      "retweets": 0,
      "replies": 0,
      "views": 0,
      "hashtags": [
        "Dream11"
      ],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/Manishchouhan__/status/2100965795065135537",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100963624156114956",
      "text": "@BCCI @lonsaikia India's next-gen is cooking — the Team India buzz is real 🔥",
      "author_username": "rishabhxAi",
      "author_display_name": "rishabh",
      "timestamp": "Fri Sep 18 15:02:16 +0000 2026",
      "likes": 0,
      "retweets": 0,
      "replies": 0,
      "views": 0,
      "hashtags": [],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/rishabhxAi/status/2100963624156114956",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100974186865078471",
      "text": "@BCCI @lonsaikia Fantasy waps lao",
      "author_username": "Thenewsdropp",
      "author_display_name": "The News Drop",
      "timestamp": "Fri Sep 18 15:44:15 +0000 2026",
      "likes": 2,
      "retweets": 0,
      "replies": 0,
      "views": 0,
      "hashtags": [],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/Thenewsdropp/status/2100974186865078471",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100965296907395080",
      "text": "@BCCI @lonsaikia The next generation is looking seriously good for India 🙌",
      "author_username": "rishabhxAi",
      "author_display_name": "rishabh",
      "timestamp": "Fri Sep 18 15:08:55 +0000 2026",
      "likes": 0,
      "retweets": 0,
      "replies": 0,
      "views": 0,
      "hashtags": [],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/rishabhxAi/status/2100965296907395080",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100966395685335433",
      "text": "@BCCI @lonsaikia \" We Want Back a Real Money Skill Gaming Industry in India #Dream11 🏌🏼🏟️ @lonsaikia  \"",
      "author_username": "Manishchouhan__",
      "author_display_name": "The Third Eye View",
      "timestamp": "Fri Sep 18 15:13:17 +0000 2026",
      "likes": 3,
      "retweets": 2,
      "replies": 0,
      "views": 0,
      "hashtags": [
        "Dream11"
      ],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/Manishchouhan__/status/2100966395685335433",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100966360427933867",
      "text": "@BCCI @lonsaikia \" We Want Back a Real Money Skill Gaming Industry in India #Dream11 🏌🏼🏟️ @lonsaikia",
      "author_username": "Manishchouhan__",
      "author_display_name": "The Third Eye View",
      "timestamp": "Fri Sep 18 15:13:09 +0000 2026",
      "likes": 2,
      "retweets": 0,
      "replies": 0,
      "views": 0,
      "hashtags": [
        "Dream11"
      ],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/Manishchouhan__/status/2100966360427933867",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100971302702227538",
      "text": "🔥 BCCI 95th AGM just dropped the roadmap. Not minutes. Momentum.\n\nFrom Hon. Sec. Devajit Saikia after the Mumbai meeting:\n\n🏏 IPL 2027 = 20th edition. Board wants it celebrated GRAND.\n🇮🇳 BCCI CENTENARY 2028 — year-long programme from Dec 2027 through 2028.\n⚖️ Umpires & match referees get enhanced pay + grade reclassification.\n📋 Arun Singh Dhumal & M Khairul Jamal Majumdar inducted into IPL Governing Council.\n🧾 FY 2025-26 accounts passed. FY 2026-27 budget approved. Auditors appointed.\n🛡️ New Internal Committee under POSH policy.\n🪪 Age Verification Policy updated.\n♿ State units asked to back differently-abled cricketers with real facilities.\n\nThis is BCCI planning the next 24 months like a festival, not a file.\n\nWhich call hits hardest — IPL 20, BCCI 100, or the umpire pay hike?\n\n@BCCI @lonsaikia\n#BCCIAGM #IPL2027 #IndianCricket",
      "author_username": "AasheeshTiwarii",
      "author_display_name": "Aasheesh Tiwarii",
      "timestamp": "Fri Sep 18 15:32:47 +0000 2026",
      "likes": 0,
      "retweets": 0,
      "replies": 0,
      "views": 0,
      "hashtags": [
        "BCCIAGM",
        "IPL2027",
        "IndianCricket"
      ],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": "Key takeaways from the AGM 📝\n\n🎥 BCCI Honorary Secretary Mr. Devajit Saikia (@lonsaikia) sheds light on the major discussions held during the 95th Annual General Meeting 🙌 https://t.co/Xki706IrEh",
      "in_reply_to_id": null,
      "url": "https://x.com/AasheeshTiwarii/status/2100971302702227538",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2101030462294831427",
      "text": "@BCCI @lonsaikia Mohsin Naqvi ne  Asia cup ke mens and womens ke dono Trophies 🏆 dediye?",
      "author_username": "KSandee94241601",
      "author_display_name": "K Sandeep",
      "timestamp": "Fri Sep 18 19:27:52 +0000 2026",
      "likes": 0,
      "retweets": 0,
      "replies": 0,
      "views": 0,
      "hashtags": [],
      "mentions": [
        "BCCI",
        "lonsaikia"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/KSandee94241601/status/2101030462294831427",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    },
    {
      "tweet_id": "2100985314731049041",
      "text": "@BCCI @lonsaikia @GautamGambhir should be next. He has not achieved anything as coach. He should be hold accountable for our poor performance",
      "author_username": "luckyn",
      "author_display_name": "Rohit Sharma Fan",
      "timestamp": "Fri Sep 18 16:28:28 +0000 2026",
      "likes": 1,
      "retweets": 1,
      "replies": 0,
      "views": 0,
      "hashtags": [],
      "mentions": [
        "BCCI",
        "lonsaikia",
        "GautamGambhir"
      ],
      "image_urls": [],
      "video_urls": [],
      "source": null,
      "is_retweet": false,
      "quote_tweet": null,
      "in_reply_to_id": null,
      "url": "https://x.com/luckyn/status/2100985314731049041",
      "parent_tweet_id": "2100962703796039707",
      "depth": 1
    }
  ],
  "raw_data": {
    "tweet_id": "2100962703796039707",
    "text": "Key takeaways from the AGM 📝\n\n🎥 BCCI Honorary Secretary Mr. Devajit Saikia (@lonsaikia) sheds light on the major discussions held during the 95th Annual General Meeting 🙌 https://t.co/Xki706IrEh",
    "author_username": "BCCI",
    "author_display_name": "BCCI",
    "timestamp": "Fri Sep 18 14:58:37 +0000 2026",
    "likes": 1256,
    "retweets": 28,
    "replies": 25,
    "views": 0,
    "hashtags": [],
    "mentions": [
      "lonsaikia"
    ],
    "image_urls": [
      "https://pbs.twimg.com/amplify_video_thumb/2100962497952112640/img/GLlQ0vzghxABK_p6.jpg"
    ],
    "video_urls": [],
    "source": null,
    "is_retweet": false,
    "quote_tweet": null,
    "in_reply_to_id": null,
    "url": "https://x.com/BCCI/status/2100962703796039707",
    "replies_data": [
      {
        "tweet_id": "2101129990830198909",
        "text": "@BCCI @lonsaikia The commercial scale of the BCCI now rivals major global leagues, but managing that growth while balancing domestic structure remains a massive test. What's your take? 🏏",
        "author_username": "TheWorldEye_",
        "author_display_name": "The World Eye",
        "timestamp": "Sat Sep 19 02:03:21 +0000 2026",
        "likes": 0,
        "retweets": 0,
        "replies": 0,
        "views": 0,
        "hashtags": [],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/TheWorldEye_/status/2101129990830198909",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100964755771211849",
        "text": "@BCCI @lonsaikia Any dicussion on women team captaincy change?",
        "author_username": "kundudilip",
        "author_display_name": "ourINDIAourPRIDE🏹",
        "timestamp": "Fri Sep 18 15:06:46 +0000 2026",
        "likes": 2,
        "retweets": 0,
        "replies": 0,
        "views": 0,
        "hashtags": [],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/kundudilip/status/2100964755771211849",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100969770535604426",
        "text": "@BCCI @lonsaikia Regulate Skill-Based fantasy sports [RMG]\n#RegulateSkillGames \n#RMG",
        "author_username": "darkhorse3456",
        "author_display_name": "DarkHorse",
        "timestamp": "Fri Sep 18 15:26:42 +0000 2026",
        "likes": 3,
        "retweets": 2,
        "replies": 0,
        "views": 0,
        "hashtags": [
          "RegulateSkillGames",
          "RMG"
        ],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/darkhorse3456/status/2100969770535604426",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100980814863622191",
        "text": "@BCCI @lonsaikia “Eexar paatil vice captain”\nFamous line",
        "author_username": "MukeshGarg0771",
        "author_display_name": "Police911💀",
        "timestamp": "Fri Sep 18 16:10:35 +0000 2026",
        "likes": 0,
        "retweets": 0,
        "replies": 0,
        "views": 0,
        "hashtags": [],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/MukeshGarg0771/status/2100980814863622191",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100963168122179600",
        "text": "@BCCI @lonsaikia Great",
        "author_username": "nikitashivam88",
        "author_display_name": "Nikita राजस्थानी 💕",
        "timestamp": "Fri Sep 18 15:00:27 +0000 2026",
        "likes": 0,
        "retweets": 0,
        "replies": 0,
        "views": 0,
        "hashtags": [],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/nikitashivam88/status/2100963168122179600",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100990307072344535",
        "text": "@BCCI @lonsaikia Bro had the whole room nodding until the mic cut out. What was the real debate behind closed doors?",
        "author_username": "petrov74940",
        "author_display_name": "John Petrov",
        "timestamp": "Fri Sep 18 16:48:18 +0000 2026",
        "likes": 0,
        "retweets": 0,
        "replies": 0,
        "views": 0,
        "hashtags": [],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/petrov74940/status/2100990307072344535",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100965795065135537",
        "text": "@BCCI @lonsaikia \" We Want Back a Real Money Skill Gaming Industry in India #Dream11 🏟️🏌🏼\"",
        "author_username": "Manishchouhan__",
        "author_display_name": "The Third Eye View",
        "timestamp": "Fri Sep 18 15:10:54 +0000 2026",
        "likes": 2,
        "retweets": 0,
        "replies": 0,
        "views": 0,
        "hashtags": [
          "Dream11"
        ],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/Manishchouhan__/status/2100965795065135537",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100963624156114956",
        "text": "@BCCI @lonsaikia India's next-gen is cooking — the Team India buzz is real 🔥",
        "author_username": "rishabhxAi",
        "author_display_name": "rishabh",
        "timestamp": "Fri Sep 18 15:02:16 +0000 2026",
        "likes": 0,
        "retweets": 0,
        "replies": 0,
        "views": 0,
        "hashtags": [],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/rishabhxAi/status/2100963624156114956",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100974186865078471",
        "text": "@BCCI @lonsaikia Fantasy waps lao",
        "author_username": "Thenewsdropp",
        "author_display_name": "The News Drop",
        "timestamp": "Fri Sep 18 15:44:15 +0000 2026",
        "likes": 2,
        "retweets": 0,
        "replies": 0,
        "views": 0,
        "hashtags": [],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/Thenewsdropp/status/2100974186865078471",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100965296907395080",
        "text": "@BCCI @lonsaikia The next generation is looking seriously good for India 🙌",
        "author_username": "rishabhxAi",
        "author_display_name": "rishabh",
        "timestamp": "Fri Sep 18 15:08:55 +0000 2026",
        "likes": 0,
        "retweets": 0,
        "replies": 0,
        "views": 0,
        "hashtags": [],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/rishabhxAi/status/2100965296907395080",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100966395685335433",
        "text": "@BCCI @lonsaikia \" We Want Back a Real Money Skill Gaming Industry in India #Dream11 🏌🏼🏟️ @lonsaikia  \"",
        "author_username": "Manishchouhan__",
        "author_display_name": "The Third Eye View",
        "timestamp": "Fri Sep 18 15:13:17 +0000 2026",
        "likes": 3,
        "retweets": 2,
        "replies": 0,
        "views": 0,
        "hashtags": [
          "Dream11"
        ],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/Manishchouhan__/status/2100966395685335433",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100966360427933867",
        "text": "@BCCI @lonsaikia \" We Want Back a Real Money Skill Gaming Industry in India #Dream11 🏌🏼🏟️ @lonsaikia",
        "author_username": "Manishchouhan__",
        "author_display_name": "The Third Eye View",
        "timestamp": "Fri Sep 18 15:13:09 +0000 2026",
        "likes": 2,
        "retweets": 0,
        "replies": 0,
        "views": 0,
        "hashtags": [
          "Dream11"
        ],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/Manishchouhan__/status/2100966360427933867",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100971302702227538",
        "text": "🔥 BCCI 95th AGM just dropped the roadmap. Not minutes. Momentum.\n\nFrom Hon. Sec. Devajit Saikia after the Mumbai meeting:\n\n🏏 IPL 2027 = 20th edition. Board wants it celebrated GRAND.\n🇮🇳 BCCI CENTENARY 2028 — year-long programme from Dec 2027 through 2028.\n⚖️ Umpires & match referees get enhanced pay + grade reclassification.\n📋 Arun Singh Dhumal & M Khairul Jamal Majumdar inducted into IPL Governing Council.\n🧾 FY 2025-26 accounts passed. FY 2026-27 budget approved. Auditors appointed.\n🛡️ New Internal Committee under POSH policy.\n🪪 Age Verification Policy updated.\n♿ State units asked to back differently-abled cricketers with real facilities.\n\nThis is BCCI planning the next 24 months like a festival, not a file.\n\nWhich call hits hardest — IPL 20, BCCI 100, or the umpire pay hike?\n\n@BCCI @lonsaikia\n#BCCIAGM #IPL2027 #IndianCricket",
        "author_username": "AasheeshTiwarii",
        "author_display_name": "Aasheesh Tiwarii",
        "timestamp": "Fri Sep 18 15:32:47 +0000 2026",
        "likes": 0,
        "retweets": 0,
        "replies": 0,
        "views": 0,
        "hashtags": [
          "BCCIAGM",
          "IPL2027",
          "IndianCricket"
        ],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": "Key takeaways from the AGM 📝\n\n🎥 BCCI Honorary Secretary Mr. Devajit Saikia (@lonsaikia) sheds light on the major discussions held during the 95th Annual General Meeting 🙌 https://t.co/Xki706IrEh",
        "in_reply_to_id": null,
        "url": "https://x.com/AasheeshTiwarii/status/2100971302702227538",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2101030462294831427",
        "text": "@BCCI @lonsaikia Mohsin Naqvi ne  Asia cup ke mens and womens ke dono Trophies 🏆 dediye?",
        "author_username": "KSandee94241601",
        "author_display_name": "K Sandeep",
        "timestamp": "Fri Sep 18 19:27:52 +0000 2026",
        "likes": 0,
        "retweets": 0,
        "replies": 0,
        "views": 0,
        "hashtags": [],
        "mentions": [
          "BCCI",
          "lonsaikia"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/KSandee94241601/status/2101030462294831427",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      },
      {
        "tweet_id": "2100985314731049041",
        "text": "@BCCI @lonsaikia @GautamGambhir should be next. He has not achieved anything as coach. He should be hold accountable for our poor performance",
        "author_username": "luckyn",
        "author_display_name": "Rohit Sharma Fan",
        "timestamp": "Fri Sep 18 16:28:28 +0000 2026",
        "likes": 1,
        "retweets": 1,
        "replies": 0,
        "views": 0,
        "hashtags": [],
        "mentions": [
          "BCCI",
          "lonsaikia",
          "GautamGambhir"
        ],
        "image_urls": [],
        "video_urls": [],
        "source": null,
        "is_retweet": false,
        "quote_tweet": null,
        "in_reply_to_id": null,
        "url": "https://x.com/luckyn/status/2100985314731049041",
        "parent_tweet_id": "2100962703796039707",
        "depth": 1
      }
    ]
  },
  "saved_file": "C:\\Users\\ASUS\\Desktop\\SIH26\\youtube-insights\\data\\twitter\\tweet_2100962703796039707_20260919_043419.json"
}

export function combinePosts(youtubeData, telegramData, twitterData) {
  const youtubeArray = Array.isArray(youtubeData)
    ? youtubeData
    : [youtubeData];

  const telegramArray = Array.isArray(telegramData)
    ? telegramData
    : [telegramData];

  const twitterArray = Array.isArray(twitterData)
    ? twitterData
    : [twitterData];

  // YouTube data has an extra object wrapper around each video
  const youtubePostsData = youtubeArray.map((yt) => Object.values(yt)[0]);

  const youtubePosts = extractYouTubeData(youtubePostsData);
  const telegramPosts = extractTelegramData(
    telegramArray.length === 1 && telegramArray[0]?.posts
      ? telegramArray[0]
      : { posts: telegramArray }
  );
  const twitterPosts = extractTwitterData(twitterArray);

  return [
    ...youtubePosts,
    ...telegramPosts,
    ...twitterPosts,
  ];
}
