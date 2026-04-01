"""
NOTIFIER: The alerting system of ACA.
Purpose: Sends desktop and mobile alerts when new jobs are discovered.
Connections: Called by dashboard.py after a successful search_jobs() call.
"""

import requests # Used for Telegram API calls
import os

def send_notification(message):
    """
    Multichannel Alert System: Desktop (Win10) and Telegram.
    Inputs: The message string to broadcast.
    """
    
    # 1. DESKTOP ALERT (Using Windows 10/11 Toast Notifications)
    try:
        from win10toast import ToastNotifier # External library for Win10 alerts
        toaster = ToastNotifier()
        toaster.show_toast(
            "ACA Job Discovery Alert", # Notification Title
            message,                   # Notification Body
            duration=5,                # Seconds to display
            threaded=True              # Runs in the background so app doesn't hang
        )
    except Exception as e:
        # Fallback if library is missing or fails
        print(f"Desktop notification failed: {e}")

    # 2. TELEGRAM ALERT (Using Bot API)
    # Token and Chat ID must be set in the .env file for this to work.
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if token and chat_id:
        # Construct the official Telegram API URL
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            # Send the message via HTTP POST request
            payload = {"chat_id": chat_id, "text": f"?? ACA ALERT: {message}"}
            requests.post(url, data=payload, timeout=10)
        except Exception as e:
            # Silence silent errors to keep the search loop running
            print(f"Telegram notification failed: {e}")
