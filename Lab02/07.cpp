#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Użycie: " << argv[0] << " <host/IP> <port>" << std::endl;
        return 1;
    }

    const char* target_host = argv[1];
    const char* target_port = argv[2];

    struct addrinfo hints, *res, *p;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;     
    hints.ai_socktype = SOCK_STREAM; 

    int status = getaddrinfo(target_host, target_port, &hints, &res);
    if (status != 0) {
        std::cerr << "Błąd getaddrinfo: " << gai_strerror(status) << std::endl;
        return 1;
    }

    int sockfd = -1;
    bool connected = false;
    char servInfo[NI_MAXSERV]; 

    for (p = res; p != NULL; p = p->ai_next) {
        sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
        if (sockfd == -1) continue;

        if (connect(sockfd, p->ai_addr, p->ai_addrlen) == 0) {
            connected = true;

            int s = getnameinfo(p->ai_addr, p->ai_addrlen,
                                NULL, 0,               
                                servInfo, sizeof(servInfo), 
                                NI_NUMERICHOST);      

            if (s != 0) {
                strncpy(servInfo, "nieznana", sizeof(servInfo));
            }
            
            break;
        }

        close(sockfd);
    }

    if (connected) {
        std::cout << "[OTWARTY]  Host: " << target_host 
                  << " | Port: " << target_port 
                  << " | Usługa: " << servInfo << std::endl;
        close(sockfd);
    } else {
        std::cout << "[ZAMKNIĘTY] Host: " << target_host 
                  << " | Port: " << target_port << std::endl;
    }

    freeaddrinfo(res);
    return connected ? 0 : 1;
}
