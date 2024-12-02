import logging
from flask import Flask, jsonify, request
import threading
import time
from telebot import TeleBot

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = "-"  # Update with your token
bot = TeleBot(TELEGRAM_BOT_TOKEN)

# Setup Flask app for web-based debugging dashboard
app = Flask(__name__)

# Global state for process monitoring
process_status = {
    "account_creation": [],
    "profiling": [],
    "interactions": [],
    "proxy_handling": [],
    "email_handling": [],
    "recaptcha_handling": [],  # Added for reCAPTCHA handling
    "email_verification": [],  # Added for email verification
}

error_logs = []  # Store recent errors for `/errors` command
# Lock for thread-safe updates
process_lock = threading.Lock()


def setup_debug_logger():
    """Set up and return the debug logger."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("DebugLogger")
    return logger


logger = setup_debug_logger()


def log_process(process_type, process_info):
    """Log and update process status."""
    with process_lock:
        process_status[process_type].append(process_info)
        if process_info.get("status") == "error":
            logger.error(f"[{process_type.upper()}] {process_info}")
            error_logs.append(process_info)  # Save errors for Telegram
        else:
            logger.info(f"[{process_type.upper()}] {process_info}")


@app.route("/status", methods=["GET"])
def get_status():
    """Return the status of all processes."""
    return jsonify(process_status)


@app.route("/control", methods=["POST"])
def control_process():
    """Control a process: pause, resume, or terminate."""
    data = request.json
    process_type = data.get("process_type")
    action = data.get("action")

    if process_type not in process_status:
        return jsonify({"error": "Invalid process type"}), 400

    logger.info(f"Action '{action}' received for process type '{process_type}'")
    return jsonify({"message": f"Action '{action}' applied to '{process_type}'"})


# Telegram Commands
@bot.message_handler(commands=['status'])
def send_status(message):
    """Send process status summary via Telegram."""
    status_message = "\n".join(
        f"{process}: {len(logs)} events logged" for process, logs in process_status.items()
    )
    bot.reply_to(message, f"Current Status:\n{status_message}")


@bot.message_handler(commands=['errors'])
def send_errors(message):
    """Send the most recent errors via Telegram."""
    if not error_logs:
        bot.reply_to(message, "No errors logged.")
        return

    errors_message = "\n".join(
        f"[{error['status']}] {error['message']}" for error in error_logs[-5:]
    )
    bot.reply_to(message, f"Recent Errors:\n{errors_message}")


@bot.message_handler(commands=['help'])
def send_help(message):
    """Send help message via Telegram."""
    help_message = (
        "Available Commands:\n"
        "/status - Get process status summary.\n"
        "/errors - Get the most recent errors.\n"
        "/help - Show this help message."
    )
    bot.reply_to(message, help_message)


# Threading for real-time monitoring
def monitor_processes():
    """Simulated process monitoring."""
    while True:
        with process_lock:
            for process_type, logs in process_status.items():
                logger.info(f"Monitoring {process_type}: {len(logs)} events logged.")
        time.sleep(10)


# Logging helper for reCAPTCHA
def log_recaptcha_step(step, success=True, details=None):
    """Log steps of the reCAPTCHA solving process."""
    status = "success" if success else "error"
    log_data = {"status": status, "step": step, "details": details}
    log_process("recaptcha_handling", log_data)


# Logging helper for email verification
def log_email_verification_step(step, success=True, details=None):
    """Log steps of the email verification process."""
    status = "success" if success else "error"
    log_data = {"status": status, "step": step, "details": details}
    log_process("email_verification", log_data)


if __name__ == "__main__":
    # Start monitoring thread
    monitoring_thread = threading.Thread(target=monitor_processes, daemon=True)
    monitoring_thread.start()

    # Start Flask app in a separate thread
    flask_thread = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=5000, debug=False), daemon=True
    )
    flask_thread.start()

    # Start Telegram bot polling
    bot.polling()
