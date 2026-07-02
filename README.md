# AWB (Awfully Written Bot)

A Telegram bot designed for secure message forwarding with captcha verification. 

## Features

- **Captcha Verification**: Users must solve an image-based captcha before their messages are forwarded.
- **Support for All Media**: Forwarding works for text, photos, videos, documents, audio, and voice messages.
- **Message Redirection**: Verified messages are automatically redirected to a configured group chat.
- **Anonymized Forwarding**: Messages are forwarded with a custom prefix `Forwarding, ID [MSG_ID]:`, maintaining privacy while allowing for message tracking.
- **Locale Support**: Built-in support for multiple languages (defaulting to English).
- **Admin Panel**: Authorized admins can access usage statistics and message logs.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd AWB
   ```

2. **Install dependencies**:
   This project uses `uv` for dependency management.
   ```bash
   uv sync
   ```
   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Copy `.env.dist` to `.env` and fill in your details:
   ```bash
   cp .env.dist .env
   ```
   Edit `.env`:
   - `BOT_TOKEN`: Your Telegram Bot token from @BotFather.
   - `GROUP_CHAT_ID`: The ID of the group where messages should be redirected.
   - `ADMIN_IDS`: A comma-separated list of Telegram User IDs who can access admin commands.
   - `DISABLE_CAPTCHA`: Set to `True` to disable the captcha verification step (optional, defaults to `False`).

## Usage

### For Users
1. Start the bot with `/start`.
2. Send any message or media.
3. Solve the image captcha by typing the characters shown.
4. Once solved, your message is redirected to the destination group.

### For Admins
- `/stats`: View total user count.
- `/logs`: See a list of the 10 most recent redirected messages.
- `/view <ID>`: View detailed information about a specific message by its ID.

## Commands

- `/start`: Initialize the bot and receive a welcome message.
- `/id`: Retrieve the ID of the current chat (useful for configuration).

## Adding Locales

The bot supports multiple languages. To add a new locale:

1. Create a new JSON file in the `locales/` directory named after the language code (e.g., `fr.json` for French).
2. Copy the keys from `locales/en.json` and provide the translations for your language.
3. The bot will automatically load the new locale on startup.


