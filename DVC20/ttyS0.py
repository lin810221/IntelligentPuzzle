import serial
import sys

cage = []
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Usage: uart_test.py <RS232 COMPORT>')
		sys.exit(-1)
		
	ComPort=sys.argv[1]
	mySerial = serial.Serial(ComPort, 115200, timeout=1)	
	
	for num in range(1):
		sendData=bytes([num])
		result=mySerial.write(sendData)
		recvData=mySerial.readline()
		if sendData!=recvData:
			print('Fail')
			sys.exit(-1)
#		print('Test')
	
	print('Pass')

	sys.exit(0)
