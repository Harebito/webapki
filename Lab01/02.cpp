#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::string fname;

    std::cout << "File name: ";
    std::cin >> fname;

    std::ifstream source_file(fname, std::ios::binary);

    if (!source_file.is_open()) {
        std::cerr << "Can't open source file " << fname << "\n";
        return 1;
    }

    std::ofstream dest_file("lab1zad1.png", std::ios::binary);

    if (!dest_file.is_open()) {
        std::cerr << "Can't create file\n";
        source_file.close();
        return 2;
    }
    dest_file << source_file.rdbuf();

    source_file.close();
    dest_file.close();

    return 0;
}
