# Shoti Video Bot

A Telegram bot that fetches random short videos from TikTok along with creator information using public APIs.

## Features

- Fetch random short videos from TikTok
- Display detailed video information (title, username, duration, region)
- Show creator profile statistics (followers, following, likes, etc.)
- Simple and intuitive commands

## Commands

- `/start` - Start the bot and see welcome message
- `/shoti` - Get a random short video with creator info
- `/help` - Show help information

## Setup

### Prerequisites

- Python 3.7 or higher
- Telegram bot token (get from [@BotFather](https://t.me/BotFather))
- Required Python packages

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/shoti-bot.git
   cd shoti-bot
   ```

2. Install the required packages:
   ```bash
   pip install python-telegram-bot requests
   ```

3. Set up your environment:
   - Replace the bot token in `shot.py` with your own token:
     ```python
     application = Application.builder().token("YOUR_BOT_TOKEN_HERE").build()
     ```

4. Run the bot:
   ```bash
   python shot.py
   ```

## Configuration

The bot uses the following APIs by default:
- Shoti API: `https://kaiz-apis.gleeze.com/api/shoti`
- TikTok Stalk API: `https://kaiz-apis.gleeze.com/api/tikstalk`

You can modify these endpoints in the script if needed.

## Error Handling

The bot includes basic error handling and will notify users when something goes wrong with a generic error message.

## Contributing

Contributions are welcome! Please open an issue or pull request for any improvements or bug fixes.

## License

This project is open source and available under the [MIT License](LICENSE).

---

**Note:** This bot uses third-party APIs that may change or become unavailable without notice. The bot owner is not responsible for the content fetched from these APIs.
