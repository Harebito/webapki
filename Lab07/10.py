import poplib
from email import message_from_bytes
from email.message import EmailMessage
from email.policy import default

POP3_SERVER = 'pop3.interia.pl'
PORT = 110
USER = 'pas2017@interia.pl'
PASSWORD = 'P4SInf2017'

def wyswietl_wszystkie_wiadomosci() -> None:
    try:
        print(f"Łączenie z serwerem {POP3_SERVER} na porcie {PORT}...")
        # 1. Nawiązanie połączenia
        klient = poplib.POP3(POP3_SERVER, PORT)
        
        # Wyświetlenie powitania serwera
        print("Serwer odpowiedział:", klient.getwelcome().decode('utf-8'))

        # 2. Autoryzacja (Logowanie)
        print("Logowanie...")
        klient.user(USER)
        klient.pass_(PASSWORD)
        print("Zalogowano pomyślnie!")

        # 3. Sprawdzenie liczby wiadomości w skrzynce
        liczba_wiadomosci, _ = klient.stat()
        print(f"\nZnaleziono wiadomości w skrzynce: {liczba_wiadomosci}")

        if liczba_wiadomosci == 0:
            print("Skrzynka jest pusta.")
            klient.quit()
            return

        # 4. Pętla pobierająca każdą wiadomość z osobna
        for i in range(1, liczba_wiadomosci + 1):
            print("\n" + "=" * 60)
            print(f" POBIERANIE WIADOMOŚCI NR {i} z {liczba_wiadomosci} ")
            print("=" * 60)

            # Pobranie konkretnej wiadomości
            _, linie_tresci, _ = klient.retr(i)

            # Łączenie linii bajtów w jeden ciąg
            surowa_wiadomosc = b'\n'.join(linie_tresci)
            
            # Parsowanie wiadomości z jawnym wskazaniem typu EmailMessage
            msg = message_from_bytes(surowa_wiadomosc, policy=default)
            if not isinstance(msg, EmailMessage):
                continue

            # Wyświetlenie nagłówków wiadomości (zapewniamy typ str lub domyślny tekst)
            print(f"Od:     {str(msg.get('From', 'Brak nadawcy'))}")
            print(f"Do:     {str(msg.get('To', 'Brak odbiorcy'))}")
            print(f"Temat:  {str(msg.get('Subject', 'Brak tematu'))}")
            print(f"Data:   {str(msg.get('Date', 'Brak daty'))}")
            print("-" * 60)
            
            # 5. Bezpieczne pobranie i wyświetlenie właściwej treści tekstowej
            body = msg.get_body(preferencelist=('plain', 'html'))
            if body is not None:
                tresc: str = body.get_content()
                print(tresc)
            else:
                print("[Wiadomość nie zawiera czytelnej treści tekstowej]")
                
            print("-" * 60)

        print("\n" + "=" * 60)
        print("Pomyślnie wyświetlono wszystkie wiadomości.")
        
        # 6. Zamknięcie połączenia
        print("Zamykanie połączenia...")
        klient.quit()
        print("Połączenie zamknięte.")

    except poplib.error_proto as e:
        print(f"\nBłąd protokołu POP3: {str(e)}")
    except Exception as e:
        print(f"\nWystąpił błąd podczas działania programu: {str(e)}")

if __name__ == "__main__":
    wyswietl_wszystkie_wiadomosci()
