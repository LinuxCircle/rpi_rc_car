import asyncio
import datetime
import random
import websockets
import json
import rc_servo

async def time(websocket, path):
    while True:
        #now = datetime.datetime.utcnow().isoformat() + 'Z'
        #await websocket.send(now)
        #await asyncio.sleep(random.random() * 3)
        name = await websocket.recv()
        json_str = json.dumps(name)
        json_obj = json.loads(name)
        #print(str(json_obj["distance"]) + " "+ str(json_obj["direction"]))
#        data = json_obj["direction"].split(":")
#        if(len(data)>1):
        data = json_obj["direction"]    
        print(str(json_obj["distance"]) + " "+ str(data))
        if(data=="left"):
            rc_servo.left(float(json_obj["distance"]))
        elif(data=="right"):
            rc_servo.right(float(json_obj["distance"]))
        else:
            rc_servo.stop()
start_server = websockets.serve(time, '192.168.200.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
