# Curtis Naples
# C0457101
# Network Programming - Lab 2

import socket, sys

host = sys.argv[1]
#checks that the port number is valid
try:
    port = int(sys.argv[2])
except ValueError:
    print()
    print('Invalid Port Number')
    print('Please Try Again')
    sys.exit()
# 1. create the socket using DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3.1)
s.connect((host, port))

#get the number of arguments and create bytearray
numberArgs = len(sys.argv)-4

#initialize byte arrray to hold operator and amount of numbers
packet = bytearray(2)

#assign operator packet
if sys.argv[3] == '+':
    packet[0] = 1
elif sys.argv[3] == '-':
    packet[0] = 2
elif sys.argv[3] == '*':
    packet[0] = 4
#used to exit and error check server
elif sys.argv[3] == 'b':
    packet[0] = 8
    s.send(packet)
    print()
    print('Server Closed/Calculations Printed')
    sys.exit()
#indicates an invalid operator was used
else:
    print()
    print('Invalid Operator')
    print('Please Try Again')
    sys.exit()

#checks that there is 2 or more operands
if numberArgs < 2:
    print()
    print('Not Enough Operands')
    print('Please Try Again')
    sys.exit()

#assign amount of numbers packet
packet[1] = numberArgs

#print('Operator: ' + str(packet[0]))
#print('Number of ARGS: ' + str(packet[1]))

#starting arguement index
index2 = 4
#starting packet index
index = 2

# 2. build the packet.
while index2 != len(sys.argv):
    #adds an empty slot to the packet
    packet.append(0)
    #gets first arguement
    packet[index] = int(sys.argv[index2])
    #print('binary data: ')
    #print(bin(packet[index]))
    
    index2 = index2 + 1
    #shifts the first integers bits 4 to left
    packet[index] = int(packet[index]) << 4
    
    #checks if a next arguement exists
    try: 
    	#concatenates the two bitstrings into one byte
    	packet[index] = int(packet[index]) | int(sys.argv[index2])
    	#print('combined bits = ' + bin(packet[index]))
    
    #index error when there is an odd number of arguements forces break
    except IndexError:
    	break

    index2 = index2 + 1
    index = index + 1

# 3. send the packet. 
s.send(packet)

# 4. receive the response
try:
    data = s.recv(32)
except:
    print()
    print(" Connection Timed Out")
    print("Result Could Be Too Big")
    print("\t Or")
    print(" Host/Port Incorrect")
    sys.exit()
# 5. unpack the byte array to a meaningful value.
#checks if the operation was a subtraction and if the result needs to be negative
if (sys.argv[3] == '-') and (int.from_bytes(data, byteorder='big') > int(sys.argv[4])):
    print()
    print(int.from_bytes(data, byteorder='big', signed=True))
    
else:
    print()
    print(int.from_bytes(data, byteorder='big'))
    
