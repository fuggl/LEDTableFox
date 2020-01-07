#!/usr/bin/env python

import asyncio
import json
import logging
import websockets

logging.basicConfig()


def empty_consumer(action, value1, value2):
    print("{} {}".format(action, value1, value2))


STATE = {"value": 0, "round_nr": 0}
USERS = set()
CONSUMER = empty_consumer


def set_consumer(call):
    global CONSUMER
    CONSUMER = call


def set_state(key, value):
    global STATE
    STATE[key] = value


def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            CONSUMER(data["action"], data["value1"], data["value2"])
            await notify_state()
    finally:
        await unregister(websocket)


def init():
    start_server = websockets.serve(counter, "192.168.0.3", 6789)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
