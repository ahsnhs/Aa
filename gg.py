
import websockets
import asyncio
import json
import random
import requests
BOT_ID = "2-2-2"
BOT_PWD = "nm12345"
NameRooms = "نبض"
ID = "id"
NAME = "name"
USERNAME = "username"
PASSWORD = "password"
ROOM = "room"
TYPE = "type"
HANDLER = "handler"
ALLOWED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"
SOCKET_URL = "wss://chatp.net:5333/server"
MSG_BODY = "body"
MSG_FROM = "from"
MSG_TO = "to"
MSG_TYPE_TXT = "text"
MSG_TYPE_IMG = "image"
MSG_TYPE_AUDIO = "audio"
MSG_URL = "url"
MSG_LENGTH = "length"
HANDLER_LOGIN = "login"
HANDLER_LOGIN_EVENT = "login_event"
HANDLER_ROOM_JOIN = "room_join"
HANDLER_ROOM_LEAVE = "room_leave"
HANDLER_ROOM_ADMIN = "room_admin"
HANDLER_ROOM_EVENT = "room_event"
HANDLER_ROOM_MESSAGE = "room_message"
EVENT_TYPE_SUCCESS = "success"

async def on_message(ws, data):    
    msg = data[MSG_BODY]
    frm = data[MSG_FROM]
    room = data[ROOM]
    if frm == BOT_ID:
           return

async def login(ws):
    jsonbody = {HANDLER: HANDLER_LOGIN, ID: gen_random_str(20), USERNAME: BOT_ID, PASSWORD: BOT_PWD}
    #print(jsonbody)
    await ws.send(json.dumps(jsonbody))

async def join_group(ws, group):
    jsonbody = {HANDLER: HANDLER_ROOM_JOIN, ID: gen_random_str(20), NAME: group}
    await ws.send(json.dumps(jsonbody))
def gen_random_str(length):
    return ''.join(random.choice(ALLOWED_CHARS) for i in range(length))

async def start_bot():
    websocket = await websockets.connect(SOCKET_URL, ssl=True)
    await login(websocket)

    while True:
        if not websocket.open:
            try:
                websocket = await websockets.connect(SOCKET_URL, ssl=True)
                print('Websocket is NOT connected. Reconnecting...')
                await login(websocket)
            except websockets.exceptions.WebSocketException as ex:
                print("Error: " + ex)

        try:
            async for payload in websocket:
                if payload is not None:
                    data = json.loads(payload)
                    handler = data[HANDLER]
                    if handler == HANDLER_LOGIN_EVENT and data[TYPE] == EVENT_TYPE_SUCCESS:
                        print("Logged In SUCCESS ✅")
                        await join_group(websocket, NameRooms)
                    elif handler == HANDLER_ROOM_EVENT and data[TYPE] == MSG_TYPE_TXT:
                        await on_message(websocket, data)
                    elif handler == HANDLER_ROOM_EVENT and data[TYPE] == MSG_TYPE_IMG:
                        await on_image_msg(websocket, data)                            

                                          
        except:
            print('Error receiving message from websocket.')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
    loop.run_forever()
