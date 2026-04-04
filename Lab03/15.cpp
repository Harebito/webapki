#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <cstring>
#include "UDPSocket.hpp"

// Funkcja pomocnicza do konwersji hex na wektor bajtów
std::vector<uint8_t> hex_to_bytes(const std::string& hex) {
    std::vector<uint8_t> bytes;
    for (size_t i = 0; i < hex.length(); i += 2) {
        std::string byteString = hex.substr(i, 2);
        uint8_t byte = (uint8_t) strtol(byteString.c_str(), NULL, 16);
        bytes.push_back(byte);
    }
    return bytes;
}

int main() {
    // 1. Zapis całego pakietu
    std::string hex_packet = "4500004ef7fa400038069d33d4b6181bc0a800020b54b9a6fbf93c57c10a06c1801800e3ce9c00000101080a03a6eb01000bf8e56e6574776f726b2070726f6772616d6d696e672069732066756e";
    std::vector<uint8_t> data = hex_to_bytes(hex_packet);

    // 2. Parsowanie nagłówka IP
    uint8_t version = data[0] >> 4; // 4 najbardziej znaczące bity
    uint8_t ihl = (data[0] & 0x0F) * 4; // 4 najmniej znaczące bity pomnożone przez 4
    
    uint16_t total_length = (data[2] << 8) | data[3];
    uint8_t protocol = data[9];
    
    // Budowanie adresów IP jako string
    std::string src_ip = std::to_string(data[12]) + "." + std::to_string(data[13]) + "." + 
                         std::to_string(data[14]) + "." + std::to_string(data[15]);
    std::string dst_ip = std::to_string(data[16]) + "." + std::to_string(data[17]) + "." + 
                         std::to_string(data[18]) + "." + std::to_string(data[19]);

    // 3. Parsowanie nagłówka TCP/UDP (zakładając, że to TCP z kodu 0x06)
    uint16_t src_port = (data[ihl] << 8) | data[ihl + 1];
    uint16_t dst_port = (data[ihl + 2] << 8) | data[ihl + 3];
    
    uint8_t tcp_header_length = (data[ihl + 12] >> 4) * 4;
    
    // 4. Wydobycie danych (Data)
    uint16_t total_headers_length = ihl + tcp_header_length;
    uint16_t data_length = total_length - total_headers_length;
    std::string payload(data.begin() + total_headers_length, data.begin() + total_headers_length + data_length);

    std::cout << "--- WYDOBYTE DANE ---" << std::endl;
    std::cout << "Wersja IP: " << (int)version << std::endl;
    std::cout << "Src IP: " << src_ip << " | Dst IP: " << dst_ip << std::endl;
    std::cout << "Protokol: " << (int)protocol << std::endl;
    std::cout << "Src Port: " << src_port << " | Dst Port: " << dst_port << std::endl;
    std::cout << "Dane: " << payload << std::endl;
    std::cout << "---------------------\n" << std::endl;

    // Przygotowanie socketu
    UDPSocket udp_socket;
    udp_socket.create();
    udp_socket.connectTo("127.0.0.1", 2911); 

    char buffer[1024];

    // ==========================================
    // ETAP 1: Wysłanie wiadomości A (Nagłówek IP)
    // ==========================================
    std::stringstream ssA;
    ssA << "zad15odpA;ver;" << (int)version << ";srcip;" << src_ip 
        << ";dstip;" << dst_ip << ";type;" << (int)protocol;
    std::string msgA = ssA.str();

    std::cout << "[INFO] Wysylam wiadomosc A: " << msgA << std::endl;
    send(udp_socket.fd, msgA.c_str(), msgA.length(), 0);

    memset(buffer, 0, sizeof(buffer));
    int n = recv(udp_socket.fd, buffer, sizeof(buffer) - 1, 0);
    
    if (n > 0) {
        std::string responseA(buffer);
        std::cout << "[SERWER] Odpowiedz A: " << responseA << std::endl;

        // Jeśli serwer zaakceptuje część pierwszą, przechodzimy do drugiej
        if (responseA == "TAK") {
            // ==========================================
            // ETAP 2: Wysłanie wiadomości B (Nagłówek TCP/Dane)
            // ==========================================
            std::stringstream ssB;
            ssB << "zad15odpB;srcport;" << src_port << ";dstport;" << dst_port 
                << ";data;" << payload;
            std::string msgB = ssB.str();

            std::cout << "\n[INFO] Wysylam wiadomosc B: " << msgB << std::endl;
            send(udp_socket.fd, msgB.c_str(), msgB.length(), 0);

            memset(buffer, 0, sizeof(buffer));
            n = recv(udp_socket.fd, buffer, sizeof(buffer) - 1, 0);

            if (n > 0) {
                std::cout << "[SERWER] Odpowiedz B: " << buffer << std::endl;
            } else {
                std::cerr << "[BLAD] Nie udalo sie odebrac odpowiedzi B." << std::endl;
            }
        } else {
            std::cout << "[INFO] Przerwano. Serwer nie zwrocil TAK dla wiadomosci A." << std::endl;
        }
    } else {
        std::cerr << "[BLAD] Brak odpowiedzi na wiadomosc A." << std::endl;
    }

    return 0;
}
