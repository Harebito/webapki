import poplib
from email import message_from_bytes
from email.policy import default

POP3_SERVER = 'pop3.interia.pl'
PORT = 110
USER = 'pas2017@interia.pl'
PASSWORD = 'P4SInf2017'

def wyswietl_najwieksza_wiadomosc():
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

        # 3. Pobranie listy wiadomości
        odpowiedz, lista_linii, laczny_rozmiar = klient.list()

        if not lista_linii:
            print("\nSkrzynka pocztowa jest pusta. Brak wiadomości do wyświetlenia.")
            klient.quit()
            return

        # 4. Szukanie wiadomości o największym rozmiarze
        najwiekszy_numer = None
        najwiekszy_rozmiar = -1

        for linia in lista_linii:
            elementy = linia.decode('utf-8').split()
            num_wiadomosci = int(elementy[0])
            rozmiar_bajtów = int(elementy[1])
            
            # Sprawdzamy, czy ta wiadomość jest większa od dotychczas znalezionej
            if rozmiar_bajtów > najwiekszy_rozmiar:
                najwiekszy_rozmiar = rozmiar_bajtów
                najwiekszy_numer = num_wiadomosci

        print(f"\nNajwiększa wiadomość to nr: {najwiekszy_numer} (Rozmiar: {najwiekszy_rozmiar} bajtów)")
        print("Pobieranie treści wiadomości...")
        print("=" * 60)

        # 5. Pobranie treści największej wiadomości
        _, linie_tresci, _ = klient.retr(najwiekszy_numer)

        # Łączymy linie bajtów w jeden ciąg i tworzymy obiekt wiadomości e-mail
        surowa_wiadomosc = b'\n'.join(linie_tresci)
        msg = message_from_bytes(surowa_wiadomosc, policy=default)

        # 6. Wyświetlenie podstawowych nagłówków i treści
        print(f"Od: {msg['From']}")
        print(f"Do: {msg['To']}")
        print(f"Temat: {msg['Subject']}")
        print(f"Data: {msg['Date']}")
        print("-" * 60)
        
        # Pobieranie właściwej treści (tekstowej) wiadomości
        body = msg.get_body(preferencelist=('plain', 'html'))
        if body:
            print(body.get_content())
        else:
            # Jeśli struktura e-maila jest nietypowa, wypisz surowy tekst
            print(msg.get_payload(decode=True).decode('utf-8', errors='ignore'))
            
        print("=" * 60)

        # 7. Zamknięcie połączenia
        print("Zamykanie połączenia...")
        klient.quit()
        print("Połączenie zamknięte.")

    except poplib.error_proto as e:
        print(f"\nBłąd protokołu POP3: {e}")
    except Exception as e:
        print(f"\nWystąpił błąd podczas działania programu: {e}")

if __name__ == "__main__":
    wyswietl_najwieksza_wiadomosc()
