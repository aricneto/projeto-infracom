# To-do list

(A) make_pkt(ext_seq, data, check) +main {cm:2023-09-04}
    - add header + ext_seq {cm:2023-09-04}
    - return packet {cm:2023-09-04}
(A) udt_send(rcvpacket) +main {cm:2023-09-04}
(A) isACK(rcvpacket, seq) +main {cm:2023-09-04}
(A) start_timer +main @timer {cm:2023-09-04}
(A) stop_timer +main @timer {cm:2023-09-04}
(B) each address should have its own seq counter {cm:2023-09-04}