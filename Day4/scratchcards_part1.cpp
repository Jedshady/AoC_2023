#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <set>

int main() {
    std::ifstream file("original_input");
    std::string line;

    int totalPoints = 0;

    if (file.is_open()) {
        while(getline(file, line)) {
            std::istringstream iss(line);
            std::string token;

            getline(iss, token, ':');
            int cardNumber = std::stoi(token.substr(token.find(" ") + 1));
            std::cout << "Card Number: " << cardNumber << std::endl;

            std::set<int> winningNumbers;
            getline(iss, token, '|');
            // std::cout << "Winning Numbers are: " << token << std::endl;

            std::istringstream winNumberStream(token);
            while(winNumberStream >> token) {
                winningNumbers.insert(std::stoi(token));
            }

            getline(iss, token);
            std::istringstream cardNumberStream(token);
            int cardPoints = 0;
            while(cardNumberStream >> token) {
                if (winningNumbers.find(std::stoi(token)) != winningNumbers.end()) {
                    cardPoints = cardPoints == 0? cardPoints + 1: cardPoints * 2;
                }
            }
            std::cout << "Card Points: " << cardPoints << std::endl;
            totalPoints += cardPoints;
        }

        file.close();
    } else {
        std::cerr << "Unable to open file" << std::endl;
    }

    std::cout << "Total Points: " << totalPoints << std::endl;

    return 0;
}