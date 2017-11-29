import time
message = ""
while True:
    if(message=="forward"):
        print("going " , message)
    else:
        print("stop")
    time.sleep(0.1)

def move(m):
    global message
    message = m
