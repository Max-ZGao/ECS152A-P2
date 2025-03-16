
import dataclasses
import socket
import struct
import sys
import time
import os

# constants
PORT_NUM = 8081
DEST_ADDR = "0.0.0.0"
DEST_PORT = 5001
TIMEOUT = 5  # in sec
PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE

@dataclasses.dataclass
class Packet:
    seq_id: int

# start measuring send time
send_time = time.time()

# create socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create a socket with IPV4(AF_INET) and UDP (SOCK_DGRAM)
# set timeout
client.settimeout(TIMEOUT)

dest = (DEST_ADDR, DEST_PORT)

# Generate packets
packets_to_send = []
with open('file.mp3', 'rb') as f: # read in mp3 
    numpacketsNeed = os.path.getsize("file.mp3") // MESSAGE_SIZE
    print(numpacketsNeed)
    print(os.path.getsize("file.mp3"))
    for i in range(numpacketsNeed):
        seq_id = Packet(i)
        nPacket = struct.pack("I", *(Packet.astuple(seq_id))) + f.read(MESSAGE_SIZE)
        packets_to_send.append(nPacket)

def create_acknowledgement(seq_id, message):
    return int.to_bytes(seq_id, SEQ_ID_SIZE, signed=True, byteorder='big') + message.encode()


acknowledgement = create_acknowledgement(packets_to_send, 'ack')

print(acknowledgement.decode())

"""
# send payload in chunks
totalPacketDelay = 0
chunk_size = 1024
for packet in packets_to_send:
    ackEd = False
    per_packet_send = time.time()
    while(ackEd == False):
        client.sendto(packet, dest)
        # receive server response
        try:
            response = client.recvfrom(1024)
            throughput = response.decode()
            
            if()
            ackEd = True
        except socket.timeout:
            print("Server response timed out. Resending")
    per_packet_recv = time.time()
    per_packet_rtt = per_packet_recv - per_packet_send
    totalPacketDelay += per_packet_rtt

client.close()
"""



""" For testing packet segmentation
with open('file2.mp3', 'wb') as f:
    for i in range(numpacketsNeed):
        print(f'writing {packets_to_send[i].seq_id}')
        if(i == 0):
            print(packets_to_send[i].message)
        f.write(packets_to_send[i].message)
"""