#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include "UDPSocket.hpp"

// Funkcja pomocnicza do konwersji ciągu znaków hex na wektor bajtów
std::vector<uint8_t> hex_to_bytes(const std::string& hex) {
    std::vector<uint8_t> bytes;
    // Iterujemy po 2 znaki (każda para to 1 bajt)
    for (size_t i = 0; i < hex.length(); i += 2) {
        std::string byteString = hex.substr(i, 2);
        uint8_t byte = (uint8_t) strtol(byteString.c_str(), NULL, 16);
        bytes.push_back(byte);
    }
    return bytes;
}

int main() {
    // 1. Pełny segment TCP zapisany w jednym ciągu znaków hex
    std::string hex_segment = "0b54898b1f9a18ecbbb164f2801800e3677100000101080a02c1a4ee001a4cee68656c6c6f203a29";
    std::vector<uint8_t> data = hex_to_bytes(hex_segment);

    // 2. Parsowanie nagłówka TCP (Big-Endian)
    uint16_t src_port = (data[0] << 8) | data[1];
    uint16_t dst_port = (data[2] << 8) | data[3];
    
    // Pobranie "Data Offset" (najbardziej znaczące 4 bity 13-go bajtu - indeks 12)
    // Przesunięcie bitowe w prawo o 4 (>> 4) wyciąga tę wartość.
    // Mnożymy przez 4, aby otrzymać wielkość nagłówka w bajtach.
    uint8_t header_length = (data[12] >> 4) * 4; 

    // 3. Wydobycie danych (Data) z segmentu, rozpoczynając po nagłówku
    std::string payload(data.begin() + header_length, data.end());

    std::cout << "--- Pobrane dane z segmentu TCP ---" << std::endl;
    std::cout << "Port zrodlowy: " << src_port << std::endl;
    std::cout << "Port docelowy: " << dst_port << std::endl;
    std::cout << "Wielkosc naglowka: " << (int)header_length << " bajtow" << std::endl;
    std::cout << "Wielkosc danych: " << payload.length() << " bajtow" << std::endl;
    std::cout << "Zawartosc: " << payload << "\n\n";

    // 4. Budowanie wiadomości wynikowej
    std::stringstream ss;
    // Ważne: polecenie na obrazku i w skrypcie pythona wymaga identyfikatora "zad13odp"
    ss << "zad13odp;src;" << src_port << ";dst;" << dst_port << ";data;" << payload;
    std::string message = ss.str();

    std::cout << "[INFO] Wysylam sformatowana wiadomosc: " << message << std::endl;

    // 5. Połączenie i wysłanie danych na localhost wykorzystując klasę UDPSocket
    UDPSocket udp_socket;
    udp_socket.create();
    
    // Cel: serwer testowy UDP (odpowiednik z Twojego skryptu)
    udp_socket.connectTo("127.0.0.1", 2909); 

    // Wysłanie danych
    if (send(udp_socket.fd, message.c_str(), message.length(), 0) < 0) {
        std::cerr << "[BLAD] Nie udalo sie wyslac wiadomosci." << std::endl;
        return 1;
    }

    // 6. Oczekiwanie na weryfikację z serwera (TAK, NIE, BAD_SYNTAX)
    char buffer[1024];
    memset(buffer, 0, sizeof(buffer));
    
    std::cout << "[INFO] Oczekiwanie na odpowiedz z serwera..." << std::endl;
    int n = recv(udp_socket.fd, buffer, sizeof(buffer) - 1, 0);

    if (n > 0) {
        std::cout << "[SUKCES] Odpowiedz serwera: " << buffer << std::endl;
    } else {
        std::cerr << "[BLAD] Blad podczas odbierania odpowiedzi z serwera." << std::endl;
    }

    return 0;
}
