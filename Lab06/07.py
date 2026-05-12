import socket
import ssl
import base64

def ask_user(prompt):
    return input(prompt).strip()

def send_command(sock, cmd):
    sock.sendall((cmd + "\r\n").encode('utf-8'))
    response = sock.recv(4096).decode('utf-8')
    print(f"> {cmd}")
    print(f"< {response.splitlines()[0]}")
    return response

def main():
    # 1. Dane od użytkownika
    user_email = ask_user("Twój email (Interia): ")
    password = ask_user("Hasło (lub hasło aplikacji): ")
    recipient = ask_user("Adres odbiorcy: ")
    subject = ask_user("Temat: ")
    body = ask_user("Treść wiadomości: ")
    filename = "zalacznik.txt"
    file_content = "To jest tresc zalacznika tekstowego."

    attachment_b64 = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')

    # 2. Połączenie TCP
    host = "poczta.interia.pl"
    port = 587
    
    raw_sock = socket.create_connection((host, port))
    print(f"< {raw_sock.recv(4096).decode('utf-8').strip()}")

    # 3. Rozpoczęcie sesji i STARTTLS
    send_command(raw_sock, f"EHLO {host}")
    send_command(raw_sock, "STARTTLS")

    # 4. "Owinięcie" socketu w SSL po komendzie STARTTLS
    context = ssl.create_default_context()
    sock = context.wrap_socket(raw_sock, server_hostname=host)

    # 5. Ponowne przywitanie i Logowanie
    send_command(sock, f"EHLO {host}")
    
    send_command(sock, "AUTH LOGIN")
    send_command(sock, base64.b64encode(user_email.encode()).decode())
    send_command(sock, base64.b64encode(password.encode()).decode())

    # 6. Adresaci
    send_command(sock, f"MAIL FROM:<{user_email}>")
    send_command(sock, f"RCPT TO:<{recipient}>")

    # 7. Treść wiadomości
    send_command(sock, "DATA")
    
    boundary = "SpecyficznaGranica123"
    
    email_data = [
        f"From: {user_email}",
        f"To: {recipient}",
        f"Subject: {subject}",
        "MIME-Version: 1.0",
        f"Content-Type: multipart/mixed; boundary={boundary}",
        "",
        f"--{boundary}",
        "Content-Type: text/plain; charset=utf-8",
        "",
        body,
        "",
        f"--{boundary}",
        f"Content-Type: text/plain; name=\"{filename}\"",
        "Content-Transfer-Encoding: base64",
        f"Content-Disposition: attachment; filename=\"{filename}\"",
        "",
        attachment_b64,
        "",
        f"--{boundary}--",
        "."
    ]

    full_message = "\r\n".join(email_data) + "\r\n"
    sock.sendall(full_message.encode('utf-8'))
    print(f"< {sock.recv(4096).decode('utf-8').strip()}")

    # 8. Zakończenie
    send_command(sock, "QUIT")
    sock.close()

if __name__ == "__main__":
    main()
