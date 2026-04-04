#include <iostream>
#include <sys/socket.h>
#include "TCPSocket.hpp"
#include "DNSResolv.hpp"
#include <string>
#include <unistd.h>
#include <algorithm>

// Funkcja gwarantująca wysłanie dokładnie 'len' bajtów
bool send_all(int sockfd, const char* buffer, size_t len) {
    size_t total_sent = 0;
    
    while (total_sent < len) {
        // Wysyłamy to, co zostało: len - total_sent
        // Zaczynamy od przesuniętego wskaźnika: buffer + total_sent
        ssize_t n = send(sockfd, buffer + total_sent, len - total_sent, 0);
        
        if (n <= 0) {
            // n == 0 oznacza zamknięcie połączenia przez drugą stronę
            // n < 0 oznacza błąd
            return false;
        }
        total_sent += n;
    }
    return true;
}

// Funkcja gwarantująca odebranie dokładnie 'len' bajtów
bool recv_all(int sockfd, char* buffer, size_t len) {
    size_t total_received = 0;
    
    while (total_received < len) {
        ssize_t n = recv(sockfd, buffer + total_received, len - total_received, 0);
        
        if (n <= 0) {
            return false;
        }
        total_received += n;
    }
    return true;
}

int main(){
    TCPSocket socket;
    socket.create();
    socket.connectTo("127.0.0.1", 2908);
    
    std::string message = "Hello Server!"; 
    const size_t MSG_LENGTH = 20;

    // Przycięcie lub uzupełnienie do równej długości 20 znaków
    message.resize(MSG_LENGTH, ' ');

    std::cout << "Wysylam: [" << message << "] (dlugosc: " << message.length() << ")" << std::endl;

    // 1. WYSYŁANIE w pętli
    if (!send_all(socket.fd, message.c_str(), MSG_LENGTH)) {
        std::cerr << "Blad: Nie udalo sie wyslac calej wiadomosci.\n";
        return 1;
    }

    // 2. ODBIÓR w pętli
    char buffer[MSG_LENGTH + 1]; 
    std::fill(buffer, buffer + MSG_LENGTH + 1, 0);

    if (recv_all(socket.fd, buffer, MSG_LENGTH)) {
        buffer[MSG_LENGTH] = '\0'; // Zapewnienie null-terminatora
        std::cout << "Odebrano: [" << buffer << "] (bajtow: " << MSG_LENGTH << ")\n";
    } else {
        std::cerr << "Blad: Nie udalo sie odebrac kompletnej wiadomosci lub polaczenie zerwane.\n";
    }
    
    return 0;
}
