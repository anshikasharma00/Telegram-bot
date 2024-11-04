import logging
import os
import sys
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import yt_dlp

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if the token is loaded correctly
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if TELEGRAM_BOT_TOKEN is None:
    logger.error("TELEGRAM_BOT_TOKEN is not set in the environment variables.")
    sys.exit("Error: TELEGRAM_BOT_TOKEN is not set. Please check your .env file.")

# Global variable to store video information temporarily
video_info = {}

# Welcome command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "Welcome to Anshika's YouTube Video Downloading Bot!\n"
        "Use /help to see available commands."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text)

# Help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "/help - Show this help message\n"
        "/youtube - Start the video download process"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

# Validate YouTube URL
def is_valid_youtube_url(url: str) -> bool:
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    return re.match(youtube_regex, url) is not None

# YouTube video download handler
async def youtube_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide the YouTube video URL.")
    context.user_data['waiting_for_link'] = True  # Set flag to wait for the link

# Handle user responses for video link
async def handle_user_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('waiting_for_link'):
        url = update.message.text
        
        if not is_valid_youtube_url(url):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid YouTube URL. Please provide a valid URL.")
            return
        
        # Proceed to extract video information
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'noplaylist': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                global video_info
                video_info = ydl.extract_info(url, download=False)
                formats = video_info.get("formats", None)

                # Filter formats for available qualities
                available_formats = {f['format_id']: f for f in formats if 'mp4' in f['ext']}
                if not available_formats:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="No MP4 formats available for this video.")
                    return

                # Create a message with available formats
                format_message = "Available qualities:\n"
                for format_id, f in available_formats.items():
                    format_message += f"{format_id}: {f['ext']} ({f.get('format_note', 'N/A')}p)\n"

                format_message += "Please reply with the format ID you want to download."
                await context.bot.send_message(chat_id=update.effective_chat.id, text=format_message)

                # Set flag to wait for format selection
                context.user_data['waiting_for_link'] = False
                context.user_data['waiting_for_format'] = True
                context.user_data['available_formats'] = available_formats

        except Exception as e:
            logger.error(f"Error extracting video information: {e}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to retrieve video information. Please check the URL and try again.")

    elif context.user_data.get('waiting_for_format'):
        # Handle format selection
        format_id = update.message.text
        if format_id not in context.user_data['available_formats']:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid format ID. Please try again.")
            return

        # Download the video
        ydl_opts = {
            'format': format_id,
            'noplaylist': True,
            'outtmpl': '%(title)s.%(ext)s',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Video downloaded successfully!")

        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to download the video. Please check the URL and try again.")

        # Reset flags
        context.user_data['waiting_for_link'] = False
        context.user_data['waiting_for_format'] = False

# Main function
def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_command)
    youtube_handler = CommandHandler('youtube', youtube_video)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_user_response)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(youtube_handler)
    application.add_handler(message_handler)

    application.run_polling()

if __name__ == '__main__':
    main()