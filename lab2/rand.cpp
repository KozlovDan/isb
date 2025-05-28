#include <iostream>
#include <bitset>
#include <cstdlib>
#include <ctime>

/**
 * @brief Генерирует и выводит псевдослучайную битовую последовательность длиной 128 бит
 * 
 * Программа использует стандартный генератор случайных чисел (rand()) 
 * для создания битовой последовательности. Каждый бит генерируется независимо 
 * с равной вероятностью.
 * 
 * @return int Код возврата
 */
int main() {
    srand(time(0));
    std::bitset<128> randomBits;
    
    for (int i = 0; i < 128; ++i) {
        randomBits[i] = rand() % 2;
    }
    
    std::cout << "Сгенерированная последовательность (128 бит):\n";
    std::cout << randomBits << std::endl;
    
    return 0;
}