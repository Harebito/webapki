import socket
import ssl
import base64
import os

def ask_user(prompt):
    return input(prompt).strip()

def send_command(sock, cmd):
    sock.sendall((cmd + "\r\n").encode('utf-8'))
    response = sock.recv(4096).decode('utf-8')
    print(f"> {cmd[:50]}...")
    print(f"< {response.splitlines()[0]}")
    return response

def main():
    # 1. Dane od użytkownika
    user_email = ask_user("Twój email (Interia): ")
    password = ask_user("Hasło / Hasło aplikacji: ")
    recipient = ask_user("Adres odbiorcy: ")
    subject = ask_user("Temat: ")
    body = ask_user("Treść wiadomości: ")
    
    image_path = "obrazek.png"
    if not os.path.exists(image_path):
        print(f"Błąd: Plik {image_path} nie istnieje!")
        return

    # 2. Przygotowanie obrazka
    with open(image_path, "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode('utf-8')

    # 3. Połączenie TCP
    host = "poczta.interia.pl"
    port = 587
    raw_sock = socket.create_connection((host, port))
    print(f"Połączono: {raw_sock.recv(4096).decode('utf-8').strip()}")

    # 4. Negocjacja STARTTLS
    send_command(raw_sock, f"EHLO {host}")
    send_command(raw_sock, "STARTTLS")

    # Przejście na szyfrowanie SSL
    context = ssl.create_default_context()
    sock = context.wrap_socket(raw_sock, server_hostname=host)

    # 5. Logowanie
    send_command(sock, f"EHLO {host}")
    send_command(sock, "AUTH LOGIN")
    send_command(sock, base64.b64encode(user_email.encode()).decode())
    send_command(sock, base64.b64encode(password.encode()).decode())

    # 6. Nadawca i Odbiorca
    send_command(sock, f"MAIL FROM:<{user_email}>")
    send_command(sock, f"RCPT TO:<{recipient}>")

    # 7. Budowanie wiadomości MIME (DATA)
    send_command(sock, "DATA")
    
    boundary = "MojaUnikalnaGranicaMIME"
    
    message_lines = [
        f"From: {user_email}",
        f"To: {recipient}",
        f"Subject: {subject}",
        "MIME-Version: 1.0",
        f"Content-Type: multipart/mixed; boundary=\"{boundary}\"",
        "",
        f"--{boundary}",
        "Content-Type: text/plain; charset=utf-8",
        "",
        body,
        "",
        f"--{boundary}",
        f"Content-Type: image/jpeg; name=\"{os.path.basename(image_path)}\"",
        "Content-Transfer-Encoding: base64",
        f"Content-Disposition: attachment; filename=\"{os.path.basename(image_path)}\"",
        "",
        img_b64,
        "",
        f"--{boundary}--",
        "."
    ]

    full_data = "\r\n".join(message_lines) + "\r\n"
    sock.sendall(full_data.encode('utf-8'))
    
    print(f"< {sock.recv(4096).decode('utf-8').strip()}")

    # 8. Koniec
    send_command(sock, "QUIT")
    sock.close()
    print("\n Proces zakończony.")

if __name__ == "__main__":
    main()
