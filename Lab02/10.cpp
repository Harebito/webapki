#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(int argc, char* argv[]) {
    // Sprawdzenie argumentów uruchomienia
    if (argc != 2) {
        std::cerr << "Użycie: " << argv[0] << " <nazwa_hosta_do_sprawdzenia>" << std::endl;
        return 1;
    }

    std::string hostname_to_send = argv[1];

    // 1. Tworzenie gniazda UDP
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        std::cerr << "Błąd: Nie można utworzyć gniazda." << std::endl;
        return 1;
    }

    // 2. Konfiguracja adresu serwera docelowego (localhost:2907)
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(2907); // Port 2907
    
    // Przekształcenie adresu localhost na format sieciowy
    if (inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr) <= 0) {
        std::cerr << "Błąd: Nieprawidłowy adres serwera." << std::endl;
        close(sockfd);
        return 1;
    }

    // 3. Wysłanie nazwy hosta (hostname) do serwera
    ssize_t sent_bytes = sendto(sockfd, hostname_to_send.c_str(), hostname_to_send.length(), 0,
                                (const struct sockaddr*)&server_addr, sizeof(server_addr));
    
    if (sent_bytes < 0) {
        std::cerr << "Błąd: Nie udało się wysłać danych." << std::endl;
        close(sockfd);
        return 1;
    }
    std::cout << "[INFO] Wysłano zapytanie o nazwę hosta: " << hostname_to_send << std::endl;

    // 4. Odbiór odpowiedzi (adres IP) od serwera
    char buffer[1024];
    memset(buffer, 0, sizeof(buffer));
    struct sockaddr_in from_addr;
    socklen_t from_len = sizeof(from_addr);

    std::cout << "[INFO] Oczekiwanie na odpowiedź z serwera..." << std::endl;
    ssize_t received_bytes = recvfrom(sockfd, buffer, sizeof(buffer) - 1, 0,
                                      (struct sockaddr*)&from_addr, &from_len);

    if (received_bytes < 0) {
        std::cerr << "Błąd: Nie udało się odebrać danych." << std::endl;
    } else {
        // Dodanie znaku końca ciągu, aby bezpiecznie wyświetlić string
        buffer[received_bytes] = '\0'; 
        std::cout << "[SUKCES] Otrzymany adres IP: " << buffer << std::endl;
    }

    // 5. Zamknięcie gniazda
    close(sockfd);
    return 0;
}
