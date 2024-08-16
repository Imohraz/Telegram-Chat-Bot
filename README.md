## Getting Started

### Prerequisites

Before you start, ensure you have the following:

- Python 3.7 or higher
- A Telegram bot token from [BotFather](https://t.me/BotFather)
- Telegram API ID and Hash from [my.telegram.org](https://my.telegram.org)
- A Telegram channel ID for membership verification

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root of your project and add the following:

    ```env
    API_ID=your_api_id
    API_HASH=your_api_hash
    BOT_TOKEN=your_bot_token
    ADMIN_ID=your_admin_telegram_id
    ```

### Usage

1. **Run the bot:**

    ```bash
    python bot.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
