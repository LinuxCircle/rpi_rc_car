
from smbus2 import SMBusWrapper
import time

SLAVE_ADDRESS = 0x40

def begin_reading():
    print("begin!")
    with SMBusWrapper(1) as bus:
        try:
            bus.write_byte(SLAVE_ADDRESS, ord('b'))
        except:
            print("error begining")
def end_reading():
    print("end")
    with SMBusWrapper(1) as bus:
        try:
            bus.write_byte(SLAVE_ADDRESS, ord('e'))
        except:
            print("error ending")

def get_volt_and_distance():
    with SMBusWrapper(1) as bus:
    # Read a block of 16 bytes from address 80, offset 0
        v = 0
        d = 100 
        try:   
            block = bus.read_i2c_block_data(SLAVE_ADDRESS, 0, 8)
        # Returned value is a list of 16 bytes
        
            block_bytes= bytes(block)
            block_string = block_bytes.decode()
            #time.sleep(0.1)
            v,d = block_string.split(',')
        except Exception as a:
            print("error reading i2c" , a)
            pass
        return [v,d]

if(__name__=="__main__"):
	su = get_volt_and_distance()
	print(su)
