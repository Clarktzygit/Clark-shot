import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
SHOTI_API_URL = "https://kaiz-apis.gleeze.com/api/shoti"
TIKTOK_STALK_API = "https://kaiz-apis.gleeze.com/api/tikstalk"
DEFAULT_ERROR_MSG = "⚠️ An error occurred while processing your request. Please try again later."

async def fetch_shoti_video():
    """Fetch a random Shoti video from the API."""
    try:
        response = requests.get(SHOTI_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'success':
            logger.error(f"API returned non-success status: {data}")
            return None
            
        return data.get('shoti')
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None
    except ValueError as e:
        logger.error(f"JSON decode error: {e}")
        return None

async def fetch_tikstalk_info(username: str):
    """Fetch TikTok user info from the API."""
    try:
        params = {'username': username.lstrip('@')}
        response = requests.get(TIKTOK_STALK_API, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('error'):
            logger.error(f"API returned error: {data.get('error')}")
            return None
            
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"TikStalk request failed: {e}")
        return None
    except ValueError as e:
        logger.error(f"TikStalk JSON decode error: {e}")
        return None

def create_video_caption(shoti_data):
    """Create a formatted caption for the video."""
    return (
        f"🎬 <b>{shoti_data['title']}</b>\n"
        f"📛 Username: @{shoti_data['username']}\n"
        f"🏷 Nickname: {shoti_data['nickname']}\n"
        f"⏱ Duration: {shoti_data['duration']} seconds\n"
        f"🌍 Region: {shoti_data['region']}\n\n"
    )

def create_user_info_caption(user_data):
    """Create a formatted caption for user info."""
    return (
        "📊 <b>TikTok User Info</b>\n\n"
        f"👤 <b>Username:</b> @{user_data.get('username', 'N/A')}\n"
        f"📛 <b>Nickname:</b> {user_data.get('nickname', 'N/A')}\n"
        f"📝 <b>Bio:</b> {user_data.get('signature', 'N/A')}\n"
        f"❤️ <b>Followers:</b> {user_data.get('followerCount', 'N/A'):,}\n"
        f"👀 <b>Following:</b> {user_data.get('followingCount', 'N/A'):,}\n"
        f"👍 <b>Likes:</b> {user_data.get('heartCount', 'N/A'):,}\n"
        f"🎥 <b>Videos:</b> {user_data.get('videoCount', 'N/A'):,}\n"
        f"🔒 <b>Private:</b> {'Yes' if user_data.get('privateAccount') else 'No'}\n"
        f"✔️ <b>Verified:</b> {'Yes' if user_data.get('verified') else 'No'}\n\n"
    )

async def shoti_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /shoti command."""
    await update.message.reply_chat_action(action='upload_video')
    
    shoti_data = await fetch_shoti_video()
    if not shoti_data:
        await update.message.reply_text(DEFAULT_ERROR_MSG)
        return
    
    try:
        # Send the video first
        caption = create_video_caption(shoti_data)
        await update.message.reply_video(
            video=shoti_data['videoUrl'],
            caption=caption,
            parse_mode='HTML',
            supports_streaming=True,
            write_timeout=60,
            read_timeout=60,
            connect_timeout=60
        )
        
        # Then fetch and send user info
        username = shoti_data['username']
        await update.message.reply_chat_action(action='typing')
        
        user_info = await fetch_tikstalk_info(username)
        if user_info:
            user_caption = create_user_info_caption(user_info)
            await update.message.reply_text(
                user_caption,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
        else:
            await update.message.reply_text(
                f"ℹ️ Couldn't fetch additional info for @{username}",
                parse_mode='HTML'
            )
        
    except Exception as e:
        logger.error(f"Error in shoti command: {e}")
        await update.message.reply_text(DEFAULT_ERROR_MSG)

# [Rest of the code remains the same: start_command, help_command, error_handler, main]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    welcome_msg = (
        "👋 Welcome to Shoti Video Bot!\n\n"
        "Use /shoti to get:\n"
        "- A random short video\n"
        "- Creator information\n"
        "- TikTok profile stats\n\n"
        "Enjoy! 😊"
    )
    await update.message.reply_text(welcome_msg)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    help_msg = (
        "🆘 <b>Shoti Video Bot Help</b>\n\n"
        "<b>Commands:</b>\n"
        "/start - Start the bot\n"
        "/shoti - Get a random short video + creator info\n"
        "/help - Show this help message\n\n"
        "⚠️ Note: All data is fetched from public APIs."
    )
    await update.message.reply_text(help_msg, parse_mode='HTML')

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)
    
    if isinstance(update, Update) and update.message:
        await update.message.reply_text(DEFAULT_ERROR_MSG)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token("8142915769:AAE0sny1JVAYE8c8eW_ttqmXPpunjiUNqnM").build()
    
    # Register commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("shoti", shoti_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Bot started and running...")

if __name__ == '__main__':
    main()