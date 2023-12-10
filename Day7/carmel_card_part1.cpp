#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <vector>

using namespace std;

int getMaxOccurence(map<char, int> &card2count) {
    auto maxElement = max_element(card2count.begin(), card2count.end(),
        [](const std::pair<char, int>& a, const std::pair<char, int>& b) {
            return a.second < b.second;
        });

    return maxElement->second;
}

string determineType(const string &current_hand) {
    string current_type;

    map<char, int> card2count;
    for(char c : current_hand) {
        if (card2count.find(c) == card2count.end()) {
            card2count[c] = 1;
        } else {
            card2count[c] ++;
        }
    }

    if (card2count.size() == 1) {
        current_type = "Five_of_a_kind";
    } else if (card2count.size() == 2) {
        int maxOccurrence = getMaxOccurence(card2count);
        if (maxOccurrence == 4) {
            current_type = "Four_of_a_kind";
        } else if (maxOccurrence == 3) {
            current_type = "Full_house";
        }
    } else if (card2count.size() == 3) {
        int maxOccurrence = getMaxOccurence(card2count);
        if (maxOccurrence == 3) {
            current_type = "Three_of_a_kind";
        } else if (maxOccurrence == 2) {
            current_type = "Two_pair";
        }
    } else if (card2count.size() == 4) {
        current_type = "One_pair";
    } else {
        current_type = "High_card";
    }

    return current_type;
}

void classifyHand2Type(map<string, vector<pair<string, int>>> &type2hand, const string &line) {
    string current_hand = line.substr(0, line.find(' '));
    int current_bid = stoi(line.substr(line.find(' ') + 1));
    
    string hand_type = determineType(current_hand);

    cout << "Current hand: " << current_hand << " Current bid: " << current_bid << " Type: " << hand_type << endl;

    type2hand[hand_type].push_back(make_pair(current_hand, current_bid));
}

// Function to create a map for card rankings
map<char, int> createCardRankMap() {
    map<char, int> rankMap;
    const string ranks = "AKQJT98765432";
    int rank = ranks.size(); // Highest rank will have the highest value

    for (char c : ranks) {
        rankMap[c] = rank--;
    }

    return rankMap;
}

// Comparator that uses the card rank map
bool compareCards(const pair<std::string, int>& a, const pair<std::string, int>& b, const map<char, int>& rankMap) {
    for (size_t i = 0; i < min(a.first.size(), b.first.size()); ++i) {
        if (rankMap.at(a.first[i]) != rankMap.at(b.first[i])) {
            return rankMap.at(a.first[i]) < rankMap.at(b.first[i]);
        }
    }
    return a.first.size() > b.first.size(); // Longer string (more cards) is considered higher if ranks are equal
}


int sortHandAndGetSum(vector<pair<string, int>> &hand_in_type, const int starting_idx){
    map<char, int> cardRankMap = createCardRankMap();

    sort(hand_in_type.begin(), hand_in_type.end(), 
        [&cardRankMap](const auto& a, const auto& b){
            return compareCards(a, b, cardRankMap);
        });

    int sum = 0;
    for (size_t i = 0; i < hand_in_type.size(); i++) {
        const auto& item = hand_in_type[i];
        // cout << item.second << " " << i+starting_idx << endl;
        sum += item.second * (i + starting_idx);
    }
    return sum;
}

int main() {
    ifstream file("original_input");
    string line;

    map<string, vector<pair<string, int>>> type2hand; 
    if (file.is_open()) {
        while(getline(file, line)) {
            classifyHand2Type(type2hand, line);
        }
        file.close();
    }

    // for (const auto &entry : type2hand) {
    //     cout << entry.first << ": ";
    //     for (const auto &pair : entry.second) {
    //         cout << "(" << pair.first << ", " << pair.second << ") ";
    //     }
    //     cout << endl;
    // }
    
    int total_winning = 0;
    int winning_high_card = 0;
    int winning_one_pair = 0;
    int winning_two_pair = 0;
    int winning_three_of_a_kind = 0;
    int winning_full_house = 0;
    int winning_four_of_a_kind = 0;
    int winning_five_of_a_kind = 0;
    
    int current_idx = 0;

    if (type2hand.find("High_card") != type2hand.end()) {
        winning_high_card = sortHandAndGetSum(type2hand["High_card"], current_idx + 1);
        current_idx += type2hand["High_card"].size(); 
    }
    cout << "Winning from High Card: " << winning_high_card << endl;

    if (type2hand.find("One_pair") != type2hand.end()) {
        winning_one_pair = sortHandAndGetSum(type2hand["One_pair"], current_idx + 1);
        current_idx += type2hand["One_pair"].size(); 
    }
    cout << "Winning from One Pair: " << winning_one_pair << endl;

    if (type2hand.find("Two_pair") != type2hand.end()) {
        winning_two_pair = sortHandAndGetSum(type2hand["Two_pair"], current_idx + 1);
        // cout << "current idx: " << current_idx << endl;
        current_idx += type2hand["Two_pair"].size(); 
    }
    cout << "Winning from Two Pair: " << winning_two_pair << endl;

    if (type2hand.find("Three_of_a_kind") != type2hand.end()) {
        winning_three_of_a_kind = sortHandAndGetSum(type2hand["Three_of_a_kind"], current_idx + 1);
        current_idx += type2hand["Three_of_a_kind"].size(); 
    }
    cout << "Winning from Three of a Kind: " << winning_three_of_a_kind << endl;

    if (type2hand.find("Full_house") != type2hand.end()) {
        winning_full_house = sortHandAndGetSum(type2hand["Full_house"], current_idx + 1);
        current_idx += type2hand["Full_house"].size(); 
    }
    cout << "Winning from Full House: " << winning_full_house << endl;

    if (type2hand.find("Four_of_a_kind") != type2hand.end()) {
        winning_four_of_a_kind = sortHandAndGetSum(type2hand["Four_of_a_kind"], current_idx + 1);
        current_idx += type2hand["Four_of_a_kind"].size(); 
    }
    cout << "Winning from Four of a Kind: " << winning_four_of_a_kind << endl;

    if (type2hand.find("Five_of_a_kind") != type2hand.end()) {
        winning_five_of_a_kind = sortHandAndGetSum(type2hand["Five_of_a_kind"], current_idx + 1);
        current_idx += type2hand["Five_of_a_kind"].size(); 
    }
    cout << "Winning from Five of a Kind: " << winning_five_of_a_kind << endl;

    total_winning = winning_high_card + winning_one_pair + winning_two_pair + winning_three_of_a_kind +
        winning_full_house + winning_four_of_a_kind + winning_five_of_a_kind;
    
    cout << "Total Winning: " << total_winning << endl;

    return 0;
}