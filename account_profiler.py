import requests
from faker import Faker
import logging
from debug_logger import log_process
from telebot import TeleBot

# Setup Faker for generating fake profile data
faker = Faker()

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = "-"  # Replace with your token
bot = TeleBot(TELEGRAM_BOT_TOKEN)


def profile_account(account, proxy=None):
    """Profiles an Instagram account by updating bio, avatar, and link."""
    try:
        # Extract account details
        username = account.get("username")
        session_token = account.get("session_token")  # Assuming the account has a session token

        if not session_token:
            log_process("profiling", {"status": "error", "message": f"Missing session token for account: {username}"})
            bot.send_message(
                "YOUR_CHAT_ID", f"Profiling failed for account {username}: Missing session token."
            )
            return False

        # Generate random profile data
        bio = faker.text(max_nb_chars=150)
        avatar_url = "https://picsum.photos/200"  # Random placeholder avatar
        website_link = faker.url()

        log_process("profiling", {"status": "info", "message": f"Updating profile for {username}..."})
        bot.send_message("YOUR_CHAT_ID", f"Profiling account {username}...")

        # Mock API request to update profile (assuming private Instagram API)
        headers = {
            "Authorization": f"Bearer {session_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "bio": bio,
            "avatar_url": avatar_url,
            "website": website_link,
        }

        proxies = {"http": proxy, "https": proxy} if proxy else None

        response = requests.post(
            "https://instagram.com/api/v1/accounts/edit_profile/",
            headers=headers,
            json=payload,
            proxies=proxies,
            timeout=10
        )
        response.raise_for_status()

        log_process("profiling", {"status": "success", "message": f"Successfully updated profile for {username}."})
        bot.send_message("YOUR_CHAT_ID", f"Successfully profiled account {username}.")
        return True

    except Exception as e:
        log_process("profiling", {"status": "error", "message": f"Failed to profile account {username}: {e}"})
        bot.send_message(
            "YOUR_CHAT_ID", f"Profiling failed for account {username}: {e}"
        )
        return False


def profile_accounts(accounts, proxy_file=None):
    """Profiles multiple Instagram accounts with optional proxy support."""
    proxies = []
    if proxy_file:
        try:
            with open(proxy_file, 'r') as file:
                proxies = [line.strip() for line in file]
        except Exception as e:
            log_process("profiling", {"status": "error", "message": f"Failed to load proxy file: {e}"})
            bot.send_message("YOUR_CHAT_ID", f"Error loading proxy file: {e}")
            return

    for account in accounts:
        proxy = proxies.pop(0) if proxies else None
        success = profile_account(account, proxy=proxy)
        if success:
            log_process("profiling", {"status": "info", "message": f"Profiled account: {account['username']}"})
        else:
            log_process("profiling", {"status": "warning", "message": f"Skipped account: {account['username']}"})

    bot.send_message("YOUR_CHAT_ID", "Profiling process completed.")


@bot.message_handler(commands=['profile'])
def handle_profile_command(message):
    """Handles the '/profile' command to trigger account profiling."""
    try:
        bot.reply_to(message, "Starting profiling process...")
        # Sample accounts (replace with dynamic fetching if needed)
        sample_accounts = [
            {"username": "test_user1", "password": "password123", "session_token": "fake_session_token1"},
            {"username": "test_user2", "password": "password456", "session_token": "fake_session_token2"},
        ]
        profile_accounts(sample_accounts)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")


if __name__ == "__main__":
    # Start Telegram bot polling
    bot.polling()
