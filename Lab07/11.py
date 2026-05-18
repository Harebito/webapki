import poplib
import os
from email import message_from_bytes
from email.policy import default

POP3_SERVER = 'pop3.interia.pl'
PORT = 110
USER = 'pas2017@interia.pl'
PASSWORD = 'P4SInf2017'

def pobierz_zalacznik_obrazkowy():
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

        # 3. Sprawdzenie liczby wiadomości
        liczba_wiadomosci, _ = klient.stat()
        print(f"Liczba wiadomości w skrzynce: {liczba_wiadomosci}")

        if liczba_wiadomosci == 0:
            print("Skrzynka jest pusta.")
            klient.quit()
            return

        znaleziono_obrazek = False

        # 4. Przeszukiwanie wiadomości (od najnowszej do najstarszej)
        for i in range(liczba_wiadomosci, 0, -1):
            print(f"\nSprawdzanie wiadomości nr {i}...")
            
            # Pobranie wiadomości z serwera
            _, linie_tresci, _ = klient.retr(i)
            surowa_wiadomosc = b'\n'.join(linie_tresci)
            
            # Parsowanie wiadomości do obiektu e-mail
            msg = message_from_bytes(surowa_wiadomosc, policy=default)
            
            # 5. Przeszukiwanie części wiadomości (MIME) w poszukiwaniu załącznika
            if msg.is_multipart():
                for czesc in msg.walk():
                    # Pobieramy typ zawartości (Content-Type)
                    content_type = czesc.get_content_type()
                    # Pobieramy nazwę pliku z nagłówka Content-Disposition
                    nazwa_pliku = czesc.get_filename()

                    # Sprawdzamy, czy ta część to obrazek i czy ma nazwę pliku
                    if nazwa_pliku and content_type.startswith('image/'):
                        print(f"Znaleziono obrazek: {nazwa_pliku} (Typ: {content_type})")
                        
                        dane_obrazka = czesc.get_content()
                        
                        # 6. Zapisanie odkodowanego obrazka na dysk
                        with open(nazwa_pliku, 'wb') as f:
                            f.write(dane_obrazka)
                        
                        print(f"Sukces! Obrazek został zapisany jako: {os.path.abspath(nazwa_pliku)}")
                        znaleziono_obrazek = True
                        break # Wyjście z pętli przeglądającej części maila
                        
            if znaleziono_obrazek:
                break # Wyjście z pętli przeglądającej maile po znalezieniu pierwszego obrazka

        if not znaleziono_obrazek:
            print("\nW żadnej wiadomości nie znaleziono załącznika będącego obrazkiem.")

        # 7. Zamknięcie połączenia
        print("\nZamykanie połączenia...")
        klient.quit()
        print("Połączenie zamknięte.")

    except poplib.error_proto as e:
        print(f"\nBłąd protokołu POP3: {e}")
    except Exception as e:
        print(f"\nWystąpił błąd podczas działania programu: {e}")

if __name__ == "__main__":
    pobierz_zalacznik_obrazkowy()
