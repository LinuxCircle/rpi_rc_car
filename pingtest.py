import ping

# delay = ping.do_one(dest_addr, timeout)

#pings github.com with a 2s timeout and returns the delay
delay = ping.do_one('192.168.200.5', 1)

def average(address, count=2):
	average = 0
	delay = 0

	for i in range(count):
		try:
			delay = float(ping.do_one(address,1))
		except:
			delay = 1
		average += delay
	average = average / count
	print(average)
	return average

if __name__=="__main__":
	average('192.168.200.4')
