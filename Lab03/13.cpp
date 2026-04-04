#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include "UDPSocket.hpp"

// Funkcja pomocnicza do konwersji ciągu znaków hex na bajty
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
    // 1. Zapis datagramu z zadania w jednym ciągu znaków (bez spacji dla wygody przetwarzania)
    std::string hex_datagram = "ed740b550024effd70726f6772616d6d696e6720696e20707974686f6e2069732066756e";
    std::vector<uint8_t> data = hex_to_bytes(hex_datagram);

    // 2. Parsowanie nagłówka UDP (Big-Endian)
    uint16_t src_port = (data[0] << 8) | data[1];
    uint16_t dst_port = (data[2] << 8) | data[3];
    
    // Wydobycie długości całego pakietu i odjęcie 8 bajtów nagłówka w celu uzyskania wielkości danych
    uint16_t total_length = (data[4] << 8) | data[5];
    uint16_t data_length = total_length - 8; 

    // 3. Wydobycie danych (zamiana bajtów na string)
    std::string payload(data.begin() + 8, data.begin() + 8 + data_length);

    std::cout << "--- Pobrane dane z datagramu ---" << std::endl;
    std::cout << "Port zrodlowy: " << src_port << std::endl;
    std::cout << "Port docelowy: " << dst_port << std::endl;
    std::cout << "Wielkosc danych: " << data_length << " bajtow" << std::endl;
    std::cout << "Zawartosc: " << payload << "\n\n";

    // 4. Budowanie wiadomości wynikowej
    std::stringstream ss;
    ss << "zad14odp;src;" << src_port << ";dst;" << dst_port << ";data;" << payload;
    std::string message = ss.str();

    std::cout << "[INFO] Wysylam sformatowana wiadomosc: " << message << std::endl;

    // 5. Połączenie i wysłanie danych na localhost wykorzystując klasę UDPSocket
    UDPSocket udp_socket;
    udp_socket.create();
    
    // Wysyłamy na localhost na porcie 2910 zgodnie ze zmodyfikowanym poleceniem
    udp_socket.connectTo("127.0.0.1", 2909); 

    // Wysłanie przygotowanego bufora
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
