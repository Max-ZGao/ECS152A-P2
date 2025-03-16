import socket
import struct
import time
import os
from collections import deque

PORT_NUM = 8081
DEST_ADDR = "127.0.0.1"
DEST_PORT = 5001
TIMEOUT = 1  # in seconds
PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
WINDOW_SIZE = 100  # Fixed window size

# Create socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPv4, UDP
client.settimeout(TIMEOUT)

dest = (DEST_ADDR, DEST_PORT)

# Generate packets
packets_to_send = []
with open('file.mp3', 'rb') as f:  # Read the file
    numpacketsNeed = (os.path.getsize("file.mp3") + MESSAGE_SIZE - 1) // MESSAGE_SIZE
    for i in range(numpacketsNeed):
        nPacket = struct.pack("I", i) + f.read(MESSAGE_SIZE)  # Pack sequence ID and data
        packets_to_send.append(nPacket)

# Add a FIN packet to signal end of transmission
fin_packet = struct.pack("I", numpacketsNeed) + b'==FINACK=='
packets_to_send.append(fin_packet)
numpacketsNeed += 1

# Sliding window variables
base = 0  # Base of the window
next_seq_num = 0  # Next sequence number to send
window = deque()  # Queue to track packets in the window
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

# Main loop
while base < numpacketsNeed:
    # Send packets in the window
    send_packets_in_window()

    # Wait for acknowledgments
    try:
        ack, _ = client.recvfrom(PACKET_SIZE)
        seq_id = ack[:SEQ_ID_SIZE]
        ack_id = int.from_bytes(seq_id, signed=True, byteorder='big')

        if base <= ack_id < base + WINDOW_SIZE:
            acks_received[ack_id] = True
            # Calculate per-packet delay
            for i in range(len(window)):
                if window[i][0] == ack_id:
                    send_time_packet = window[i][1]
                    per_packet_rtt = time.time() - send_time_packet
                    totalPacketDelay += per_packet_rtt
                    break

            # Slide the window forward
            while base < numpacketsNeed and acks_received[base]:
                base += 1

            # If all packets are acknowledged, stop the timer
            if base == numpacketsNeed:
                recv_time = time.time()

    except socket.timeout:
        # Resend all packets in the window
        print("Timeout")
        next_seq_num = base
        window.clear()
        
send_time = window[0][1]  # Start time is the time of the first packet sent
# Calculate statistics
rtt = recv_time - send_time
throughput = os.path.getsize("file.mp3") / rtt  # Throughput in bytes per second
perPackDelay = totalPacketDelay / numpacketsNeed  # Average per-packet delay
metric = 0.3 * (throughput / 1000) + (0.7 / perPackDelay)  # Performance metric

# Output results
print(f"{throughput:.7f}, {perPackDelay:.7f}, {metric:.7f}")

# Close the socket
client.close()