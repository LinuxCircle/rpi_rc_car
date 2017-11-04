import time
 
import pigpio
 
pi = pigpio.pi() # Connect to local Pi.
#pi.stop()
#pi.start()
# set gpio modes
 
pi.set_mode(14, pigpio.OUTPUT)
pi.set_mode(15, pigpio.OUTPUT)

 
 
# start 1500 us servo pulses on gpio4

midthrotle = 1550 
midstir = 1450

time.sleep(1)
last = 0
lastx = 0
lasty = 0

def init():
 move("None", "None",0, 0)
 pi.set_PWM_dutycycle(15,255)
 pi.set_PWM_dutycycle(14,255)
 pi.set_servo_pulsewidth(15, midstir) #put it in middle
 pi.set_servo_pulsewidth(14, midthrotle) #stop it
 time.sleep(1)
 print("ready to rock and roll!!")
 

def move(dirx, diry, disx, disy):
 global lastx, lasty
 pulsey = 0
 if(diry=="up"):
   pulsey = int(midthrotle + float(disy/100 * 300))
 elif(diry=="down"):
   pulsey = int(midthrotle - float(disy/100 * 200))
 pi.set_servo_pulsewidth(14, pulsey)
 lasty = pulsey
 print(pulsey)
 if(dirx=="left"):
   left(disx)
 elif(dirx=="right"):
   right(disx)
 else:
   pi.set_servo_pulsewidth(15,midstir)
   lastx = midstir
 return dirx + " " + diry
def stopthrotle():
 pi.set_servo_pulsewidth(14, midthrotle)
 time.sleep(0.1)
 pi.set_PWM_dutycycle(14, 0) # 192/255 = 75%

def right(a): 
 global lastx
 pulse = int(midstir- float(a/100 * 400))
 print("SERVO right: " + str(pulse))	
 pi.set_servo_pulsewidth(15, pulse)
 lastx = pulse
 #time.sleep(0.1)

def left(a):
 global lastx 
 pulse = int(midstir + float(a/100 * 400))	
 print("SERVO left: " + str(pulse))
 pi.set_servo_pulsewidth(15, pulse)
 lastx = pulse
 #time.sleep(0.1)



def test():
 pi.set_servo_pulsewidth(15, 1000)
 time.sleep(1)
 pi.set_servo_pulsewidth(15, 1800)
 time.sleep(1)
 pi.set_servo_pulsewidth(15, 1400)
 time.sleep(1)
 pi.set_servo_pulsewidth(15, 0)
# start 75% dutycycle PWM on gpio17
 
 pi.set_PWM_dutycycle(14, 192) # 192/255 = 75%
 pi.stop()
def testPulse():
 for x in range(1000, 1800, 10):
   pi.set_servo_pulsewidth(14,x)
   print(x)
   time.sleep(0.1)
 for x in range(1800, 1000, -10):
   pi.set_servo_pulsewidth(14,x)
   print(x)
   time.sleep(0.1)


def testPWM():
 pi.set_PWM_dutycycle(15, 200)
 time.sleep(1)
 for x in range(200,0,-5):
   pi.set_PWM_dutycycle(15,x)
   time.sleep(0.1)
   print(x)
def stop():
 pi.set_PWM_dutycycle(15,255)
 global lastx
 print("SERVO stop")
# if(lastx>midstir):
#   for x in range(lastx,midstir-10,-10):
#     pi.set_servo_pulsewidth(15, x)
     #pi.set_PWM_dutycycle(15,x)
#     print(x)
#     time.sleep(0.01)
#     lastx = x
# elif(lastx<midstir):
#   for x in range(lastx, midstir+10, +10):
#     pi.set_servo_pulsewidth(15, x)
#     print(x)
#     time.sleep(0.01)
 pi.set_servo_pulsewidth(15, midstir)
 lastx = midstir
 time.sleep(0.3)
 pi.set_PWM_dutycycle(15, 0)
 #pi.stop()

if __name__ == '__main__':
    init() 
    move("left","up",100, 100)
    time.sleep(1)
    testPulse()
    stop()
    stopthrotle()
    pi.stop()
