import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main():
    # 1. Pobieranie danych od użytkownika
    print("--- Konfiguracja wysyłki ESMTP (HTML) ---")
    user_email = input("Twój email (Interia): ").strip()
    password = input("Hasło / Hasło aplikacji: ").strip()
    recipient = input("Adres odbiorcy: ").strip()
    subject = input("Temat wiadomości: ").strip()

    # 2. Tworzenie szkieletu wiadomości HTML
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h3 style="color: #004a99;">Test formatowania HTML w ESMTP</h3>
        <p>Witaj!</p>
        <p>Oto przykłady formatowania tekstu wymagane w zadaniu:</p>
        <ul>
          <li><b>Tekst pogrubiony (bold)</b></li>
          <li><i>Tekst pochylony (italic)</i></li>
          <li><u>Tekst podkreślony (underline)</u></li>
          <li><mark>Tekst wyróżniony (tło)</mark></li>
        </ul>
        <p style="color: gray; font-size: 0.8em;">Wysłano z programu Python przy użyciu biblioteki smtplib.</p>
      </body>
    </html>
    """

    # 3. Składanie obiektu MIME
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = user_email
    msg['To'] = recipient

    part_html = MIMEText(html_content, "html", "utf-8")
    msg.attach(part_html)

    # 4. Wysyłka przez serwer Interii
    host = "poczta.interia.pl"
    port = 587

    try:
        print(f"Łączenie z {host}...")
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            
            server.login(user_email, password)
            
            server.send_message(msg)
            
        print("\n Wiadomość HTML została wysłana pomyślnie!")

    except Exception as e:
        print(f"\n Błąd podczas wysyłki: {e}")

if __name__ == "__main__":
    main()
