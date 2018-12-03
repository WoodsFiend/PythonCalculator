# Curtis Naples
# C0457101
# Network Programming - Lab 2

import socket, math, sys

#gets the port from arguement
port = int(sys.argv[1])

# Create the socket object using DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the port. Using "" for the interface so it binds to
# all known interfaces, including "localhost".
s.bind( ("", port) )

# Servers stay open -- they handle a client, then loop back
# to wait for another client.
theCount = 1
while True:

    # wait for a client to send a packet
    packet, addr = s.recvfrom(1024)
    #get operator
    operator = packet[0]
    #print(operator)
    if operator != 8:
        print(' ' + str(theCount) + '.  Calculation of '  + str(packet[1]) + ' Numbers')
    
    #ADDITION
    if operator == 1:
        result = 0
        index = 2

        #loop through integers and add them
        #index-2 <= (math.ceil((packet[1])/2)-1)
        while index != len(packet):
            #import pdb
            #pdb.set_trace()
            #print(bin(packet[index]))
            #splits up a single byte into 2 unsigned 4 bit integers
            first = int(format(packet[index],'#010b')[2:6],2)
            second = int(format(packet[index],'#010b')[6:],2)

            if (packet[1]%2) != 0 and (index == len(packet)-1):
                result = result + first
                print('\t' + str(first) + ' = ' + str(result))
            #all other multiplications done here
            else:
                result = (result + first + second)
                print('\t' + str(first) + ' + ' + str(second) + ' = ' + str(result) + ' +')
            index = index + 1

    #SUBTRACTION
    elif operator == 2:
        result = 0
        index = 2

        #loop through integers and subtract them
        while index != len(packet):
            #import pdb
            #pdb.set_trace()
            #print(bin(packet[index]))
            #splits up a single byte into 2 unsigned 4 bit integers
            first = int(format(packet[index],'#010b')[2:6],2)
            second = int(format(packet[index],'#010b')[6:],2)
            
            #checks if its the first byte and subtracts accordingly
            if index == 2:
                result = first - second
            #all other subtractions
            else:
                result = (result - first) - second
            print('\t' + str(first) + ' - ' + str(second) + ' = ' + str(result) + ' -')
            index = index + 1

    #MULTIPLICATION
    elif operator == 4:
        result = 0
        index = 2

        #loop through integers and add them
        while index != len(packet):
            #import pdb
            #pdb.set_trace()
            #print(bin(packet[index]))
            #splits up a single byte into 2 unsigned 4 bit integers
            first = int(format(packet[index],'#010b')[2:6],2)
            second = int(format(packet[index],'#010b')[6:],2)
            
            #checks if its the first byte and multiplies accordingly
            if index == 2:
                result = first * second
                print('\t' + str(first) + ' * ' + str(second) + ' = ' + str(result) + ' *')
            
            #checks if its the last and multiplies accordingly
            elif (packet[1]%2) != 0 and (index == len(packet)-1):
                result = result * first
                print('\t' + str(first) + ' = ' + str(result))
            #all other multiplications done here
            else:
                result = (result * first) * second
                print('\t' + str(first) + ' * ' + str(second) + ' = ' + str(result) + ' *')
            index = index + 1
    
    #---------------------------Client closes Server SENT OPERATOR = exit --------------------------------
    elif operator == 8:
        print('\t\tClient Closed Server')
        s.close()
        break
    #Error Check client sent invalid operator
    else:
        print()
        print("\tInvalid Operator")
        s.close()
        break
    # Pack the result into a 32 bit signed byte array that is big-endian.
    try:
        #Negative result
        if result < 0:
            result = result.to_bytes(4, byteorder='big', signed=True)
        #Positive result
        else:
            result = result.to_bytes(4, byteorder='big')

        print()
        packet = bytearray()
        i=0

        #appends the signed integer to the packet
        while i < len(result):
            #print(result[i])
            packet.append(result[i])
            i = i + 1
        # Send the packet back to the client.
        s.sendto(packet, addr)
        theCount = theCount + 1
    except OverflowError:
        print('\tThe result is too large to send to the client in 4 bytes')
        break
    
    
    

    