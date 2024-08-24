from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import *

bot = Client("my_bot", API_ID, API_HASH, BOT_TOKEN)

@bot.on_message(filters.command('start') & filters.private)
async def start(client, message):
    users.append(message.from_user.id)
    user_status[message.from_user.id] = False
    forwarded = await client.forward_messages(ADMIN_ID, message.chat.id, message.id)
    await client.send_message(
        ADMIN_ID,
        f"@{message.from_user.username} - {message.from_user.id} - {message.from_user.first_name}start the bot",
        reply_to_message_id=forwarded.id,
    )
    if bot_motor["active"]:
        if message.from_user.id in blocked_users:
            await message.reply(
                "Sorry, you are blocked and cannot send messages.\n Once you are unblocked, you can send a message by "
                "using the <b>/start</b> command or check if you have been unblocked."
            )
        else:
            try:
                member = await client.get_chat_member(channel_id, message.from_user.id)
                if member.status:
                    if message.from_user.id == ADMIN_ID:
                        await message.reply(
                            text="""
Hello admin, use the following commands to control the robot. 

📊 /stats - bot stats

🔓 /unblock - Unblocks users

💤 /off - Shuts down the robot.

🛜  /on -  lets you turn the bot back on.

🆘 /help - More info

""",
                        )
                    else:
                        await message.reply(
                            text=f"Hi dear <b>{message.from_user.first_name}</b> ️",
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("📬 Send Message", callback_data='send_message')]
                            ])
                        )
            except:
                await message.reply(
                    text=f"Dear {message.from_user.first_name}, please join this channel to continue. Then, send the "
                         f"/start command or click on 'Restart' to use the bot",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("👥  join", url=channel_url)],
                        [InlineKeyboardButton("🔄  Restart", url=restart_bot)]
                    ])
                )
    else:
        await message.reply(
            "😴 Sorry, but the bot is currently on break. Please send the /start command to try again later"
        )


@bot.on_callback_query(filters.regex("send_message"))
async def send_message(client, callback_query):
    user_status[callback_query.from_user.id] = True
    if user_status:
        await callback_query.message.edit_text(
            text="Please send your message 🤩. To <b>'Cancel'</b>, send /cancel."
        )


@bot.on_message(filters.command("cancel"))
async def cancel(client, message):
    if user_status[message.from_user.id]:
        await message.reply(
            text="Message sending has been canceled. If you need to send another message, please use the <b>'Send "
                 "Message'</b> button.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📬 Send Message", callback_data='send_message')]
            ])
        )
        user_status[message.from_user.id] = False
    else:
        await message.reply(
            text="Use the <b>'Send Message'</b> button to send your message. For help, type the '/help' command.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📬 Send Message", callback_data='send_message')]
            ])
        )


@bot.on_message(~filters.user(ADMIN_ID) & filters.private)
async def new_message(client, message):
    if bot_motor["active"]:
        if message.from_user.id in blocked_users:
            await message.reply(
                "Sorry, you are blocked and cannot send messages.\n Once you are unblocked, you can send a message by "
                "using the <b>/start</b> command or check if you have been unblocked."
            )
        else:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🗣Reply", callback_data=f'adminReply_{message.from_user.id}_{message.id}')],
                [InlineKeyboardButton("🌚Seen", callback_data=f"seen_{message.from_user.id}_{message.id}")],
                [InlineKeyboardButton("🔒Block", callback_data=f"block_{message.from_user.id}_{message.id}")],
                [InlineKeyboardButton("🗃User info", callback_data=f"info_{message.from_user.id}_{message.id}")],
            ])
            try:
                member = await client.get_chat_member(channel_id, message.from_user.id)
                if member.status:
                    if user_status[message.from_user.id]:
                        forwarded_msg = await client.forward_messages(ADMIN_ID, message.chat.id, message.id)
                        await client.send_message(
                            ADMIN_ID,
                            f"User {message.from_user.first_name} - @{message.from_user.username or ''} sent this "
                            f"message 👆🏻",
                            reply_to_message_id=forwarded_msg.id,
                            reply_markup=keyboard
                        )
                        forwarded_messages[forwarded_msg.id] = message.chat.id
                        await message.reply(
                            text="Your message has been sent successfully.",
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("🚀 Send Again", callback_data="send_again")],
                            ]),
                            reply_to_message_id=message.id
                        )
                        user_status[message.from_user.id] = False
                    elif message.text == "/help":
                        await message.reply(
                            text=f"""

Hello dear <b>{message.from_user.first_name}</b>, welcome to my bot!
Please use the /start command and the buttons to send a message.
If you cancel sending the message, I won’t receive a notification.
You can use the <b>/bug</b> command to report any issues with the bot.
Have a great day!


"""
                        )
                    elif message.text == "/bug":
                        await client.send_message(
                            chat_id=ADMIN_ID,
                            text=f'{message.from_user.id}-{message.from_user.first_name}-@{message.from_user.username}'
                            'report a problem'
                        )
                        await message.reply(
                            "Your report has been sent to the admin. 👍🏼"
                        )
                    else:
                        await message.reply(
                            text="Use the <b>'Send Message'</b> button to send your message. For help, type the '/help'"
                                 " command.",
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("📬 Send Message", callback_data='send_message')]
                            ])
                        )
                else:
                    await message.reply(
                        "😴 Sorry, but the bot is currently on break. Please send the /start command to try again later"
                    )

            except:
                await message.reply(
                    text=f"Dear {message.from_user.first_name}"
                         ", please join this channel to continue. Then, send the /start command or click on "
                         "'Restart' to use the bot",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("👥  join", url=channel_url)],
                        [InlineKeyboardButton("🔄  Restart", url=restart_bot)]
                    ])
                )


@bot.on_callback_query(filters.regex("send_again"))
async def send_again(client, callback_query):
    user_status[callback_query.from_user.id] = True
    if user_status:
        await callback_query.message.edit_text(
            text="Please send your message 🤩. To <b>'Cancel'</b>, send /cancel."
        )


@bot.on_message(filters.command("help"))
async def help_command(client, message):
    if message.from_user.id == ADMIN_ID:
        await message.reply(
            text="""
🚀 Hello Admin, welcome to your chat bot.

📊 The /stats command shows the bot statistics and the number of users in your bot.

🔓 With the /unblock command, you can unblock a user by sending their user ID.

💤 The /off command allows you to temporarily turn off the bot,

🛜 and the /on command lets you turn the bot back on.

📢 Additionally, the /broadcast command enables you to send a message to all users.

""",
        )


@bot.on_message(filters.user(ADMIN_ID) & filters.reply)
async def admin_reply_message(client, message):
    original_msg_id = message.reply_to_message.id
    if original_msg_id in forwarded_messages:
        user_id = forwarded_messages[original_msg_id]
        await client.send_message(
            chat_id=user_id,
            text=message.text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Reply", callback_data=f"userReply_{message.id}")]
            ])
        )
        del forwarded_messages[original_msg_id]
    await message.reply(
        text="🚀 Your message has been sent successfully.",
        reply_to_message_id=message.id
    )


@bot.on_callback_query(filters.regex("user_reply"))
async def user_reply(client, callback_query):
    user_status[callback_query.from_user.id] = True
    await client.send_message(
        chat_id=callback_query.message.chat.id,
        text="🧐 Please send your message. To <b>'Cancel'</b>, send /cancel.",
        reply_to_message_id=callback_query.message.id
    )


@bot.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcasting(client, message):
    broadcast["active"] = True
    await message.reply(
        "You are currently sending a message to all users . . ."
    )


@bot.on_message(filters.user(ADMIN_ID))
async def admin_reply(client, message):
    if broadcast["active"]:
        for user in users:
            await client.send_message(
                chat_id=user,
                text=message.text
            )
            broadcast["active"] = False
        if broadcast["active"] == False:
            await message.reply(
                "message sent.📢",
                reply_to_message_id=message.id
            )
    else:
        if message.text == "/on":
            await message.reply(
                "Bot has been successfully started 🤩"
            )
            bot_motor["active"] = True
        elif message.text == "/off":
            await message.reply(
                "Bot has been successfully shut down 😴"
            )
            bot_motor["active"] = False
        elif message.text == "/":
            for user in users:
                await client.send_message(
                    chat_id=user,
                    text=message.text
                )
            await message.reply(
                "Your message have been successfully sent to all users✅"
            )
        else:
            await message.reply(
                "🖊 To respond to each user, reply to their message.\n\nget more help, send the /help command."
            )


@bot.on_callback_query(filters.regex("adminReply"))
async def admin_saw(client, callback_query):
    await callback_query.answer(
        "Just reply to the forwarded message and send it")


@bot.on_callback_query(filters.user(ADMIN_ID))
async def admin_query(client, callback_query):
    data = callback_query.data
    user_id = int(data.split('_')[1])
    message_id = int(data.split('_')[2])

    if data.startswith("info"):
        user = await client.get_users(user_id)
        user_info = f"""
🔺 Username: @{user.username} or ❌
🔺 ID :  {user.id}
🔺 Name : {user.first_name} - {user.last_name}
"""
        profile_photos = client.get_chat_photos(user_id)
        count = await client.get_chat_photos_count(user_id)
        photos_list = [photo async for photo in profile_photos]
        if count > 0:
            await client.send_photo(
                chat_id=ADMIN_ID,
                photo=photos_list[0].file_id,
                caption=user_info,
                reply_to_message_id=callback_query.message.id
            )
        else:
            await client.send_message(
                chat_id=ADMIN_ID,
                text=f"""
👹 User has no profile photo
🔺 Username: @{user.username} or ❌
🔺 ID :  {user.id}
🔺 Name : {user.first_name} - {user.last_name}
""",
                reply_to_message_id=callback_query.message.id

            )
    elif data.startswith("block"):
        user_status[user_id] = False
        blocked_users.append(user_id)
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🗣Reply", callback_data=f'adminReply_{user_id}_{message_id}')],
                [InlineKeyboardButton("🔓Unblock", callback_data=f"unblock_{user_id}_{message_id}")],
                [InlineKeyboardButton("🗃User info", callback_data=f"info_{user_id}_{message_id}")],
            ])
        )
        await client.send_message(
            chat_id=ADMIN_ID,
            text="User Blocked 🔒",
            reply_to_message_id=callback_query.message.id
        )
    elif data.startswith("unblock"):
        user_status[user_id] = False
        blocked_users.remove(user_id)
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🗣Reply", callback_data=f'adminReply_{user_id}_{message_id}')],
                [InlineKeyboardButton("🔒Block", callback_data=f"unblock_{user_id}_{message_id}")],
                [InlineKeyboardButton("🗃User info", callback_data=f"info_{user_id}_{message_id}")],
            ])
        )
        await client.send_message(
            chat_id=ADMIN_ID,
            text="User Unblocked 🔓",
            reply_to_message_id=callback_query.message.id
        )
    elif data.startswith("seen"):
        await client.send_message(
            chat_id=user_id,
            text="👀 Admin has seen your message",
            reply_to_message_id=message_id
        )
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🗣Reply", callback_data=f'adminReply_{user_id}_{message_id}')],
                [InlineKeyboardButton("🔒Block", callback_data=f"block_{user_id}_{message_id}")],
                [InlineKeyboardButton("🗃User info", callback_data=f"info_{user_id}_{message_id}")],
            ])
        )
        await client.send_message(
            chat_id=ADMIN_ID,
            text="🤓 User knows that their message has been seen.",
            reply_to_message_id=callback_query.message.id
        )


bot.run()
