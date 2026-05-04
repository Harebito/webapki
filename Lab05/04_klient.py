import socket
import time

def start_comparison_client():
    host = '127.0.0.1'
    data = b"X" * (1024 * 1024) # 1 MB danych

    # --- Wysyłka TCP ---
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp:
        s_tcp.connect((host, 3000))
        s_tcp.sendall(data)
        print("Wysłano dane przez TCP")

    time.sleep(1) # Przerwa między testami

    # --- Wysyłka UDP ---
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_udp:
        chunk_size = 4096
        for i in range(0, len(data), chunk_size):
            s_udp.sendto(data[i:i+chunk_size], (host, 3001))
        print("Wysłano dane przez UDP")

if __name__ == "__main__":
    start_comparison_client()
