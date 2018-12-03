# Basic UDP server
# Receives 3 1-byte integers, adds them, and returns the 1-byte result.
import socket

port = 10010

# Create the socket object using DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the port. Using "" for the interface so it binds to
# all known interfaces, including "localhost".
s.bind( ("", port) )

# Servers stay open -- they handle a client, then loop back
# to wait for another client.
while True:

    # wait for a client to send a packet
    packet, addr = s.recvfrom(1024)
    
    # unpack the data. In this case we're just using
    # each byte as an integer.
    one = packet[0]
    two = packet[1]
    three = packet[2]
    
    # Calculate the result.
    result = one + two + three
    
    # Pack the result into a 1-element byte array.
    packet = bytearray()
    packet.append(result)
    
    # Send the packet back to the client.
    s.sendto(packet, addr)
