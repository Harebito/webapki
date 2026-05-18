import poplib

POP3_SERVER = 'pop3.interia.pl'
PORT = 110
USER = 'pasinf2017@interia.pl'
PASSWORD = 'P4SInf2017'

def sprawdz_skrzynke():
    try:
        print(f"Łączenie z serwerem {POP3_SERVER} na porcie {PORT}...")
        # 1. Nawiązanie połączenia
        klient = poplib.POP3(POP3_SERVER, PORT)
        
        # Powitanie serwera
        print("Serwer odpowiedział:", klient.getwelcome().decode('utf-8'))

        # 2. Autoryzacja
        print("Logowanie...")
        klient.user(USER)
        klient.pass_(PASSWORD)
        print("Zalogowano pomyślnie!")

        # 3. Pobranie statusu skrzynki
        liczba_wiadomosci, laczny_rozmiar = klient.stat()

        print("\n" + "="*30)
        print(f"Liczba wiadomości w skrzynce: {liczba_wiadomosci}")
        print(f"Łączny rozmiar skrzynki: {laczny_rozmiar} bajtów")
        print("="*30 + "\n")

        # 4. Zamknięcie połączenia
        print("Zamykanie połączenia...")
        klient.quit()
        print("Połączenie zamknięte.")

    except poplib.error_proto as e:
        print(f"\nBłąd protokołu POP3 (np. złe hasło lub login): {e}")
    except Exception as e:
        print(f"\nWystąpił błąd podczas połączenia: {e}")

if __name__ == "__main__":
    sprawdz_skrzynke()
