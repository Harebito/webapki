import socket
import random

def start_standalone_server():
    host = '127.0.0.1'
    port = 2912
    
    # Serwer losuje liczbę na początku działania
    secret_number = random.randint(1, 100)
    print(f"Serwer oczekuje na połączenie pod adresem {host}:{port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Ustawienie opcji ponownego użycia portu (przydatne przy częstym restartowaniu)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)

        conn, addr = s.accept()
        with conn:
            print(f"Połączono z: {addr}")
            
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                # Dekodowanie otrzymanej wiadomości i usuwanie białych znaków
                received_data = data.decode('utf-8').strip()

                # Walidacja: Czy otrzymana wiadomość jest liczbą?
                if not received_data.isdigit() and not (received_data.startswith('-') and received_data[1:].isdigit()):
                    msg = "BŁĄD: Przesłana wiadomość nie jest liczbą!"
                    conn.sendall(msg.encode('utf-8'))
                    continue

                # Konwersja na typ int
                guess = int(received_data)

                # Logika porównywania
                if guess < secret_number:
                    response = "Twoja liczba jest mniejsza od wylosowanej."
                elif guess > secret_number:
                    response = "Twoja liczba jest większa od wylosowanej."
                else:
                    response = "GRATULACJE! Odgadłeś liczbę."
                    conn.sendall(response.encode('utf-8'))
                    print(f"Liczba {secret_number} odgadnięta. Kończę działanie.")
                    break # Wyjście z pętli kończy działanie serwera

                conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    start_standalone_server()
