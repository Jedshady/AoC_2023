#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <map>

using namespace std;


int main() {
    ifstream file("original_input");
    // ifstream file("test_input_2");
    string line;

    string instructions;

    map<string, pair<string, string>> navigation;
    vector<string> point_ending_A;

    if (file.is_open()) {
        while(getline(file, line)) {
            if (!line.empty() && line.find('=') == string::npos) {
                instructions = line;
            } else if ( !line.empty() ) {
                string key = line.substr(0, line.find('=') - 1);
                string value = line.substr(line.find('=') + 1);

                // cout << "Value: " << value << endl;

                size_t startPos = value.find('(') + 1;
                size_t endPos = value.find(')', startPos);
                value = value.substr(startPos, endPos - startPos);

                size_t comma_pos = value.find(',');
                string first = value.substr(0, comma_pos);
                string second = value.substr(comma_pos + 2);

                // cout << "Key: " << key << " First: " << first << " Second: " << second << endl;              
                
                navigation[key] = make_pair(first, second);

                // If key ends in A, add it to point_ending_A
                regex pattern("^[A-Z1-9]{2}A$");

                if (regex_match(key, pattern)) {
                    point_ending_A.push_back(key);
                }
            }        
        }
        file.close();
    }

    // Test input is parsed fine
    cout << "Instructions: " << instructions << endl;
    cout << "Point ending in A: ";
    for (const string& point : point_ending_A) {
        cout << point << " ";
    }
    cout << endl;

    // for (const auto &entry : navigation) {
    //     cout << entry.first << ": ";
    //     const auto &pair = entry.second;
    //     cout << "(" << pair.first << ", " << pair.second << ") " << endl;
    // }

    string start_point;
    regex end_point_pattern("^[A-Z1-9]{2}Z$");

    bool all_reach_Z = true;
    
    vector<string> current_point = point_ending_A;
    vector<string> next_point;
    int total_step = 0;

    for (int i = 0; i < instructions.size(); i++) {    
    // for (int i = 0; i < instructions.size() && total_step < 1; i++) {    
        for (string& point : current_point) {
            // cout << "i: " << i << " At: " << point << " Instruction: " << instructions[i] << " Navigation: (" << navigation[point].first << ", " << navigation[point].second << ')' << endl;
            if (instructions[i] == 'L') {
                next_point.push_back(navigation[point].first);
            } else if (instructions[i] == 'R') {
                next_point.push_back(navigation[point].second);
            }
        } 
        
        current_point = next_point;
        next_point.clear();
        total_step ++;

        // cout << "Current point: ";
        for (const string& cur : current_point) {
            // cout << cur << " ";
            if (!regex_match(cur, end_point_pattern)) {
                all_reach_Z = false;
            }
        }
        // cout << endl;
        
        if (all_reach_Z) {
            break;
        } else {
            all_reach_Z = true;
        } 
        
        if (i == instructions.size() - 1) {
            cout << "Reach the end of the instruction. Do it all over again." << endl;
            cout << "Total step: " << total_step << endl;
            i = -1;
        }
    }
    
    cout << "Total step: " << total_step << endl;

    return 0;
}