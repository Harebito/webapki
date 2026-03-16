#include <iostream>
#include <string>
#include <cstring>
#include <netdb.h>
#include <arpa/inet.h>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Użycie: " << argv[0] << " <hostname>" << std::endl;
        return 1;
    }

    const char* hostname = argv[1];
    struct addrinfo hints, *res;
    char ip_str[INET_ADDRSTRLEN];

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;

    int status = getaddrinfo(hostname, NULL, &hints, &res);
    if (status != 0) {
        std::cerr << "Błąd: " << gai_strerror(status) << std::endl;
        return 1;
    }

    std::cout << "Wyniki dla hosta: " << hostname << std::endl;

    for (struct addrinfo* p = res; p != NULL; p = p->ai_next) {
        struct sockaddr_in* ipv4 = (struct sockaddr_in*)p->ai_addr;
        
        inet_ntop(p->ai_family, &(ipv4->sin_addr), ip_str, sizeof(ip_str));
        std::cout << "  - Adres IP: " << ip_str << std::endl;
    }

    freeaddrinfo(res);

    return 0;
}
