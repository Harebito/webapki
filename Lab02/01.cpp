#include <iostream>
#include "DNSResolv.hpp"
#include "TCPSocket.hpp"
#include <string>
#include <sys/socket.h>
#include <unistd.h>

int main(){
    

    std::string ip = DNSResolv::resolve("time.nist.gov");
    if(ip.empty()) return 1;

    TCPSocket socket;
    socket.create();
    socket.connectTo(ip.c_str(), 13);
    
    char buffer[128];
    
    int n = read(socket.fd, buffer, sizeof(buffer) - 1);

    if(n > 0){
        buffer[n] = '\0';
        std::cout << "Czas: " << buffer << "\n";
    } else {
        std::cerr << "Failed to read data\n";
    }

    return 0;
}
