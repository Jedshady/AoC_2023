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
            }        
        }
        file.close();
    }

    cout << "Instructions: " << instructions << endl;
    for (const auto &entry : navigation) {
        cout << entry.first << ": ";
        const auto &pair = entry.second;
        cout << "(" << pair.first << ", " << pair.second << ") " << endl;
    }

    string start_point = "GJZ";
    
    regex end_point_pattern("^[A-Z1-9]{2}Z$");
    int total_step = 0;

    // cout << instructions.size() << endl;
    for (int i = 0; i < instructions.size(); i++) {
        cout << "i: " << i << " At: " << start_point << " Instruction: " << instructions[i] << endl;
        if (instructions[i] == 'L') {
            if (regex_match(navigation[start_point].first, end_point_pattern)) {
                cout << navigation[start_point].first << endl;
                total_step ++;
                break;
            }

            start_point = navigation[start_point].first;
            total_step ++;

        } else if (instructions[i] == 'R') {
            if (regex_match(navigation[start_point].second, end_point_pattern)) {
                cout << navigation[start_point].second << endl;
                total_step ++;
                break;
            }

            start_point = navigation[start_point].second;
            total_step ++;
        }

        cout << "New start point: " << start_point << endl;

        if (i == instructions.size() - 1) {
            cout << "Reach the end of the instruction. Do it all over again." << endl;
            i = -1;
        }
    }    
    
    cout << "Total step: " << total_step << endl;

    return 0;
}