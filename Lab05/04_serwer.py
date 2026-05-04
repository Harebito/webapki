import socket
import time

def start_comparison_server():
    host = '127.0.0.1'
    port_tcp = 3000
    port_udp = 3001
    data_size = 1024 * 1024  # 1 MB

    # --- TEST TCP ---
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp:
        s_tcp.bind((host, port_tcp))
        s_tcp.listen(1)
        print("Serwer TCP czeka...")
        conn, addr = s_tcp.accept()
        with conn:
            start_time = time.time()
            received = 0
            while received < data_size:
                data = conn.recv(4096)
                if not data: break
                received += len(data)
            end_time = time.time()
            print(f"TCP: Odebrano {received} bajtów w {end_time - start_time:.4f}s")

    # --- TEST UDP ---
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_udp:
        s_udp.bind((host, port_udp))
        print("Serwer UDP czeka na pierwszy pakiet...")
        received = 0
        first_packet = True
        while received < data_size:
            data, addr = s_udp.recvfrom(4096)
            if first_packet:
                start_time = time.time()
                first_packet = False
            received += len(data)
        end_time = time.time()
        print(f"UDP: Odebrano {received} bajtów w {end_time - start_time:.4f}s")

if __name__ == "__main__":
    start_comparison_server()
