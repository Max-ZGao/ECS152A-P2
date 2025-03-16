import socket
import struct
import time
import os
from collections import deque

PORT_NUM = 8081
DEST_ADDR = "127.0.0.1"
DEST_PORT = 5001
TIMEOUT = 1
PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
WINDOW_SIZE = 100  #  window size


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
client.settimeout(TIMEOUT)

dest = (DEST_ADDR, DEST_PORT)

#  packets
packets_to_send = []
with open('file.mp3', 'rb') as f:  
    numpacketsNeed = (os.path.getsize("file.mp3") + MESSAGE_SIZE - 1) // MESSAGE_SIZE
    for i in range(numpacketsNeed):
        nPacket = struct.pack("I", i) + f.read(MESSAGE_SIZE)  # sequence ID and data
        packets_to_send.append(nPacket)




base = 0  # base of the window
next_seq_num = 0  # next sequence number to send
window = []

# send packets in the window
def send_packets_in_window():
    global next_seq_num
    while next_seq_num < numpacketsNeed and next_seq_num < base + WINDOW_SIZE:
        packet = packets_to_send[next_seq_num]
        client.sendto(packet, dest)
         # packet send time
        window.append((next_seq_num, time.time())) 
        next_seq_num += 1


while base < numpacketsNeed:
    # TODO:  sliding window logic
    send_packets_in_window()
    try:
        data, addr = client.recvfrom(1024)
        ack = struct.unpack("I", data)[0]
        while window and window[0][0] <= ack:
            send_time = window[0][1] 
            recv_time = time.time() 
            totalPacketDelay += recv_time - send_time 
            window.pop(0) 
            base += 1
    except socket.timeout:
        
    pass

recv_time = None 
send_time = None 
totalPacketDelay = None

rtt = recv_time - send_time
throughput = os.path.getsize("file.mp3") / rtt 
perPackDelay = totalPacketDelay / numpacketsNeed 
metric = 0.3 * (throughput / 1000) + (0.7 / perPackDelay)  



client.close()