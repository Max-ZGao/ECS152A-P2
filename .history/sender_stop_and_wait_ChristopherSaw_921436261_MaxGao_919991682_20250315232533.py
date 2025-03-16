
import dataclasses
import socket
import struct
import sys
import time
import os

# constants
PORT_NUM = 8081
DEST_ADDR = "127.0.0.1"
DEST_PORT = 5001
TIMEOUT = 1  # in sec
PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE

@dataclasses.dataclass
class Packet:
    seq_id: int



dest = (DEST_ADDR, DEST_PORT)

# Generate packets
packets_to_send = []
with open('file.mp3', 'rb') as f: # read in mp3 
    numpacketsNeed = os.path.getsize("file.mp3") // MESSAGE_SIZE
    for i in range(numpacketsNeed):

        nPacket = struct.pack("I", (i)) + f.read(MESSAGE_SIZE)
        packets_to_send.append(nPacket)

# start measuring send time
send_time = time.time()

# create socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create a socket with IPV4(AF_INET) and UDP (SOCK_DGRAM)
# set timeout
client.settimeout(TIMEOUT)

# send payload in chunks
totalPacketDelay = 0
chunk_size = 1024
counter = 0

for packet in packets_to_send:
    ackEd = False
    per_packet_send = time.time()
    while(ackEd == False):

        try:
            client.sendto(packet, dest)
            # receive server response
            # print(f"trying to recieve {counter}")
            ack, _ = client.recvfrom(PACKET_SIZE)
            seq_id = ack[:SEQ_ID_SIZE] 
            id = int.from_bytes(seq_id, signed=True, byteorder='big')
            if(id == counter):
                ackEd = True
                counter += 1
                if(id == numpacketsNeed - 1): # last ack recieved mark down recv time
                    recv_time = time.time()
        except socket.timeout:
            print("Server response timed out. Resending")
        
    per_packet_recv = time.time()
    per_packet_rtt = per_packet_recv - per_packet_send
    totalPacketDelay += per_packet_rtt

# print statistics
rtt = recv_time - send_time
throughput = rtt / os.path.getsize("file.mp3")
perPackDelay = totalPacketDelay / numpacketsNeed
metric = 0.3 * (throughput / 1000) + (0.7 / perPackDelay)

print(f'Throughput: {throughput:7f},')
print(f'Average packet delay: {perPackDelay:7f},')
print(f'Metric: {metric:7f}')
client.close()




""" For testing packet segmentation
with open('file2.mp3', 'wb') as f:
    for i in range(numpacketsNeed):
        print(f'writing {packets_to_send[i].seq_id}')
        if(i == 0):
            print(packets_to_send[i].message)
        f.write(packets_to_send[i].message)
"""