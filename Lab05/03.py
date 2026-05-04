import socket
import time

def solve_port_knocking():
    target_ip = "212.182.24.27"
    tcp_port = 2913
    ping_msg = b"PING"
    
    print(f"--- Faza 1: Szukanie portów UDP (kończących się na 666) ---")
    valid_udp_ports = []
    
    # Przeszukujemy porty UDP kończące się na 666 (np. 666, 1666, 2666...)
    for port in range(666, 65536, 1000):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
            udp_sock.settimeout(0.5) # Krótki timeout dla szybkości skanowania
            try:
                udp_sock.sendto(ping_msg, (target_ip, port))
                data, _ = udp_sock.recvfrom(1024)
                
                if b"PONG" in data:
                    print(f"[+] Znaleziono port UDP: {port}")
                    valid_udp_ports.append(port)
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Błąd na porcie {port}: {e}")

    if not valid_udp_ports:
        print("Nie znaleziono żadnych portów UDP. Czy serwer jest dostępny?")
        return

    print(f"\n--- Faza 2: Port Knocking (Sekwencja: {valid_udp_ports}) ---")
    # Wysyłamy pakiety UDP w znalezionej kolejności
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as knocker:
        for p in valid_udp_ports:
            print(f"Pukanie do portu UDP: {p}")
            knocker.sendto(ping_msg, (target_ip, p))
            time.sleep(0.2) # Krótka przerwa między pukanie, by serwer przetworzył kolejność

    print(f"\n--- Faza 3: Próba połączenia z ukrytą usługą TCP na porcie {tcp_port} ---")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
            tcp_sock.settimeout(5.0)
            tcp_sock.connect((target_ip, tcp_port))
            
            # Odbieranie gratulacji
            response = tcp_sock.recv(1024).decode('utf-8')
            print(f"Wiadomość od serwera: {response}")
            
    except ConnectionRefusedError:
        print("Błąd: Port TCP nadal zamknięty. Spróbuj zmienić kolejność pukania lub zwiększyć odstępy.")
    except Exception as e:
        print(f"Wystąpił błąd podczas łączenia z TCP: {e}")

if __name__ == "__main__":
    solve_port_knocking()
