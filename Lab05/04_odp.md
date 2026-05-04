### Porównanie protokołów TCP i UDP

#### **1. Dla którego z gniazd czas jest krótszy?**
W przeprowadzonym teście krótszy czas przesyłu danych uzyskuje zazwyczaj gniazdo UDP.

#### **2. Z czego wynika krótszy czas?**
Krótszy czas przesyłu w protokole UDP wynika z jego specyficznej architektury, która minimalizuje narzut komunikacyjny:

*   **Brak nawiązywania połączenia:** TCP wymaga procedury *Three-way handshake* (SYN, SYN-ACK, ACK) przed przesłaniem właściwych danych. UDP jest bezpołączeniowe – wysyła dane natychmiast.
*   **Brak potwierdzeń (ACK):** W TCP każdy odebrany pakiet (lub ich grupa) musi zostać potwierdzony przez odbiorcę. UDP nie wymaga potwierdzeń, co eliminuje ruch powrotny i oczekiwanie nadawcy.
*   **Brak retransmisji:** Jeśli pakiet TCP zginie, protokół wstrzymuje dalsze przesyłanie do czasu pomyślnego ponowienia wysyłki brakującego fragmentu. UDP ignoruje zgubione pakiety i przesyła kolejne.
*   **Uproszczony nagłówek:** Nagłówek UDP jest znacznie mniejszy (8 bajtów) w porównaniu do nagłówka TCP (minimum 20 bajtów), co oznacza mniej danych pomocniczych do przetworzenia.



#### **3. Zalety i wady obu rozwiązań**

| Cecha | **TCP** (Transmission Control Protocol) | **UDP** (User Datagram Protocol) |
| :--- | :--- | :--- |
| **Zalety** | **Niezawodność:** Gwarantuje dostarczenie danych.<br>**Kolejność:** Zapewnia, że dane dotrą w takiej samej kolejności, w jakiej zostały wysłane.<br>**Błędy:** Automatyczna retransmisja w razie zgubienia pakietu. | **Szybkość:** Brak opóźnień związanych z kontrolą przepływu.<br>**Lekkość:** Minimalny narzut na sieć i procesor.<br>**Transmisja:** Doskonały do przesyłania danych w czasie rzeczywistym (multicast/broadcast). |
| **Wady** | **Opóźnienia:** Większy czas odpowiedzi (overhead).<br>**Zasoby:** Wymaga więcej pamięci i mocy obliczeniowej do zarządzania stanem połączenia. | **Brak gwarancji:** Dane mogą zostać zgubione bez powiadomienia nadawcy.<br>**Brak kolejności:** Pakiety mogą dotrzeć do odbiorcy w pomieszanej kolejności. |
| **Zastosowania** | Strony WWW (HTTP/HTTPS), Poczta e-mail (SMTP/IMAP), Przesyłanie plików (FTP), SSH. | Gry online, Streaming wideo/audio, VoIP (rozmowy głosowe), Zapytania DNS. |
