#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

int main() {
    std::ifstream file("original_input");
    std::string line;

    int sum = 0;

    if (file.is_open()) {
        while(getline(file, line)) {
            std::istringstream iss(line);
            std::string token;

            getline(iss, token, ':');
 
            int gameNumber = std::stoi(token.substr(token.find(" ") + 1));
            std::cout << "Game Number: " << gameNumber << std::endl;

            int maxRed = 0, maxBlue = 0, maxGreen = 0;
            
            while(getline(iss, token, ';')) {
                std::istringstream colorStream(token);
                std::string colorToken;

                while(colorStream >> token) {
                    int number = std::stoi(token);
                    colorStream >> colorToken;

                    if (colorToken.back() == ',') {
                        colorToken.pop_back();
                    }

                    if (colorToken == "red") {
                        maxRed = std::max(maxRed, number);
                    } else if (colorToken == "blue") {
                        maxBlue = std::max(maxBlue, number);
                    } else if (colorToken == "green") {
                        maxGreen = std::max(maxGreen, number);
                    }
                }
            }

            std::cout << "maxRed: " << maxRed << std::endl;
            std::cout << "maxBlue: "  << maxBlue << std::endl;
            std::cout << "maxGreen: " << maxGreen << std::endl;

            if (maxRed <= 12 && maxBlue <= 14 && maxGreen <= 13) {
                std::cout << "Game Number: " << gameNumber << " is valid." << std::endl;
                sum += gameNumber;
            }
        }
        file.close();
    } else {
        std::cerr << "Unable to open file" << std::endl;
    }

    std::cout << "Total sum: " << sum << std::endl;

    return 0;
}