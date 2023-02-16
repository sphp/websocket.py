import json
import websocket
import time

chrome_url = "ws://localhost:55555/devtools/page/3436581F6C3B1003F0372F33F78E29C6"
ws = websocket.create_connection(chrome_url)

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
        "expression": "document.querySelector('input[type=email]').value='GMAILID'",
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
time.sleep(2)
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

