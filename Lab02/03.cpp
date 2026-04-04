#include <iostream>
#include <sys/socket.h>
#include "TCPSocket.hpp"
#include <string>
#include <unistd.h>

int main(){

    TCPSocket socket;
    socket.create();
    socket.connectTo("127.0.0.1", 2900);
    
    std::string message;

    char buffer[128];
    while(true) {
        std::cin >> message;
        int bytesSent = write(socket.fd, message.c_str(), message.length());
        
        if (bytesSent < 0) {
            std::cerr << "Failed to send data\n";
            return 1;
        }

        // 2. RECEIVE data
        // Clear buffer first to be safe
        std::fill(buffer, buffer + 128, 0);

        int n = read(socket.fd, buffer, sizeof(buffer) - 1);

        if(n > 0){
            buffer[n] = '\0';
            std::cout << buffer << "\n";
        } else {
            std::cerr << "Failed to read data\n";
        }
    }
    return 0;
}
