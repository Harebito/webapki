#include <iostream>
#include <sys/socket.h>
#include "TCPSocket.hpp"
#include "DNSResolv.hpp"
#include <string>
#include <unistd.h>
#include <algorithm>

int main(){
    TCPSocket socket;
    socket.create();
    
    socket.connectTo("127.0.0.1", 2908);
    
    std::string message = "Hello Server!"; 
    
    const size_t MSG_LENGTH = 20;

    message.resize(MSG_LENGTH, ' ');

    std::cout << "Wysylam: [" << message << "] (dlugosc: " << message.length() << ")" << std::endl;

    int bytesSent = write(socket.fd, message.c_str(), MSG_LENGTH);
    
    if (bytesSent < 0) {
        std::cerr << "Failed to send data\n";
        return 1;
    }

    char buffer[MSG_LENGTH + 1]; 
    std::fill(buffer, buffer + MSG_LENGTH + 1, 0);

    int n = read(socket.fd, buffer, MSG_LENGTH);

    if(n > 0){
        buffer[n] = '\0';
        std::cout << "Odebrano: [" << buffer << "] (bajtow: " << n << ")\n";
    } else {
        std::cerr << "Failed to read data\n";
    }
    
    return 0;
}
