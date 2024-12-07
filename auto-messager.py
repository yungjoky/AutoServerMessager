import requests
import json
import os
import time

settings_file = 'settings.json'

def help():
    print("For this program to work correctly you have to enter your authorization token and the channel id of the server you want to send messages to.")
    print("version 1.0 created by yungjoky")

def enter_auth_token():
    global auth
    auth = input("Enter your authorization token: ")

def enter_channel_id():
    global channel_id
    channel_id = input("Enter the channel id of the server: ")

def enter_content_message():
    global content
    content = input("Enter the message you want to get sent: ")

def set_message_interval():
    global interval
    interval = input("Enter the message interval (mm:ss): ")

def save_settings():
    settings = {
        'auth': auth,
        'channel_id': channel_id,
        'content': content,
        'interval': interval
    }
    with open(settings_file, 'w') as f:
        json.dump(settings, f)
    print("Settings saved.")

def load_settings():
    global auth, channel_id, content, interval
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            settings = json.load(f)
            auth = settings.get('auth')
            channel_id = settings.get('channel_id')
            content = settings.get('content')
            interval = settings.get('interval')
        print("Settings loaded.")
    else:
        print("No saved settings found.")

def start_auto_messager():
    while True:
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        payload = { 
            "content": f"{content}"
        }
        headers = {
            "Authorization": auth
        }
        res = requests.post(url, json=payload, headers=headers)
        print(res.status_code, res.text)
        if interval:
                try:
                    minutes, seconds = map(int, interval.split(':'))
                    time.sleep(minutes * 60 + seconds)
                except ValueError:
                    print("Invalid interval format. Please use mm:ss")
                    break
        else:
            break

def start_auto_messager_last_settings():
    load_settings()
    start_auto_messager()

def load_settings_only():
    load_settings()

while True:
    print("""1. Help  
2. Enter the authorization token of your account
3. Enter the content that you want to get sent in the server (message)
4. Enter the channel id of the server
5. Set a message interval (mm:ss)
6. Start the auto messager
7. Start the auto messager with the last settings
8. Load settings only
9. Save settings""")
    choice = input("Enter choice: ") 
    switcher = {
        '1': help,
        '2': enter_auth_token,
        '3': enter_content_message,
        '4': enter_channel_id,
        '5': set_message_interval,
        '6': start_auto_messager,
        '7': start_auto_messager_last_settings,
        '8': load_settings,
        '9': save_settings
    }
    func = switcher.get(choice)
    if func:
        func()
    else:
        print("Invalid choice")
