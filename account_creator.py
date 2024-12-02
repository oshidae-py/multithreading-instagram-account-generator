import asyncio
import csv
import logging
from concurrent.futures import ThreadPoolExecutor
from secmail import AsyncClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from faker import Faker
from user_agent import generate_user_agent
import time
import requests
import random
import pickle  # Add this import


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
