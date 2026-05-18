import poplib

POP3_SERVER = 'pop3.interia.pl'
PORT = 110
USER = 'pas2017@interia.pl'
PASSWORD = 'P4SInf2017'

def sprawdz_rozmiar_skrzynki():
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

        # 3. Pobranie danych o rozmiarze
        _, laczny_rozmiar_bajtów = klient.stat()

        print("\n" + "="*40)
        print(f"Łączny rozmiar wiadomości w skrzynce: {laczny_rozmiar_bajtów} bajtów")
        # Na kilobajty dla lepszej czytelności
        print(f"W przeliczeniu: {laczny_rozmiar_bajtów / 1024:.2f} KB")
        print("="*40 + "\n")

        # 4. Zamknięcie połączenia
        print("Zamykanie połączenia...")
        klient.quit()
        print("Połączenie zamknięte.")

    except poplib.error_proto as e:
        print(f"\nBłąd protokołu POP3 (np. błędne dane logowania): {e}")
    except Exception as e:
        print(f"\nWystąpił błąd podczas połączenia: {e}")

if __name__ == "__main__":
    sprawdz_rozmiar_skrzynki()
