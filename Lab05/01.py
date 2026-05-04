import socket

def start_client():
    host = 'localhost'
    port = 2912

    # Tworzymy gniazdo (socket) TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Nawiązanie połączenia z serwerem
            s.connect((host, port))
            print(f"Połączono z serwerem na {host}:{port}")
            print("Wpisz 'exit', aby zakończyć.")

            while True:
                # Pobranie liczby od użytkownika
                user_input = input("Zgadnij liczbę: ")

                if user_input.lower() == 'exit':
                    break

                # Wysyłanie danych do serwera (zakodowane jako tekst)
                s.sendall(user_input.encode('utf-8'))

                # Odbieranie odpowiedzi od serwera
                data = s.recv(1024)
                
                if not data:
                    print("Serwer zakończył połączenie.")
                    break

                print(f"Odpowiedź serwera: {data.decode('utf-8')}")

        except ConnectionRefusedError:
            print("Błąd: Nie można połączyć się z serwerem. Upewnij się, że serwer działa.")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    start_client()
