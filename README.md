# Telegram-bot 📹
Welcome to Anshika's YouTube Video Downloading Bot! This bot allows users to download YouTube videos directly through Telegram.

## Table of Contents 📚
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)

## Features ✨
- Download YouTube videos in various formats.
- User-friendly interface through Telegram.
- Error handling for invalid URLs and download issues.

## Installation ⚙️

**Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/youtube-video-downloader-bot.git
   cd youtube-video-downloader-bot
   ```

  2. **Install the required packages:**
     ```bash
     pip install python-telegram-bot yt-dlp python-dotenv
     ```
3. **Set up the environment:** Create a .env file in the root directory and add your Telegram Bot Token:
   ```plaintext
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```
4. **Run the bot:*
   ```bash
    python telebot.py
   ```

## Usage 🚀
- Open Telegram and search for your bot.
- Start a chat with the bot and use the `/start` command to initiate.
- Use the `/youtube` command to begin the video download process.
- Follow the prompts to provide a YouTube video URL and select the desired format.

## Commands 📜
- `/start` - Welcome message and instructions.
- `/help` - List of available commands.
- `/youtube` - Start the video download process.

## Example Interaction:
1. User sends `/youtube`.
2. Bot replies: "Please provide the YouTube video URL."
3. User sends a valid YouTube URL.
4. Bot replies with available formats.
5. User selects a format by replying with the format ID.
6. Bot downloads the video and confirms the download.
