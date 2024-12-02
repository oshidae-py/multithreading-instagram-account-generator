<div style="text-align: center;">
  <img src="Screenshots/instagram_logo_demon.png" alt="Demon" display: block; margin: 0 auto;>
<p style="font-size: 1.5em; text-align: center;">The ultimate tool for automated Instagram account generation and management</p>
</div>

---

# 🚨 WARNING: FOR EDUCATION PURPOSES ONLY! NOT INTENDED FOR ILLEGAL PURPOSES! 🚨

---

## Table of Contents
1. [Features Demonstration](#features-demonstration)
2. [Program Capabilities](#program-capabilities)
3. [Requirements](#requirements)
4. [Key Code Snippet](#key-code-snippet)
5. [Screenshots & Demo](#screenshots--demo)
6. [Credits](#credits)

---

## Features
### Account Management, Commands, Captcha Bypass:
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
  <img src="Screenshots/Thread_Checker_Commands" alt="Ability to Create Accounts" width="800">
  <img src="Screenshots/account_created.png" alt="Accounts Have Been Created" width="300">
  <img src="Screenshots/captcha_passed.png" alt="Captcha Has Been Passed" width="300">
</div>


---

## Program Capabilities
- Multithreading
- Proxy or proxyless deployment
- Uses temp mail api to confirm emails.
- Utilizes **Selenium** with undetected ChromeDriver for stealth browsing.
- Super-secret ChromeDriver configurations/settings ensuring a **100% undetection rate**.
- Updated reCAPTCHA v2 solver using audio processing.
- Dynamic **swarm functions** like bulk-follow and bulk-like actions.
- Account profiling includes avatar updates, bio, and link modifications.
- Advanced debug logging via a custom **Flask-based dashboard**.
- Command queue for batch interactions like `/like` or `/follow`.
- Minimal dependency on external APIs to avoid rate limits.
- Automatic proxy loading, testing, and rotation for anonymity.
- Error handling with Telegram bot notifications for real-time updates.

---

## Requirements
### To run this program, you will need:
- Python 3.8+

- More in requirements.txt
- Selenium: `pip install selenium`
- Undetected ChromeDriver: `pip install undetected-chromedriver`
- Flask (for debugging): `pip install flask`
- Requests: `pip install requests`
- Faker (for generating fake data): `pip install faker`
- TeleBot (for Telegram integration): `pip install pyTelegramBotAPI`
- Speech Recognition and PyDub (for reCAPTCHA solver):
  ```bash
  pip install speechrecognition pydub
  ```
- FFmpeg (for audio conversion): [Download here](https://ffmpeg.org/download.html)
- Latest **ChromeDriver** matching your Chrome version: [Download here](https://chromedriver.chromium.org/downloads)

---

## Key Code Snippet
Here is an example of how you can add custom bot features using the `interaction_manager.py`:

```python
from interaction_manager import follow_user

# Example of following a user
account = {"username": "demo_user", "session_token": "demo_token"}
user_id = "123456789"
follow_user(account, user_id)
```

---

## Screenshots & Demo
### Program in action:
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
  <img src="Screenshots/proxy_check_completed.png" alt="Proxy Check Completed" width="300">
  <img src="Screenshots/browser_score.png" alt="Undetected Browser Confirmed" width="300">
</div>

---

## Credits
1. [py-bypass-uc](https://github.com/storm0611/py-bypass-uc)
2. [selenium-recaptcha-solver](https://github.com/thicccat688/selenium-recaptcha-solver)

---

*For the full version of this program, contact @oshidaepy*
