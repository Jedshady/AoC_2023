#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <set>
#include <map>

int main() {
    std::ifstream file("original_input");
    std::string line;

    std::map<int, int> cardToCount = {{1, 1}};
    int totalPoints = 0;

    if (file.is_open()) {
        while(getline(file, line)) {
            std::istringstream iss(line);
            std::string token;

            getline(iss, token, ':');
            int cardNumber = std::stoi(token.substr(token.find(" ") + 1));
            std::cout << "Card Number: " << cardNumber << std::endl;

            if (cardToCount.find(cardNumber) == cardToCount.end()) {
                cardToCount.insert({cardNumber, 1});
            }

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
                    cardPoints ++; 
                }
            }
            std::cout << "Card Points: " << cardPoints << std::endl;

            int cardCount = cardToCount[cardNumber];
            for (int i = 1; i <= cardPoints; i++) {
                if (cardToCount.find(cardNumber+i) == cardToCount.end()) {
                    cardToCount.insert({cardNumber+i, 1});
                }
                cardToCount[cardNumber + i] += cardCount;
                std::cout << "Card " << cardNumber + i << " now has " << cardToCount[cardNumber + i] << " cards." << std::endl;
            }
        }

        file.close();
    } else {
        std::cerr << "Unable to open file" << std::endl;
    }

    for (const auto &pair : cardToCount) {
        int cardNumber = pair.first;
        int cardCount = pair.second;
        std::cout << "Card " << cardNumber << " has " << cardCount << " cards." << std::endl;
        totalPoints += cardCount;
    }

    std::cout << "Total Points: " << totalPoints << std::endl;

    return 0;
}