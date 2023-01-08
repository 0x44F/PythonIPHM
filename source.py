import socket
import struct

class PacketSender:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

    def modify_ip_header(self, packet, src_addr):
        # unpack the IP header
        ip_header = packet[:20]
        ip_header = struct.unpack("!BBHHHBBH4s4s", ip_header)

        # modify the source address
        ip_header = list(ip_header)
        ip_header[8] = 0
        ip_header[9] = 0
        ip_header[10] = src_addr & 0xff
        ip_header[11] = (src_addr >> 8) & 0xff
        ip_header[12] = (src_addr >> 16) & 0xff
        ip_header[13] = (src_addr >> 24) & 0xff
        ip_header = tuple(ip_header)

        # pack the modified IP header
        modified_ip_header = struct.pack("!BBHHHBBH4s4s", *ip_header)

        # rebuild the packet with the modified IP header
        modified_packet = modified_ip_header + packet[20:]

        return modified_packet

    def send_packet(self, packet, src_addr, dst_addr, dst_port):
        # bind the socket to the desired source address
        self.s.bind((src_addr, 0))

        # modify the IP header
        packet = self.modify_ip_header(packet, src_addr)

        # send the packet
        self.s.sendto(packet, (dst_addr, dst_port))

# test the API
packet_sender = PacketSender()
packet = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
src_addr = "1.2.3.4"
dst_addr = "5.6.7.8"
dst_port = 80
packet_sender.send_packet(packet, src_addr, dst_addr, dst_port)
