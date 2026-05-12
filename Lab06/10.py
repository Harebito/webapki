import socket

def main():
    host = '127.0.0.1'
    port = 2525  # Używamy portu powyżej 1024, aby nie wymagać uprawnień roota
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"Serwer SMTP uruchomiony na {host}:{port}")
    print("Oczekiwanie na połączenie od klienta...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Połączono z: {addr}")
        
        # 1. Powitanie serwera
        conn.sendall(b"220 localhost ESMTP Simulator Ready\r\n")
        
        in_data_mode = False
        
        while True:
            data = conn.recv(4096).decode('utf-8')
            if not data:
                break
            
            # Obsługa trybu DATA (odbieranie treści maila)
            if in_data_mode:
                # Szukamy kropki w nowej linii kończącej transmisję
                if "\r\n.\r\n" in data or data == ".\r\n":
                    print("--- KONIEC TREŚCI WIADOMOŚCI ---")
                    conn.sendall(b"250 2.0.0 Ok: queued as 12345\r\n")
                    in_data_mode = False
                else:
                    print(f"Odebrano treść: {data.strip()}")
                continue

            # Parsowanie komend
            line = data.strip()
            command = line.split(' ')[0].upper()
            print(f"Klient: {line}")

            if command == "EHLO" or command == "HELO":
                conn.sendall(b"250-localhost Hello\r\n250-SIZE 52428800\r\n250-AUTH LOGIN\r\n250 HELP\r\n")
            
            elif command == "AUTH":
                # Symulujemy akceptację każdego logowania
                conn.sendall(b"334 VXNlcm5hbWU6\r\n") # Prośba o login
                # Odbieramy login
                conn.recv(1024)
                conn.sendall(b"334 UGFzc3dvcmQ6\r\n") # Prośba o hasło
                # Odbieramy hasło
                conn.recv(1024)
                conn.sendall(b"235 2.7.0 Authentication successful\r\n")

            elif command == "MAIL":
                conn.sendall(b"250 2.1.0 Ok\r\n")
            
            elif command == "RCPT":
                conn.sendall(b"250 2.1.5 Ok\r\n")
            
            elif command == "DATA":
                in_data_mode = True
                conn.sendall(b"354 End data with <CR><LF>.<CR><LF>\r\n")
                print("--- START TREŚCI WIADOMOŚCI ---")
            
            elif command == "QUIT":
                conn.sendall(b"221 2.0.0 Bye\r\n")
                conn.close()
                break
            
            elif command == "NOOP":
                conn.sendall(b"250 2.0.0 Ok\r\n")

            else:
                # Obsługa niezaimplementowanych komend
                conn.sendall(b"502 5.5.1 Command not implemented\r\n")
                print(f"Nierozpoznana komenda: {command}")

        print(f"Rozłączono z {addr}")

if __name__ == "__main__":
    main()
