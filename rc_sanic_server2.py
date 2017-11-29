
from sanic import Sanic
from sanic.response import file
from sanic import response
from sanic.config import Config
import json
import rc_servo
import shot
from websockets.exceptions import ConnectionClosed
from sanic.exceptions import RequestTimeout
import rc_thread

Config.REQUEST_TIMEOUT = 60

app = Sanic(__name__)
app.static('/static', '/home/pi/Projects/static')

client_ip = "0.0.0.0"

a = None
b = None

@app.route('/')
async def index(request):
   # rc_servo.init()
    return await file('/home/pi/Projects/rc_sanic.html')

@app.exception(RequestTimeout)
def timeout(request, exception):
    print("Losing server")
#    a.stop()
#    b.stop()
#    a.join()
#    b.join()
    rc_servo.stopthrotle()

    #return response.text('RequestTimeout from error_handler.', 408)

@app.websocket('/feed')
async def feed(request, ws):
    global a,b
    distancey =0.0
    distancex = 0.0
    directionx=""
    directiony=""
    await ws.send("Connected")
    client_ip = ws.remote_address[0] 
    a = rc_thread.Thread_A("actuators")
    a.start()
    b = rc_thread.Thread_B("sensors")
    b.start()
    b.registerIP(client_ip)

    while True:
        try:
            name = await ws.recv()
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
                a.change(directionx, directiony, distancex, distancey)
                if(joyid == 0):
                    if(directiony=="up"):
                        dist = b.getdistance()
                        if(dist>100):
                            await ws.send(str(dist)+ "cm" )
                        elif(dist>65 and dist<=100):
                            await ws.send("slowly!" + str(dist) + "cm")
                        else:
                            await ws.send("CRASHING! "+ str(dist) + "cm")
                    elif(directiony=="down"):
                        await ws.send("Wifi:" + str(b.signal()))
                    else:
                        await ws.send("Bat:" + str(b.getvoltage()) + "V")
        except (ConnectionClosed):
            print("Client disconected")
            a.stop()
            b.stop()
            a.join()
            b.join()
            rc_servo.stopthrotle()
            break
        except KeyboardInterrupt:
            a.stop()
            b.stop()
            a.join()
            b.join()
            rc_servo.stopthrotle()
            println("Exit!")
            break
        except Exception as ex:
            print("exception: " , ex)
            #a.stop()
            #b.stop()
            #a.join()
            #b.join()
            rc_servo.stopthrotle()

            break

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

