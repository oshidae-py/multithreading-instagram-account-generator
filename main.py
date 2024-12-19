import threading
import asyncio
from telebot import TeleBot
from account_creator import create_accounts, load_proxies
from debug_logger import setup_debug_logger
import time


# Initialize Logger
logger = setup_debug_logger()

# Global configuration
CONFIG = {
    "telegram_bot_token": "INPUT YOUR TOKEN HERE!",  # Replace with your Telegram bot token
    "proxy_file": "proxies.txt"  # Path to proxy list file
}

# Initialize Telegram Bot
bot = TeleBot(CONFIG["telegram_bot_token"])

# Telegram Command Handlers
@bot.message_handler(commands=['createaccount'])
def handle_createaccount(message):
    try:
        # Parse command arguments
        args = message.text.replace('/createaccount', '').strip().split()
        params = {}
        for arg in args:
            if '=' in arg:
                key, value = arg.split('=', 1)
                params[key.strip()] = value.strip()

        # Extract and validate arguments with defaults
        threads = int(params.get('threads', 1))
        max_accounts = int(params.get('max_accounts', 1))
        use_proxy = params.get('use_proxy', 'false').lower() == 'true'

        if threads <= 0 or max_accounts <= 0:
            raise ValueError("Threads and max_accounts must be positive integers.")

        # Notify user about the process start
        bot.reply_to(
            message,
            f"Starting account creation with {threads} threads, {max_accounts} accounts, use_proxy={use_proxy}."
        )

        # Run account creation
        async def run_account_creation():
            tasks = []
            for _ in range(threads):
                task = create_accounts(
                    max_accounts // threads,
                    proxy_file=CONFIG["proxy_file"],
                    use_proxy=use_proxy
                )
                tasks.append(task)

            results = await asyncio.gather(*tasks)

            for accounts in results:
                if not accounts:
                    bot.send_message(
                        message.chat.id,
                        "No accounts were created. Please check the logs for details."
                    )
                for account in accounts:
                    bot.send_message(
                        message.chat.id,
                        f"Account created:\n"
                        f"Email: {account['email']}\n"
                        f"Username: {account['username']}\n"
                        f"Password: {account['password']}"
                    )

        # Use a thread-safe execution for asyncio.run()
        threading.Thread(target=lambda: asyncio.run(run_account_creation()), daemon=True).start()

    except ValueError as ve:
        bot.reply_to(message, f"Error: {ve}")
    except Exception as e:
        logger.error(f"Error in handle_createaccount: {e}")
        bot.reply_to(message, "Error: Failed to start account creation. Please check your command format.")

@bot.message_handler(commands=['proxynumber'])
def handle_proxynumber(message):
    try:
        proxies = load_proxies(CONFIG["proxy_file"])
        bot.reply_to(message, f"Total proxies loaded: {len(proxies)}")
    except Exception as e:
        logger.error(f"Error in handle_proxynumber: {e}")
        bot.reply_to(message, "Error: Failed to load proxies.")

@bot.message_handler(commands=['proxycheck'])
def handle_proxycheck(message):
    try:
        proxies = load_proxies(CONFIG["proxy_file"])
        working_proxies = [proxy for proxy in proxies if test_proxy(proxy)]
        bot.send_message(
            message.chat.id,
            f"Working proxies: {len(working_proxies)}\n" + "\n".join(working_proxies)
        )
    except Exception as e:
        logger.error(f"Error in handle_proxycheck: {e}")
        bot.reply_to(message, "Error: Failed to check proxies.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    """Provide a list of available commands and their usage."""
    help_text = (
        "Available commands:\n"
        "/createaccount threads=<num> max_accounts=<num> use_proxy=<true/false> - Start account creation.\n"
        "/proxynumber - Display the number of proxies loaded.\n"
        "/proxycheck - Test proxies and display the working ones.\n"
        "/help - Show this help message.\n"
        "/status - Display the status of running threads and processes."
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['status'])
def handle_status(message):
    """Provide the status of active threads and processes."""
    try:
        active_threads = threading.enumerate()
        status_text = "Active threads:\n"
        for thread in active_threads:
            status_text += f"- {thread.name}: {'Alive' if thread.is_alive() else 'Not Alive'}\n"
        bot.reply_to(message, status_text)
    except Exception as e:
        logger.error(f"Error in handle_status: {e}")
        bot.reply_to(message, "Error: Failed to retrieve status.")

# Monitor Processes
def monitor_processes():
    while True:
        logger.info("Monitoring active threads...")
        for thread in threading.enumerate():
            logger.info(f"Thread: {thread.name}, Alive: {thread.is_alive()}")
        time.sleep(5)

# Main Orchestrator
if __name__ == "__main__":
    logger.info("Starting Main Orchestrator...")

    # Launch Monitor Thread
    monitor_thread = threading.Thread(target=monitor_processes, daemon=True)
    monitor_thread.start()

    # Start Telegram Bot in a separate thread
    telegram_thread = threading.Thread(target=bot.infinity_polling, daemon=True)
    telegram_thread.start()

    # Wait for all threads to finish
    monitor_thread.join()
    telegram_thread.join()
