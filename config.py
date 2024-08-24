# Replace these with your actual API, token, IDs, and URLs.
API_ID = "API ID"
API_HASH = "API HASH"
BOT_TOKEN = "BOT TOKEN"
ADMIN_ID = "ADMIN ID AS INT "
channel_id = "@CHANNEL_ID"
channel_url = "https://t.me/CHANNEL_ID"
restart_bot = "https://t.me/BOT_ID?start=start"

# Data structures to manage bot state and users
user_status = {}           # Tracks the status of each user
forwarded_messages = {}    # Stores forwarded message details
blocked_users = []         # List of users blocked from the bot
users = []                 # List of all users interacting with the bot
bot_motor = {"active": True}   # Indicates whether the bot is active or paused
broadcast = {"active": False}  # Tracks the status of broadcast messages
