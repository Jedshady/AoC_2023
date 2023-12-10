#include <iostream>
#include <fstream>
#include <string>
#include <cctype>
#include <map>

int main() {
    std::ifstream file("original_input");
    // std::ifstream file("corner_cases");

    std::string line;
    int sum = 0;


    if (file.is_open()) {
        while (std::getline(file, line)) {

            bool first_digit_found = false;
            std::string first_digit, last_digit;
            std::string temp;

            std::map<std::string, std::string> wordToNum = {
                {"one", "1"}, {"two", "2"}, {"three", "3"}, {"four", "4"},
                {"five", "5"}, {"six", "6"}, {"seven", "7"}, {"eight", "8"}, 
                {"nine", "9"}
            };

            for (char c : line) {                
                if (std::isalpha(c)) {
                    // Build the word
                    temp += c;
                    // std::cout << "Temp: " << temp << std::endl;
                    
                    std::string last3 = temp.length() >= 3 ? temp.substr(temp.length() - 3) : "";
                    std::string last4 = temp.length() >= 4 ? temp.substr(temp.length() - 4) : "";
                    std::string last5 = temp.length() >= 5 ? temp.substr(temp.length() - 5) : "";

                    if (wordToNum.find(last3) != wordToNum.end()) {
                        std::string digit = wordToNum[last3];
                        // std::cout << "Last3: " << digit << std::endl;
                        
                        if (!first_digit_found) {
                            first_digit = digit;
                            first_digit_found = true;
                        }
                        last_digit = digit;
                    } else if (wordToNum.find(last4) != wordToNum.end()) {
                        std::string digit = wordToNum[last4];
                        // std::cout << "Last4: " << digit << std::endl;
                        
                        if (!first_digit_found) {
                            first_digit = digit;
                            first_digit_found = true;
                        }
                        last_digit = digit;
                    } else if (wordToNum.find(last5) != wordToNum.end()) {
                        std::string digit = wordToNum[last5];                        
                        // std::cout << "Last5: " << digit << std::endl;

                        if (!first_digit_found) {
                            first_digit = digit;
                            first_digit_found = true;
                        }
                        last_digit = digit;
                    }
                }
               
                if (std::isdigit(c) || !std::isalpha(c) || &c == &line.back()) {
                    // Process the digit if c is a digit
                    if (std::isdigit(c)) {
                       if (!first_digit_found) {
                            first_digit = c;
                            first_digit_found = true;
                        }
                        last_digit = c; 
                    }
                    temp.clear();
                }
                // std::cout << "First digit: " << first_digit << std::endl;
                // std::cout << "Last digit: " << last_digit << std::endl;
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