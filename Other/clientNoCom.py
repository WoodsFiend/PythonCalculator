# Curtis Naples
# C0457101
# Network Programming - Lab 2

import socket, sys, os, subprocess

#function used to iteravely top-down search directory for server.py file location
def search_files(directory='./'):
    for dirpath, dirnames, files in os.walk(directory):
        #print(files)
        for name in files:
            if name == 'server.py':
                return ("\""+dirpath + '\\' + name + "\"")
                #print(name)
    return("NF")
#function used to check if int or not
def is_number():
    try:
        int(sys.argv[4])
        return True
    except ValueError:
        return False
    except IndexError:
        return True
host = sys.argv[1]
#checks that the port number is valid
try:
    port = int(sys.argv[2])
except ValueError:
    print()
    print('\tInvalid Port Number')
    print('\t Please Try Again')
    sys.exit()
# 1. create the socket using DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3.1)
try:
    s.connect((host, port))
except socket.gaierror as e:
    print()
    print('\tConnection To Host Failed')
    print('\t    Check  Host/Port')
    print('\t    Please Try Again')
    sys.exit()
#get the number of arguments and create bytearray
numberArgs = len(sys.argv)-4

#initialize byte arrray to hold operator and amount of numbers
packet = bytearray(2)

#assign operator packet
#ADD
if sys.argv[3] == '+':
    packet[0] = 1
#SUBTRACT
elif sys.argv[3] == '-':
    packet[0] = 2
#MULTIPLY
elif sys.argv[3] == '*':
    packet[0] = 4

#used to close and print server calculations
elif sys.argv[3] == 'exit':
    packet[0] = 8
    s.send(packet)
    print()
    print('\tServer Exited/Calculations Printed')
    print()
    sys.exit()

#used to start the server from client ------------Can Send Server Directory as next arguement----Recursively Searches for server.py
elif sys.argv[3] == 'start':
    #if arg 4 is string it searches that directory for server.py
    if is_number() == False:
        value = str(sys.argv[4])
        #print(search_files(sys.argv[4]))
        file = search_files(sys.argv[4])
        #print(sys.argv[4])
        #print(file)
        #file was found
        if file != "NF":
            subprocess.Popen('python '+ file + ' ' + sys.argv[2])
            print()
            print("\t Server Started From Given Directory")
            print('   ' + file)
            print("\t        Send Calculations")
        #file not found
        else:
            print()
            print("\t File Not Found In Given Directory")
            print("\t       Or Any Subdirectories")

    #defaults to check client directory for file  
    else:
        #starts the server if it is within same folder as client
        try:
            subprocess.Popen('python server.py ' + sys.argv[2])
            print()
            print("\t Server Started From Client Directory")
            print("\t        Send Calculations")
        #server.py couldnt be started
        except:
            print()
            print("\t File Not Found In Client Directory")

    sys.exit()
#indicates an invalid operator was used
else:
    print()
    print('\tInvalid Operator')
    print('\t       ' + sys.argv[3])
    print('\tPlease Try Again')
    sys.exit()

#checks that there is 2 or more operands
if numberArgs < 2:
    print()
    print('\tNot Enough Numbers')
    print('\t Please Try Again')
    sys.exit()

#assign amount of numbers packet
packet[1] = numberArgs

#loop to check that all values are valid
count = 3
while count != len(sys.argv)-1:
    count = count + 1
    try:
        if ((int(sys.argv[count]) < 0) or (int(sys.argv[count]) > 15)):
            print()
            print("\t\tInvalid Number")
            print('\t\t      ' + sys.argv[count])
            print("\t Must Use Positive Integers 0-15")
            print('\t\tPlease Try Again')
            sys.exit()
    except ValueError:
        print()
        print("\t\t Invalid Number")
        print('\t\t      ' + sys.argv[count])
        print("\t Must Use Positive Integers 0-15")
        print('\t\tPlease Try Again')
        sys.exit()
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
except Exception as e:
    print()
    print("\t  Connection Timeout")
    print("\tResult Could Be Too Big")
    print("\t\t Or")
    print("\t Host/Port Incorrect")
    print("\t    Check Server")
    sys.exit()
# 5. unpack the byte array to a meaningful value.
#checks if the operation was a subtraction and if the result needs to be negative
if (sys.argv[3] == '-') and (int.from_bytes(data, byteorder='big') > int(sys.argv[4])):
    #print()
    print(int.from_bytes(data, byteorder='big', signed=True))
    
else:
    #print()
    print(int.from_bytes(data, byteorder='big'))
    
