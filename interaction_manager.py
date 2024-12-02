import requests
import logging
from time import sleep
from random import uniform
from queue import Queue
from debug_logger import log_process  # Use centralized debug logger
from telebot import TeleBot

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("InteractionManager")

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = "-"  # Replace with your token
bot = TeleBot(TELEGRAM_BOT_TOKEN)

# Command Queue for Swarm Actions
command_queue = Queue()

def like_post(account, post_id, proxy=None):
    """Likes a post on Instagram."""
    try:
        session_token = account.get("session_token")
        if not session_token:
            log_process("interactions", {"status": "error", "message": f"Missing session token for account: {account['username']}"})
            return False

        headers = {
            "Authorization": f"Bearer {session_token}",
            "Content-Type": "application/json",
        }

        proxies = {"http": proxy, "https": proxy} if proxy else None

        response = requests.post(f"https://instagram.com/api/v1/media/{post_id}/like/", headers=headers, proxies=proxies)
        response.raise_for_status()

        log_process("interactions", {"status": "success", "message": f"Account {account['username']} liked post {post_id}."})
        return True

    except Exception as e:
        log_process("interactions", {"status": "error", "message": f"Failed to like post {post_id} with account {account['username']}: {e}"})
        return False

def follow_user(account, user_id, proxy=None):
    """Follows a user on Instagram."""
    try:
        session_token = account.get("session_token")
        if not session_token:
            log_process("interactions", {"status": "error", "message": f"Missing session token for account: {account['username']}"})
            return False

        headers = {
            "Authorization": f"Bearer {session_token}",
            "Content-Type": "application/json",
        }

        proxies = {"http": proxy, "https": proxy} if proxy else None

        response = requests.post(f"https://instagram.com/api/v1/friendships/create/{user_id}/", headers=headers, proxies=proxies)
        response.raise_for_status()

        log_process("interactions", {"status": "success", "message": f"Account {account['username']} followed user {user_id}."})
        return True

    except Exception as e:
        log_process("interactions", {"status": "error", "message": f"Failed to follow user {user_id} with account {account['username']}: {e}"})
        return False

def process_command():
    """Processes commands from the queue."""
    while True:
        if not command_queue.empty():
            command = command_queue.get()
            action = command.get("action")
            target_id = command.get("target_id")
            accounts = command.get("accounts")
            proxy = command.get("proxy")

            for account in accounts:
                if action == "like":
                    success = like_post(account, target_id, proxy)
                elif action == "follow":
                    success = follow_user(account, target_id, proxy)
                else:
                    success = False

                if success:
                    bot.send_message(command["chat_id"], f"Action '{action}' succeeded for account: {account['username']}")
                else:
                    bot.send_message(command["chat_id"], f"Action '{action}' failed for account: {account['username']}")

                sleep(uniform(2, 5))  # Add a random delay to mimic human behavior

@bot.message_handler(commands=['like'])
def handle_like_command(message):
    """Handles the '/like' command."""
    try:
        post_id = message.text.split(" ")[1]  # Extract post ID
        command_queue.put({
            "action": "like",
            "target_id": post_id,
            "accounts": sample_accounts,
            "chat_id": message.chat.id,
            "proxy": None,  # Add proxy handling if needed
        })
        bot.reply_to(message, f"Enqueued 'like' action for post {post_id}.")
    except IndexError:
        bot.reply_to(message, "Usage: /like [post_id]")

@bot.message_handler(commands=['follow'])
def handle_follow_command(message):
    """Handles the '/follow' command."""
    try:
        username = message.text.split(" ")[1]  # Extract username
        command_queue.put({
            "action": "follow",
            "target_id": username,
            "accounts": sample_accounts,
            "chat_id": message.chat.id,
            "proxy": None,  # Add proxy handling if needed
        })
        bot.reply_to(message, f"Enqueued 'follow' action for user {username}.")
    except IndexError:
        bot.reply_to(message, "Usage: /follow [username]")

if __name__ == "__main__":
    # Sample accounts for demonstration
    sample_accounts = [
        {"username": "test_user1", "session_token": "fake_session_token1"},
        {"username": "test_user2", "session_token": "fake_session_token2"},
    ]

    # Start the command processor in a separate thread
    command_processor_thread = threading.Thread(target=process_command, daemon=True)
    command_processor_thread.start()

    # Start Telegram bot polling
    bot.polling()
