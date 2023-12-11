#include <iostream>
#include <vector>
#include <cstdint>
#include <numeric>

using namespace std;

int main() {
    
    vector<uint64_t> numbers = {15871, 16409, 12643, 21251, 19637, 11567};

    uint64_t lcm = numbers[0];
    for (int i=1; i < numbers.size(); i++) {
        cout << lcm << ' ' << numbers[i] << endl;
        lcm = (lcm / gcd(lcm, numbers[i])) * numbers[i];
    }

    std::cout << "The LCM is: " << lcm << std::endl;

    return 0;
}