#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdio.h>

// Zwraca 0 w przypadku sukcesu, -1 w przypadku błędu
int lookup_hostname(const char *ip_str, char *buffer, size_t buffer_len) {
    struct sockaddr_in sa;
    memset(&sa, 0, sizeof(sa));
    sa.sin_family = AF_INET;
    
    // Konwersja stringa IP na postać binarną
    if (inet_pton(AF_INET, ip_str, &sa.sin_addr) <= 0) return -1;

    // Pobieranie nazwy hosta
    if (getnameinfo((struct sockaddr*)&sa, sizeof(sa), 
                    buffer, buffer_len, 
                    NULL, 0, NI_NAMEREQD) != 0) {
        return -1;
    }
    return 0;
}
