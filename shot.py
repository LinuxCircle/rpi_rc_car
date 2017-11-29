from urllib import request

import datetime
import time



def snap():
    now = datetime.datetime.now()
    t = now.strftime("%Y%m%dT%H%M%S")
    filename = "/home/pi/Pictures/snap" + t + ".jpg"
    request.urlretrieve("http://192.168.200.1:8080/?action=snapshot", filename)
    return filename
