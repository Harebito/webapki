#include <iostream>
#include <string>
#include <sstream>
#include <vector>

bool ip_segment(const std::string& segment) {
    if (segment.empty() || segment.length() > 3) return false;

    for (char c : segment) {
        if (!isdigit(c)) return false;
    }

    int number = std::stoi(segment);
    if (number < 0 || number > 255) return false;

    if (segment.length() > 1 && segment[0] == '0') return false;

    return true;
}

bool czyPoprawneIP(const std::string& ip) {
    std::stringstream ss(ip);
    std::string segment;
    std::vector<std::string> segments;

    while (std::getline(ss, segment, '.')) {
        segments.push_back(segment);
    }

    if (segments.size() != 4) return false;

    if (ip.back() == '.') return false;

    for (const std::string& s : segments) {
        if (!ip_segment(s)) return false;
    }

    return true;
}

int main() {
    std::string ip;
    std::cout << "Podaj adres IP: ";
    std::cin >> ip;

    if (czyPoprawneIP(ip)) {
        std::cout << "Adres " << ip << " jest POPRAWNY.\n";
    } else {
        std::cout << "Adres " << ip << " jest NIEPOPRAWNY.\n";
    }

    return 0;
}
