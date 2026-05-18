import asyncio
import socket

HOST = '127.0.0.1'
PORT = 1110

# Zasymulowana baza danych e-maili w pamięci serwera
ZASYMULOWANE_MAILE = {
    1: (
        b"From: jan.kowalski@example.com\n"
        b"To: moj_login@twojadomena.pl\n"
        b"Subject: Pierwsza wiadomosc testowa\n"
        b"Date: Mon, 18 May 2026 10:00:00 +0200\n"
        b"Content-Type: text/plain; charset=utf-8\n"
        b"\n"
        b"Witaj! To jest pierwsza, automatycznie wygenerowana\n"
        b"wiadomosc tekstowa na Twoim wlasnym serwerze POP3."
    ),
    2: (
        b"From: anna.nowak@example.com\n"
        b"To: moj_login@twojadomena.pl\n"
        b"Subject: Testowy obrazek (Zalacznik)\n"
        b"Date: Mon, 18 May 2026 10:05:00 +0200\n"
        b"MIME-Version: 1.0\n"
        b"Content-Type: multipart/mixed; boundary=\"boundary_12345\"\n"
        b"\n"
        b"--boundary_12345\n"
        b"Content-Type: text/plain; charset=utf-8\n"
        b"\n"
        b"W zalaczniku przesylam maly, czarny kwadrat w formacie PNG.\n"
        b"\n"
        b"--boundary_12345\n"
        b"Content-Type: image/png; name=\"kwadrat.png\"\n"
        b"Content-Disposition: attachment; filename=\"kwadrat.png\"\n"
        b"Content-Transfer-Encoding: base64\n"
        b"\n"
        b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9"
        b"AwAAAABJRU5ErkJggg==\n"
        b"\n"
        b"--boundary_12345--"
    )
}

async def obsluga_klienta(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    adres = writer.get_extra_info('peername')
    print(f"[*] Nowe polaczenie z adresu: {adres}")
    
    # Stan sesji: 'AUTHORIZATION', 'TRANSACTION', 'UPDATE'
    stan = 'AUTHORIZATION'
    zalogowany_user = ""

    # Wyslanie powitania POP3
    writer.write(b"+OK Fake POP3 Server ready\r\n")
    await writer.drain()

    try:
        while True:
            dane = await reader.readline()
            if not dane:
                break
                
            linia = dane.decode('utf-8', errors='ignore').strip()
            if not linia:
                continue
                
            print(f"[{adres}] Klient napisal: {linia}")
            
            # Podzial na komende i argumenty
            elementy = linia.split(' ', 1)
            komenda = elementy[0].upper()
            argument = elementy[1] if len(elementy) > 1 else ""

            # --- FAZA 1: AUTORYZACJA ---
            if stan == 'AUTHORIZATION':
                if komenda == 'USER':
                    zalogowany_user = argument
                    writer.write(f"+OK password required for user {zalogowany_user}\r\n".encode())
                elif komenda == 'PASS':
                    if zalogowany_user:
                        stan = 'TRANSACTION'
                        writer.write(b"+OK Mailbox locked and ready\r\n")
                    else:
                        writer.write(b"-ERR login with USER first\r\n")
                elif komenda == 'QUIT':
                    writer.write(b"+OK Goodbye\r\n")
                    await writer.drain()
                    break
                else:
                    writer.write(b"-ERR Unknown command or invalid in this state\r\n")

            # --- FAZA 2: TRANSAKCJA ---
            elif stan == 'TRANSACTION':
                if komenda == 'STAT':
                    L = len(ZASYMULOWANE_MAILE)
                    rozmiar_total = sum(len(m) for m in ZASYMULOWANE_MAILE.values())
                    writer.write(f"+OK {L} {rozmiar_total}\r\n".encode())
                    
                elif komenda == 'LIST':
                    if argument:
                        try:
                            num = int(argument)
                            if num in ZASYMULOWANE_MAILE:
                                writer.write(f"+OK {num} {len(ZASYMULOWANE_MAILE[num])}\r\n".encode())
                            else:
                                writer.write(b"-ERR no such message\r\n")
                        except ValueError:
                            writer.write(b"-ERR invalid argument\r\n")
                    else:
                        writer.write(b"+OK mail list follows\r\n")
                        for num, mail in ZASYMULOWANE_MAILE.items():
                            writer.write(f"{num} {len(mail)}\r\n".encode())
                        writer.write(b".\r\n")
                        
                elif komenda == 'RETR':
                    try:
                        num = int(argument)
                        if num in ZASYMULOWANE_MAILE:
                            mail_bytes = ZASYMULOWANE_MAILE[num]
                            writer.write(f"+OK {len(mail_bytes)} octets\r\n".encode())
                            for l in mail_bytes.split(b'\n'):
                                if l.startswith(b'.'):
                                    writer.write(b'.' + l + b'\r\n')
                                else:
                                    writer.write(l + b'\r\n')
                            writer.write(b".\r\n")
                        else:
                            writer.write(b"-ERR no such message\r\n")
                    except ValueError:
                        writer.write(b"-ERR invalid argument\r\n")
                        
                elif komenda == 'NOOP':
                    writer.write(b"+OK\r\n")
                    
                elif komenda == 'QUIT':
                    stan = 'UPDATE'
                    writer.write(b"+OK Fake POP3 server signing off\r\n")
                    await writer.drain()
                    break
                    
                # Obsluga komend poprawnych w protokole POP3, ale niesymulowanych przez ten serwer
                elif komenda in ['DELE', 'RSET', 'UIDL', 'CAPA']:
                    writer.write(f"-ERR Command {komenda} is valid but not implemented in this mock\r\n".encode())
                    
                # Obsluga zupelnie blednych komend
                else:
                    writer.write(b"-ERR Unknown command\r\n")
            
            await writer.drain()

    except Exception as e:
        print(f"[!] Blad podczas obslugi {adres}: {e}")
    finally:
        print(f"[*] Zamykanie polaczenia z: {adres}")
        writer.close()
        await writer.wait_closed()

async def main() -> None:
    # Uruchomienie serwera TCP przy uzyciu asyncio
    server = await asyncio.start_server(obsluga_klienta, HOST, PORT, family=socket.AF_INET)
    print(f"[*] Serwer POP3 uruchomiony na {HOST}:{PORT}")
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Serwer zatrzymany przez uzytkownika.")
