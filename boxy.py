import getopt
import sys
import time

from relay import status
from relay import tcp
from relay import udp

relayport = 0
remoteport = 0 
remoteaddress = ""
protocol = "UDP"

help = "Invalid arguments, usage:\nboxy.py -i <input port> -p <remote port> -a <remote address> [-t]"

def quit():
	print("Quitting...")

	if (protocol == "UDP"):
		udp.stop()
	else:
		tcp.stop()

	exit(0)

#process args
try:
	options, args = getopt.getopt(sys.argv[1:], "i:p:a:t")
except getopt.GetoptError:
	print(help)
	sys.exit(2)

try:
	for option, arg in options:
		if (option == "-i"):
			relayport = int(arg)
		elif (option == "-p"):
			remoteport = int(arg)
		elif (option == "-a"):
			remoteaddress = arg
		elif (option == "-t"):
			protocol = "TCP"
except ValueError:
	print(help)
	sys.exit(2)

if ((0 < relayport <= 65535 and 0 < remoteport <= 65535 and remoteaddress != "") == False):
	print(help)
	sys.exit(2)

print("Relay starting on port {0}, relaying {1} to {2}:{3}".format(relayport, protocol, remoteaddress, remoteport))

if (protocol == "UDP"):
	udp.start(relayport, remoteaddress, remoteport)
else:
	tcp.start(relayport, remoteaddress, remoteport)
status.start(relayport, remoteaddress, remoteport)

try:
	while True:
		time.sleep(3600)
except KeyboardInterrupt:
	quit()
except EOFError:
	#this exception is raised when ctrl-c is used to close the application on Windows, appears to be thrown twice?
	try:
		quit()
	except KeyboardInterrupt:
		exit(0)
