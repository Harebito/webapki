#include <iostream>
#include <string>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Użycie: " << argv[0] << " <adres_IP>" << std::endl;
        return 1;
    }

    std::string ip_address = argv[1];
    struct sockaddr_in sa;
    char hostname[NI_MAXHOST];

    if (inet_pton(AF_INET, ip_address.c_str(), &sa.sin_addr) != 1) {
        std::cerr << "Błąd: Nieprawidłowy format adresu IP." << std::endl;
        return 1;
    }

    sa.sin_family = AF_INET;

    int result = getnameinfo((struct sockaddr*)&sa, sizeof(sa), 
                             hostname, NI_MAXHOST, 
                             NULL, 0, NI_NAMEREQD);

    if (result != 0) {
        std::cerr << "Błąd: Nie udało się odnaleźć nazwy hosta (gai_error: " 
                  << gai_strerror(result) << ")" << std::endl;
        return 1;
    }

    std::cout << "Adres IP: " << ip_address << std::endl;
    std::cout << "Hostname: " << hostname << std::endl;

    return 0;
}
