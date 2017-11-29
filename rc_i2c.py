from smbus2 import SMBus
import time
import array

bus = SMBus(1)
SLAVE_ADDRESS = 0x40
data = ''

def request_reading():
    data = ''
    voltage = 0.0
    distance = 0.0
    try:
     data0 = bus.read_i2c_block_data(SLAVE_ADDRESS, 0,8)
     data0 = array.array('B',data0).tostring()
     x = str(data0,'utf-8')
     voltage , distance = x.split(",")
     print("V = " , voltage)
     print("D = " , distance)
    except Exception as s: 
     print("Error",s)

    return [voltage, distance]

def read_others():
    command = input("Enter command: l - toggle LED, r - read A0 ")
    if command == 'l' :
        bus.write_byte(SLAVE_ADDRESS, ord('l'))
    elif command == 'r' :
        request_reading()
    elif command == 'd':
        bus.write_byte(SLAVE_ADDRESS, ord('d'))
        data = bus.read_i2c_block_data(SLAVE_ADDRESS, 0, 4)
        data = array.array('B',data).tostring()
        print (str(data,'utf-8'))

if(__name__=="__main__"):
    result = request_reading()
    print("Current distance is: " , result[1])
