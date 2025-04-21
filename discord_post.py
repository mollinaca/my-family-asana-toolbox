#!/usr/bin/env python3
import datetime
import os
import requests
from dotenv import load_dotenv
load_dotenv()

def post(message:str = "test message"):
    ret = {"ok": False}
    WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

    payload = {
        "content": message
    }
    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        ret = {"ok": True}
    else:
        ret = {"ok": False, "status_code": response.status_code}
    
    return ret
