import os
import time
import json
import winreg
import random
import requests
import websocket
import subprocess

chrome_path = None
try:
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")
except OSError:
    pass
else:
    chrome_path = winreg.QueryValue(key, "")
    winreg.CloseKey(key)
if chrome_path is not None:
    #port = random.randint(10000, 59999)
    port = 59999
    user_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_" + str(port))
    if not os.path.exists(user_data_dir):
        os.mkdir(user_data_dir)
    args = [
        chrome_path,
        "https://accounts.google.com/ServiceLogin?hl=en&continue=https://myaccount.google.com",
        "--remote-debugging-port={}".format(port),
        "--user-data-dir={}".format(user_data_dir),
        "--window-size=500,700",
        "--window-position=-7,0",
        "--no-default-browser-check",
        "--disable-default-apps",
        "--hide-crash-restore-bubble"
    ]
while True:
    try:
        response = requests.get("http://localhost:"+str(port)+"/json")
        response.raise_for_status()
        pages = response.json()
        ws_url= pages[0]['webSocketDebuggerUrl']
        ws = websocket.create_connection(ws_url)
        dom_msg = {
            "id": 1,
            "method": "DOM.enable"
        }
        ws.send(json.dumps(dom_msg))
        ws.recv()
        page_msg = {
            "id": 2,
            "method": "Page.enable"
        }
        ws.send(json.dumps(page_msg))
        ws.recv()
        nav_msg = {
            "id": 3,
            "method": "Page.navigate",
            "params": {
                "url": "https://accounts.google.com/ServiceLogin?hl=en&continue=https://mail.google.com/mail/"
            }
        }
        ws.send(json.dumps(nav_msg))
        ws.recv()
        while True:
            msg = json.loads(ws.recv())
            if "method" in msg and msg["method"] == "Page.loadEventFired":
                break
        script = {
            "id": 4,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "document.querySelector('input[type=email]').value='USERNAME'",
                "returnByValue": True
            }
        }
        ws.send(json.dumps(script))
        ws.recv()
        script = {
            "id": 5,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "document.querySelectorAll('button')[2].click()",
                "returnByValue": True
            }
        }
        ws.send(json.dumps(script))
        ws.recv()
        time.sleep(3)
        script = {
            "id": 6,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "document.querySelector('input[type=password]').value='PASSWORD'",
                "returnByValue": True
            }
        }
        ws.send(json.dumps(script))
        ws.recv()
        time.sleep(1)
        script = {
            "id": 7,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "document.querySelectorAll('button')[2].click()",
                "returnByValue": True
            }
        }
        ws.send(json.dumps(script))
        ws.recv()
        ws.close()
    except requests.exceptions.RequestException:
        subprocess.Popen(args)  # If requests.get() failed, open the URL in a web browser instead
