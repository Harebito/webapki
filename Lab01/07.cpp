#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>

void scan_ports(const char* target_host) {
    struct addrinfo hints, *res;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;

    if (getaddrinfo(target_host, NULL, &hints, &res) != 0) {
        std::cerr << "Błąd: Nie można znaleźć hosta " << target_host << std::endl;
        return;
    }

    std::cout << "Skanowanie hosta: " << target_host << " (porty 1-1024)..." << std::endl;

    for (int port = 1; port <= 1024; ++port) {
        int sockfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
        if (sockfd < 0) continue;

        struct sockaddr_in* addr = (struct sockaddr_in*)res->ai_addr;
        addr->sin_port = htons(port);

        struct timeval tv;
        tv.tv_sec = 1;  // 1 sekunda timeoutu
        tv.tv_usec = 0;
        setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof(tv));
        setsockopt(sockfd, SOL_SOCKET, SO_SNDTIMEO, (const char*)&tv, sizeof(tv));

        if (connect(sockfd, (struct sockaddr*)addr, sizeof(struct sockaddr_in)) == 0) {
            std::cout << "[+] Port " << port << " jest OTWARTY" << std::endl;
            close(sockfd);
        } else {
            close(sockfd);
        }
    }

    freeaddrinfo(res);
    std::cout << "Skanowanie zakończone." << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Użycie: " << argv[0] << " <host/IP>" << std::endl;
        return 1;
    }

    scan_ports(argv[1]);
    return 0;
}
