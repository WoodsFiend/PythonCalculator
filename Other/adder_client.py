# Basic UDP Client
# Sends 3 1-byte integers to the server. Receives a 1-byte response
# and prints it (in base-10).
import socket, sys

host = "localhost"
port = 10010

# 1. create the socket using DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. build the packet.
packet = bytearray(3)
packet[0] = int(sys.argv[1])
packet[1] = int(sys.argv[2])
packet[2] = int(sys.argv[3])

# 3. send the packet. 
s.sendto(packet, (host, port))

# Note, you can also do:
# s.connect( (host, port) )
# s.send(packet)

# 4. receive the response
data = s.recv(1)

# 5. unpack the byte array to a meaningful value.
#    In this case, it's just one byte that is an integer.
value = data[0]
print(value)
