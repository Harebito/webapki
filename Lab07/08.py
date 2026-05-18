import poplib

POP3_SERVER = 'pop3.interia.pl'
PORT = 110
USER = 'pas2017@interia.pl'
PASSWORD = 'P4SInf2017'

def sprawdz_rozmiary_wiadomosci():
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

        # 3. Pobranie listy wiadomości (odpowiednik komendy LIST)
        odpowiedz, lista_linii, laczny_rozmiar = klient.list()

        print("\n" + "="*45)
        print(" LISTA WIADOMOŚCI I ICH ROZMIARY ")
        print("="*45)
        print(f"{'Numer wiadomości':<20} | {'Rozmiar (bajty)':<15}")
        print("-"*45)

        # Jeśli skrzynka jest pusta, lista_linii będzie pusta
        if not lista_linii:
            print("Skrzynka pocztowa jest pusta.")
        else:
            # Iteracja po każdej linii zwróconej przez serwer
            for linia in lista_linii:
                # Dekodujemy bajty na tekst i dzielimy spacją
                elementy = linia.decode('utf-8').split()
                num_wiadomosci = elementy[0]
                rozmiar_bajtów = elementy[1]
                
                print(f"Wiadomość nr {num_wiadomosci:<11} | {rozmiar_bajtów:<15} bajtów")

        print("="*45 + "\n")

        # 4. Zamknięcie połączenia
        print("Zamykanie połączenia...")
        klient.quit()
        print("Połączenie zamknięte.")

    except poplib.error_proto as e:
        print(f"\nBłąd protokołu POP3 (np. błędne dane logowania): {e}")
    except Exception as e:
        print(f"\nWystąpił błąd podczas połączenia: {e}")

if __name__ == "__main__":
    sprawdz_rozmiary_wiadomosci()
