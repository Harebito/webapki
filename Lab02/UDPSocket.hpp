#ifndef UDP_SOCKET_HPP
#define UDP_SOCKET_HPP

#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

class UDPSocket {
public:
    int fd;

    UDPSocket() : fd(-1) {}

    ~UDPSocket() {
        if (fd != -1) close(fd);
    }

    void create() {
        // Note: SOCK_DGRAM is used for UDP
        if ((fd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
            perror("udp socket creation failed");
            exit(1);
        }
    }
    void connectTo(const char* ip, int port) {
    struct sockaddr_in servaddr;
    memset(&servaddr, 0, sizeof(servaddr));
    
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(port);
    inet_pton(AF_INET, ip, &servaddr.sin_addr);

    if (connect(fd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("Connect failed");
        exit(1);
    }
}
    // UDP doesn't "connect" in the same way, but we can set 
    // a default destination for sendto/recvfrom calls.
};

#endif
