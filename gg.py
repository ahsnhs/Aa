async def room_kick(ws, room , tr):
    jsonbody = {HANDLER: HANDLER_ROOM_ADMIN, ID: gen_random_str(20), TYPE: TARGET_ROLE_KICK, ROOM: room, USERR: tr, TTT: "none" }
    #print(jsonbody)
    await ws.send(json.dumps(jsonbody))