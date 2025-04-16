#!/usr/bin/env python3
import datetime
import os
import sys
import requests
from dotenv import load_dotenv
load_dotenv()

def main():
    WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL_TEST")

    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = DEFAULT_MESSAGE

    payload = {
        "content": message
    }

    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        print("message post successes")
    else:
        print(f"message post failed, status_code: {response.status_code}")

if __name__ == '__main__':
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    DEFAULT_MESSAGE = f"test from discord_post.py : {now_str}"
    main()
