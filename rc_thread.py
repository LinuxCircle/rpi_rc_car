import threading
import time
import rc_servo
import ping
c = threading.Condition()
flag = False      #shared between Thread_A and Thread_B
dirx = "None"
diry = "None"
disx = 0
disy = 0
ip = "192.168.200.1"
distance = 0
voltage = 0
timedout = False
import rc_i2c2

class Thread_A(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.running = True
        print(name , " created")
    def stop(self):
        self.running = False
    def run(self):
        global flag
        global dirx, diry, disx, disy     #made global here
        global distance
        global timedout
        readytostop = False
        self.running = True
        distance = 0
        try:
         while self.running:
         #   c.acquire()
            if(timedout ==False):
                if (diry !="None"): 
                    if(diry == "up"):
                        if(flag == False):
                            rc_i2c2.begin_reading()
                            flag = True
                        try:
                            distance = int(rc_i2c2.get_volt_and_distance()[1])
                        except Exception as a:
                            print("Error reading!", a)
                        if(distance<=0):
                            print("False reading")
                        elif(distance>80):
                            print ("Values: " + " " + str(dirx) + " " + str(diry) + " " + str(disx) + " " + str(disy)+ " in " + str(distance) + "cm")
                            rc_servo.move(dirx, diry, disx, disy)
                            readytostop = True
                        else:
                            print("Going to crash!", str(distance) , "cm")
                            if(readytostop):
                                rc_servo.emergencybreak()
                                readytostop = False
                            else:
                                print("Do Nothing")
                        
                    else:
                        if flag==True:
                            rc_i2c2.end_reading()
                            flag = False
                        rc_servo.move(dirx,diry,disx,disy)
                        print ("Values: " + " " + str(dirx) + " " + str(diry) + " " + str(disx) + " " + str(disy))
#        c.notify_all()
                    time.sleep(0.1)
                else:
 
                   # print ("Values: " + " " + str(dirx) + " " + str(diry) + " " + str(disx) + " " + str(disy))
                    if flag==True:
                        rc_i2c2.end_reading()
                        flag = False
                    rc_servo.move(dirx, diry, disx, disy)
            else:
                rc_servo.stopthrotle()
                #c.wait()
                print("Lost connection. Ping = ",pingtime," second")
                dirx = "None"
                diry = "None"
                disx = 0
                disy = 0
                self.running = False
                timedout = False
               # self.join() 
                if flag==True:
                    rc_i2c2.end_reading()
                    flag = False
                break

        #    c.release()
        except KeyboardInterrupt:
            self.running = False
            println("Exit!")

        except Exception as ex:
            print("Error in thread A:" , ex)
           # self.join()   

    def change(self,dx,dy,x,y ):
        global dirx, diry, disx,disy
        dirx = dx
        diry = dy
        disx = x
        disy = y


class Thread_B(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.running = True
        rc_i2c2.begin_reading()
        rc_i2c2.get_volt_and_distance()
        rc_i2c2.end_reading()
        print(name , " created")
    def stop(self):
        self.running = False
#        self.join()
        print("Stopping thread B!")
    def registerIP(self,p):
        global ip
        ip = p
        print("Client is alive at " , ip)
    def signal(self):
        signal = int(100 - (float(ping.do_one(ip,2))*500))
        
        return signal
 

    def run(self):
        global flag
        global distance    #made global here
        global voltage
        global pingtime
        interval = 0 
        ping_array = [0.01,0.01,0.01] #default 
        ping_time_out = 1
        global timedout
        global crashing
        crashing = False 
        self.running = True
        try:
            while self.running:
                p = 0
                ping_time_out = 1
 
                if(interval%10==0):               
                    try:
             #  c.acquire()
                        #rc_i2c2.begin_reading()
                        result = rc_i2c2.get_volt_and_distance()
                        #rc_i2c2.end_reading()

                        voltage = float(result[0])
                        d = int(result[1])
                        print(str(voltage),"v" , str(d),"cm")
                   #               # c.notify_all()
                    except:
                        pass
                interval+=1
                try:
                    pingtime = float(ping.do_one(ip,2))
                except Exception as a:
                    pingtime = 1
                    interval=0
                    print("error:",a)
                del ping_array[0]
                ping_array.append(pingtime)
                print(ip , ": ", pingtime , " second")
                time.sleep(1)
#                    print(ping_array)
                              #record the pings, then decide after 3 times of time out in a row
                for i in range(len(ping_array)):
    #a = rc_thread.Thread_A("myThread_name_A")
                    p = 0
                    if(ping_array[i]>=1):
                        p = 1
                    else:
                        p = 0
                    ping_time_out = int(ping_time_out * p)
                #print("Result: " , str(ping_time_out), " " , str(p))
                if(ping_time_out==1):
                    print("PING OUT!", str(ping_array))
                    timedout=True
                    self.stop()
#                    self.join()
                    break    
        except KeyboardInterrupt:
            print("exit")
            self.stop()
 #           self.join()
            self.running = False
            #c.release()

    def getvoltage(self):
        global voltage
        return voltage

    def getdistance(self):
        global distance
        return distance

if(__name__=="__main__"):
 a = Thread_A("myThread_name_A")
 b = Thread_B("myThread_name_B")

 b.start()
 a.start()

 a.join()
 b.join()
