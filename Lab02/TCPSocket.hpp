#ifndef TCP_SOCKET_HPP
#define TCP_SOCKET_HPP

#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

class TCPSocket {
public:
    int fd;

    TCPSocket() : fd(-1) {}

    ~TCPSocket() {
        if (fd != -1) close(fd);
    }

    void create() {
        if ((fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
            perror("socket creation failed");
            exit(1);
        }
    }

    void connectTo(const char* ip, int port) {
        struct sockaddr_in serv_addr;
        memset(&serv_addr, 0, sizeof(serv_addr));

        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(port);

        if (inet_pton(AF_INET, ip, &serv_addr.sin_addr) <= 0) {
            perror("invalid address");
            exit(1);
        }

        if (connect(fd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
            perror("connection failed");
            exit(1);
        }
    }
};

#endif
