
from sanic import Sanic
from sanic.response import file
import json
import rc_servo
import shot
from websockets.exceptions import ConnectionClosed
from sanic.exceptions import RequestTimeout
import ping

app = Sanic(__name__)
app.static('/static', '/home/pi/Projects/static')

client_ip = "0.0.0.0"

@app.route('/')
async def index(request):
    rc_servo.init()
    return await file('/home/pi/Projects/rc_sanic.html')

@app.websocket('/feed')
async def feed(request, ws):
    distancey =0.0
    distancex = 0.0
    directionx=""
    directiony=""
    await ws.send("Connected")
    while True:
        client_ip = ws.remote_address[0]
        print("IP:", client_ip)
        try:
            name = await ws.recv()
            print(name)    
        except (ConnectionClosed):
            print("Client disconected")
            rc_servo.stop()
            rc_servo.stopthrotle()
            name = None
        try:
            if(name=="less"):
                print("adjust left")
                pos = rc_servo.adjust("less")
                await ws.send(pos)
            elif(name=="default"):
                print("adjust default")
                pos = rc_servo.adjust("default")
                await ws.send(pos)
            elif(name=="more"):
                print("adjust more")
                pos = rc_servo.adjust("more")
                await ws.send(pos)
            elif(name=="snap"):
                print("snap")
                filename = shot.snap()
                await ws.send("Saved as: " + filename)

            else:
                json_str = json.dumps(name)
                json_obj = json.loads(name)
        #if True:
                joyid = int(json_obj["joyid"])
                directiony = json_obj["directiony"]
                directionx = json_obj["directionx"]
                distancey = float(json_obj["distancey"])
                distancex = float(json_obj["distancex"])
                print(str(joyid) + " " +str(distancey) + " "+ str(distancex) + " throtle:" + str(directiony) + " stir:"+ str(directionx))

                if(joyid == 0 and directiony=="None"):
                    rc_servo.stopthrotle()
                elif(joyid == 1 and directionx=="None"):
                    rc_servo.stop()
                else:  
                    if(ping.do_one(client_ip,0.5)<0.1):
                      s = rc_servo.move(directionx, directiony, distancex, distancey)
                      await ws.send(directiony + " and " + directionx)
                      print("MOVING! " , s)
        except:
            print("ERROR in data")
            rc_servo.stop()
            rc_servo.stopthrotle()        
            await ws.send("Data error!")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
