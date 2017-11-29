import time
 
import pigpio

import timeit
 
pi = pigpio.pi() # Connect to local Pi.
#pi.stop()
#pi.start()
# set gpio modes
 
pi.set_mode(14, pigpio.OUTPUT)
pi.set_mode(15, pigpio.OUTPUT)

 
 
# start 1500 us servo pulses on gpio4

midthrotle = 1500 
midstir = 1485

last = 0
lastx = midstir
lasty = midthrotle

direction = "None"
ready_to_stop = True
ready_to_stop_gas = True

def init():
 move("None", "None",0, 0)
# pi.set_servo_pulsewidth(15, midstir + 100)
# time.sleep(1)
# pi.set_servo_pulsewidth(15, midstir - 100)
# time.sleep(1)
 pi.set_PWM_dutycycle(15, 192) # 192/255 = 75%
 pi.set_PWM_dutycycle(14, 60) # 192/255 = 75%
 pi.set_servo_pulsewidth(15, midstir) #put it in middle
 time.sleep(0.5)
 pi.set_servo_pulsewidth(14, midthrotle) #stop it
 time.sleep(0.5)
print("ready to rock and roll!!")
 
def adjust(p):
 global midstir
 if(p=="more"):
  midstir = midstir - 15
  pi.set_servo_pulsewidth(15, midstir)
  time.sleep(0.5)
 elif(p=="less"):
  midstir = midstir + 15
  pi.set_servo_pulsewidth(15, midstir)
  time.sleep(0.5)
 else:
  midstir = 1485
  pi.set_servo_pulsewidth(15, midstir)
  time.sleep(0.4)
 pi.set_PWM_dutycycle(15, 0) # 192/255 = 75%
 return str(midstir)

def changedir(d):
 global direction
 direction = d
    

def move(dirx, diry, disx, disy):
 global lastx, lasty
 global ready_to_stop
 global ready_to_stop_gas
# pi.set_PWM_dutycycle(14, 255) # 192/255 = 75%
 if(dirx == "left"):
   left(disx)
   ready_to_stop = True
 elif(dirx == "right"):
   right(disx)
   ready_to_stop = True
 else:
   if(ready_to_stop == True):
    stop()
    ready_to_stop = False
 
 pulsey = midthrotle
# start_time = timeit.default_timer()
# code you want to evaluate
 if(diry=="up"):
   pulsey = int(midthrotle + float(disy/100 * 300))
   ready_to_stop_gas = True
   pi.set_servo_pulsewidth (14,pulsey)
 elif(diry=="down"):
   pulsey = int(midthrotle - 50 - float(disy/100 * 250))
   ready_to_stop_gas = True   
   pi.set_servo_pulsewidth (14,pulsey)
 else:
   if(ready_to_stop_gas == True):
     pulsey = midthrotle
#     pi.set_servo_pulsewidth (14,pulsey)
     stopthrotle()
#     time.sleep(0.1)
#     pi.set_PWM_dutycycle(14, 0) # 192/255 = 75%
     ready_to_stop_gas = False

# code you want to evaluate
# elapsed = timeit.default_timer() - start_time
# print("Elapsed time: ", elapsed)
 lasty = pulsey
# print(pulsey)
 return dirx, diry

def emergencybreak():
 global lasty
 print("EMEGENCY BREAK!")
 pi.set_servo_pulsewidth(14, midthrotle)
 lasty = midthrotle
 time.sleep(1)

def stopthrotle():
 global lasty
 print(str(lasty) , " mid = " , str( midthrotle))
 y = lasty
 x = 5

 if(lasty>midthrotle):
   #for y in range(lasty,midthrotle-10,for j in  range (0,)):
   while(y>midthrotle):
     pi.set_servo_pulsewidth(14, y)
     print(y)
     y -= int(x)
     x = x *2
     time.sleep(0.05)
 elif(lasty<midthrotle):
   while(y<midthrotle):
     pi.set_servo_pulsewidth(14, y)
     print(y)
     y += int(x)
     x = x *2
     time.sleep(0.05) 

 pi.set_servo_pulsewidth(14, midthrotle)
 time.sleep(0.05)
 lasty = midthrotle
 pi.set_PWM_dutycycle(14, 0) # 192/255 = 75%

def right(a): 
 global lastx
 pulse = int(midstir- float(a/100 * 350))
 print("SERVO right: " + str(pulse))	
 pi.set_servo_pulsewidth(15, pulse)
 lastx = pulse
 #time.sleep(0.01)

def left(a):
 global lastx 
 pulse = int(midstir + float(a/100 * 350))	
 print("SERVO left: " + str(pulse))
 pi.set_servo_pulsewidth(15, pulse)
 lastx = pulse
 #time.sleep(0.01)



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
 for x in range(mid_throtle, 1800, 10):
   pi.set_servo_pulsewidth(14,x)
   print(x)
   time.sleep(0.1)
 for x in range(1800, midthrotle, -10):
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
 global lastx
 print("SERVO stop")
 pi.set_servo_pulsewidth(15, midstir)
 lastx = midstir
 time.sleep(0.3)
 pi.set_PWM_dutycycle(15, 0)
 #pi.stop()

if __name__ == '__main__':
    init() 
    move("left","up",100, 100)
    stopthrotle()
    time.sleep(1)
    testPulse()
    stop()
    stopthrotle()
    pi.stop()
