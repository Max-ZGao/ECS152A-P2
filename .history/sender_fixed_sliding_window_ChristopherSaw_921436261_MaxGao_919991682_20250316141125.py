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
WINDOW_SIZE = 100  

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
client.settimeout(TIMEOUT)
dest = (DEST_ADDR, DEST_PORT)

packets_to_send = []
with open('file.mp3', 'rb') as f:  
    numpacketsNeed = (os.path.getsize("file.mp3") + MESSAGE_SIZE - 1) // MESSAGE_SIZE
    for i in range(numpacketsNeed):
        nPacket = struct.pack("I", i) + f.read(MESSAGE_SIZE) 
        packets_to_send.append(nPacket)


base = 0 
 # next sequence number to send
next_seq_num = 0 
window = [] 
acks_received = [False] * numpacketsNeed  # Track acknowledgments
totalPacketDelay = 0  # Total delay for all packets
recv_time = None  # Time when the last acknowledgment is received

# Function to send packets in the window
def send_packets_in_window():
    global next_seq_num
    while next_seq_num < numpacketsNeed and next_seq_num < base + WINDOW_SIZE:
        packet = packets_to_send[next_seq_num]
        client.sendto(packet, dest)
        window.append((next_seq_num, time.time()))  # Track packet send time
        next_seq_num += 1


send_time = time.time()

while base < numpacketsNeed:
    send_packets_in_window()

    try:   
        #print("Getting ACK")
        ack, _ = client.recvfrom(PACKET_SIZE)
        seq_id = ack[:SEQ_ID_SIZE]
        ack_id = int.from_bytes(seq_id, signed=True, byteorder='big')

        if base <= ack_id < base + WINDOW_SIZE:
            acks_received[ack_id] = True
            print(f"Received ACK {ack_id}")
            for i in range(len(window)):
                if window[i][0] == ack_id:
                    send_time_packet = window[i][1]
                    per_packet_rtt = time.time() - send_time_packet
                    totalPacketDelay += per_packet_rtt
                    break

            while base < numpacketsNeed and acks_received[base]:
                base += 1

            if base == numpacketsNeed:
                #print("done")
                recv_time = time.time()

    except socket.timeout:
        print("Timeout")
        next_seq_num = base
        window.clear()

rtt = recv_time - send_time
print(f'RTT: {rtt:.7f},')
throughput = os.path.getsize("file.mp3") / rtt 
print(f'Throughput: {throughput:.7f},')
perPackDelay = totalPacketDelay / numpacketsNeed  
print(f'Throughput: {throughput:.7f},')
metric = 0.3 * (throughput / 1000) + (0.7 / perPackDelay)  
print(f'Throughput: {throughput:7f},')

client.close()