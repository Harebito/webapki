import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

nadawca = input("Podaj swój e-mail (Interia): ")
haslo = input("Podaj hasło (lub hasło do aplikacji): ")
odbiorca = input("Podaj e-mail odbiorcy: ")
temat = input("Podaj temat wiadomości: ")
tresc = input("Podaj treść wiadomości: ")

msg = MIMEMultipart()
msg['From'] = nadawca
msg['To'] = odbiorca
msg['Subject'] = temat
msg.attach(MIMEText(tresc, 'plain', 'utf-8'))

try:
    print("Łączenie z serwerem...")
    server = smtplib.SMTP('poczta.interia.pl', 587)
    
    server.starttls()
    
    server.login(nadawca, haslo)
    
    server.send_message(msg)
    
    print(" Wiadomość wysłana pomyślnie!")
    
except Exception as e:
    print(f" Błąd: {e}")

finally:
    server.quit()
