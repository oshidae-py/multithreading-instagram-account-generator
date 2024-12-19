import os
import shutil
import tempfile
import asyncio
import csv
import logging
import random
from rebrowser_playwright.async_api import async_playwright
from faker import Faker
from user_agent import generate_user_agent
from telebot import TeleBot
from RecaptchaSolver_playwright import RecaptchaSolver
from secmail import AsyncClient
import time
from random import randint
import re
import httpx
from playwright_stealth import stealth_async
from playwright.async_api import Page
from playwright.async_api import Page, BrowserContext
from browserforge.fingerprints import FingerprintGenerator
from browserforge.injectors.playwright import AsyncNewContext


# Initialize Faker for generating fake user data
faker = Faker()

# Setup logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AccountCreator")

# Initialize Telegram Bot
TELEGRAM_BOT_TOKEN = "--"
CHAT_ID = "-"

# Set up browser with optional proxy
def setup_browser(proxy=None):
    """Setup Selenium WebDriver with options for stealth and proxies."""
    chrome_options = Options()

    # Add stealth options
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,800")


print ("Contact @oshidaepy on Telegram for the UPDATED VERSION! + FULL SCRIPT!")
