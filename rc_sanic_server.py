
from sanic import Sanic
from sanic.response import file
import json
import rc_servo

app = Sanic(__name__)
app.static('/static', '/home/pi/Projects/static')

@app.route('/')
async def index(request):
    rc_servo.init()
    return await file('/home/pi/Projects/rc_sanic.html')

@app.websocket('/feed')
async def feed(request, ws):
    while True:
        name = await ws.recv()
        json_str = json.dumps(name)
        json_obj = json.loads(name)
        #print(str(json_obj["distance"]) + " "+ str(json_obj["direction"]))
#        data = json_obj["direction"].split(":")
#        if(len(data)>1):
        distancey =0.0
        distancex = 0.0
        directionx=""
        directiony=""
    # try:
        if True:
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
                rc_servo.move(directionx, directiony, distancex, distancey)

     #   except:
      #      print("ERROR in data")
      #      rc_servo.stop()
      #      rc_servo.stopthrotle()        

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
