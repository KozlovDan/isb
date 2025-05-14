import json
import math
from func import *
from scipy.special import erfc, gammainc


def frequency_test(sequence: str) -> float:
    """
    Выполняет частотный тест для бинарной последовательности
    :param sequence: Бинарная строка для тестирования
    :return: P-значение частотного теста
    """
    n = len(sequence)
    sn = sum(1 if bit == '1' else -1 for bit in sequence) / math.sqrt(n)
    return erfc(abs(sn) / math.sqrt(2))


def runs_test(sequence):
    """
    Выполняет тест на одинаковые подряд идущие биты
    :param sequence: Бинарная строка для тестирования
    :return: P-значение теста
    """
    n = len(sequence)
    pi = sequence.count('1') / n

    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0

    vn = sum(1 for i in range(n - 1) if sequence[i] != sequence[i + 1])
    numerator = abs(vn - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    return erfc(numerator / denominator)


def longest_runs_test(sequence, PI: list, block_size=8):
    """
    Выполняет тест на самую длинную последовательность единиц в блоках.
    :param sequence: Бинарная строка для тестирования
    :param PI: Теоретические вероятности PI
    :param block_size: Размер блоков для разделения последовательности
    :return:
    """
    n = len(sequence)
    blocks = [sequence[i:i + block_size] for i in range(0, n, block_size)]

    v = [0] * 4
    for block in blocks:
        max_run = max(len(run) for run in block.split('0')) if '0' in block else block_size
        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    chi2 = sum(
        (v[i] - 16 * PI[i]) ** 2 / (16 * PI[i]) for i in
        range(4))
    return gammainc(1.5, chi2 / 2)


def main():
    try:
        config = open_json('config.json')

        cpp_sequence_txt = config["cpp_sequence"]
        java_sequence_txt = config["java_sequence"]
        test_results_cpp = config["cpp_results"]
        test_results_java = config["java_results"]
        PI = config["PI"]

        cpp_sequence = open_file(cpp_sequence_txt)
        java_sequence = open_file(java_sequence_txt)

        freq_test_cpp = frequency_test(cpp_sequence)
        runs_test_cpp = runs_test(cpp_sequence)
        longest_runs_test_cpp = longest_runs_test(cpp_sequence, PI)

        result_cpp_test = (f"CPP sequence: {cpp_sequence}\n\n"
                           f"Frequency bit test: {freq_test_cpp:.6f}\n"
                           f"Test for identical consecutive bits: {runs_test_cpp:.6f}\n"
                           f"Test for the longest sequence of ones in a block: {longest_runs_test_cpp:.6f}")

        save_file(test_results_cpp, result_cpp_test)

        freq_test_java = frequency_test(java_sequence)
        runs_test_java = runs_test(java_sequence)
        longest_runs_test_java = longest_runs_test(java_sequence, PI)

        result_java_test = (f"Java sequence: {java_sequence}\n\n"
                            f"Frequency bit test: {freq_test_java:.6f}\n"
                            f"Test for identical consecutive bits: {runs_test_java:.6f}\n"
                            f"Test for the longest sequence of ones in a block: {longest_runs_test_java:.6f}")

        save_file(test_results_java, result_java_test)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()