6041268# To-do list

(A) make_pkt(ext_seq, data, check) +main
    - add header + ext_seq
    - return packet
(A) udt_send(rcvpacket) +main
    - self.sock.sendto(msg[total_sent:total_sent + self.buffer_size], destination)
(A) isACK(rcvpacket, seq) +main
    - 00
(A) start_timer +main @timer
(A) stop_timer +main @timer
