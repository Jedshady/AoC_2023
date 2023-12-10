#include <iostream>
#include <fstream>
#include <vector>
#include <set>

bool isSymbol(char ch) {
    return ch != '.' && ch != '\n' && !isdigit(ch);
}

int exactNumber(const std::vector<std::string> &grid, 
                int x, 
                int y, 
                std::set<std::pair<int, int>> &counted) {
    std::string numberStr(1, grid[x][y]);
    // std::cout << "Number String: " << numberStr << std::endl;
    counted.insert({x, y});

    // Extend to the left
    int left = y - 1;
    while (left >= 0 && isdigit(grid[x][left])) {
        numberStr = grid[x][left] + numberStr;
        counted.insert({x, left});
        left--;
    }
    
    // Extend to the right
    int right = y + 1;
    while (right <= grid[x].size() && isdigit(grid[x][right])) {
        numberStr = numberStr + grid[x][right];
        counted.insert({x, right});
        right++;
    }

    return std::stoi(numberStr);
}

std::vector<std::string> readGridFromFile (const std::string& filename) {
    std::vector<std::string> grid;
    std::ifstream file(filename);
    std::string line;

    if (file.is_open()) {
        while (std::getline(file, line)) {
            grid.push_back(line);
        }
        file.close();
    } else {
        std::cerr << "Unable to open file for reading." << std::endl;
    }

    return grid;
}

int main() {
    std::string filename = "original_input";

    std::vector<std::string> grid = readGridFromFile(filename);

    std::set<std::pair<int, int>> counted;
    int totalSum = 0;

    for (int i = 0; i < grid.size(); i++) {
        for (int j = 0; j < grid[i].size(); j++) {
            // std::cout << "Row: " << i << " Column: " << j << std::endl;
            if (isSymbol(grid[i][j])) {
                std::cout << "Symbol: " << grid[i][j] << " at position {" << i << ", " << j << "}" << std::endl;
                for (int dx = -1; dx <= 1; dx++) {
                    for (int dy = -1; dy <= 1; dy++) {
                        int newX = i + dx;
                        int newY = j + dy;
                        if (newX >= 0 && newX <= grid.size() &&
                            newY >= 0 && newY <= grid[i].size() &&
                            isdigit(grid[newX][newY])) {
                                // std::cout << "Testing {X, Y}: {" << newX << ", " << newY << "}" << std::endl;
                                if (counted.find({newX, newY}) == counted.end()) {
                                    // std::cout << "Position is not in the set." << std::endl;
                                    int number = exactNumber(grid, newX, newY, counted);
                                    std::cout << "Number: " << number << " is valid." << std::endl;

                                    totalSum += number;
                                } 
                            }
                    }
                }
            }
        }
    }

    std::cout << "Total sum: " << totalSum << std::endl;

    return 0;
}