
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
    message: int

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
        nPacket = Packet(i, f.read(MESSAGE_SIZE))
        packets_to_send.append(nPacket)

print(packets_to_send.__sizeof__())

with open('file2.mp3', 'wb') as f:
    for i in range(numpacketsNeed):
        print(f'writing {packets_to_send[i].seq_id}')
        if(i == 0):
            print(packets_to_send[i].message)
        f.write(packets_to_send[i].message)
"""
# send header packet
header_sent = False
while not header_sent:
    try:
        client.sendto(header_packet, dest)
        print("Header packet sent:", header)

        # acknowledgment from the server
        ack, _ = client.recvfrom(1024)
        if ack.decode() == "Header Recieved":
            print("Header packet acknowledged by server.")
            header_sent = True
    except socket.timeout:
        print("Header packet lost, restarting...")
        continue

# send payload in chunks
chunk_size = 1024
for i in range(0, len(payload), chunk_size):
    chunk = payload[i:i + chunk_size] 
    client.sendto(chunk, dest)
    

# receive server response
try:
    response, server_address = client.recvfrom(1024)
    throughput = response.decode()
    print(f"Server response received from {server_address}:")
    print(f"Throughput: {throughput} KB/s")
except socket.timeout:
    print("Server response timed out. Data may have been lost.")

client.close()"
"""