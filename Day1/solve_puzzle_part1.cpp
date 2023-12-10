#include <iostream>
#include <fstream>
#include <string>
#include <cctype>

int main() {
    std::ifstream file("input"); 
    std::string line;
    int sum = 0;


    if (file.is_open()) {
        while (std::getline(file, line)) {

            bool first_digit_found = false;
            std::string first_digit, last_digit;

            for (char c : line) {
                if (std::isdigit(c)) {
                    if (!first_digit_found) {
                        first_digit = c;
                        first_digit_found = true;
                    }
                    last_digit = c;
                }
            }

            if (first_digit_found) {
                std::string number_str;
                number_str += first_digit;
                number_str += last_digit;
                
                int number = std::stoi(number_str);
                sum += number;

                std::cout << "Number: " << number << std::endl;
            } else if (line.length() == 1) {
                std::cout << "Line:" << line << std::endl;
            } else {
                // No digits found
                std::cout << "No digits found in line: " << line << std::endl;
            }

        }
        file.close();
    } else {
        std::cerr << "Unable to open file" << std::endl;
    }

    std::cout << "Total sum: " << sum << std::endl;

    return 0;
}