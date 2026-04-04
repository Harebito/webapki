#ifndef DNS_RESOLV_HPP
#define DNS_RESOLV_HPP

#include <netdb.h>
#include <arpa/inet.h>
#include <string>
#include <stdio.h>

class DNSResolv {
public:
    // Forward Lookup
    static std::string resolve(const char* hostname) {
        struct hostent *he = gethostbyname(hostname);
        if (!he) {
            herror("gethostbyname");
            return "";
        }
        return std::string(inet_ntoa(*(struct in_addr*)he->h_addr));
    }

    // Reverse Lookup
    static std::string reverse(const char* ip_address) {
        struct in_addr addr;
        // 1. Convert string "8.8.8.8" into binary address
        if (inet_pton(AF_INET, ip_address, &addr) <= 0) {
            return "invalid ip";
        }

        // 2. Call the reverse function
        struct hostent *he = gethostbyaddr((const char*)&addr, sizeof(addr), AF_INET);
        if (!he) {
            herror("gethostbyaddr");
            return "unknown host";
        }

        return std::string(he->h_name);
    }
};

#endif
