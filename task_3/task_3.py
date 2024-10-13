import timeit
import requests


# Функція для завантаження тексту та обробки помилок
def fetch_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка статусу відповіді
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Помилка при завантаженні даних з URL: {e}")
        return None


# Текст 1, в якому будемо шукати
url1 = "https://drive.usercontent.google.com/u/0/uc?id=18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh&export=download"
text1 = fetch_text(url1)

# Текст 2, в якому будемо шукати
url2 = "https://drive.usercontent.google.com/u/0/uc?id=13hSt4JkJc11nckZZz2yoFHYL89a4XkMZ&export=download"
text2 = fetch_text(url2)

# Перевіряємо, чи завантажено текст перед продовженням
if not text1 or not text2:
    print("Не вдалося завантажити один з текстів. Перевірте URL.")
else:
    # Створення патернів для пошуку у тексті
    pattern_existing = "Алгоритми – це послідовність точно визначених дій"
    pattern_non_existing = "JavaScript"

    # Алгоритм Кнута-Морріса-Пратта
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1

        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        return lps

    def kmp_search(main_string, pattern):
        M = len(pattern)
        N = len(main_string)
        lps = compute_lps(pattern)
        i = j = 0

        while i < N:
            if pattern[j] == main_string[i]:
                i += 1
                j += 1
            elif j != 0:
                j = lps[j - 1]
            else:
                i += 1

            if j == M:
                return i - j

        return -1

    # Алгоритм Боєра-Мура
    def build_shift_table(pattern):
        table = {}
        length = len(pattern)
        for index, char in enumerate(pattern[:-1]):
            table[char] = length - index - 1
        table.setdefault(pattern[-1], length)
        return table

    def boyer_moore_search(text, pattern):
        shift_table = build_shift_table(pattern)
        i = 0
        while i <= len(text) - len(pattern):
            j = len(pattern) - 1
            while j >= 0 and text[i + j] == pattern[j]:
                j -= 1
            if j < 0:
                return i
            i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
        return -1

    # Алгоритм Рабіна-Карпа
    def polynomial_hash(s, base=256, modulus=101):
        n = len(s)
        hash_value = 0
        for i, char in enumerate(s):
            power_of_base = pow(base, n - i - 1) % modulus
            hash_value = (hash_value + ord(char) * power_of_base) % modulus
        return hash_value

    def rabin_karp_search(main_string, substring):
        substring_length = len(substring)
        main_string_length = len(main_string)
        base = 256
        modulus = 101
        substring_hash = polynomial_hash(substring, base, modulus)
        current_slice_hash = polynomial_hash(
            main_string[:substring_length], base, modulus
        )
        h_multiplier = pow(base, substring_length - 1) % modulus

        for i in range(main_string_length - substring_length + 1):
            if substring_hash == current_slice_hash:
                if main_string[i : i + substring_length] == substring:
                    return i
            if i < main_string_length - substring_length:
                current_slice_hash = (
                    current_slice_hash - ord(main_string[i]) * h_multiplier
                ) % modulus
                current_slice_hash = (
                    current_slice_hash * base + ord(main_string[i + substring_length])
                ) % modulus
                if current_slice_hash < 0:
                    current_slice_hash += modulus
        return -1

    # Функція для вимірювання часу виконання
    def measure_time(search_function):
        return timeit.timeit(search_function, number=100) / 100

    # Виведення результатів у табличному вигляді
    def print_results():
        print(
            f"|{'Pattern':<20}|{'Area':<10}|{'kmp_search, sec':<20}|{'boyer_moore, sec':<20}|{'rabin_karp, sec':<20}|"
        )
        print(
            "|--------------------|----------|--------------------|--------------------|--------------------|"
        )
        print(
            f"|{'Existing':<20}|{'text1':<10}|{measure_time(lambda: kmp_search(text1, pattern_existing)):<20.10f}|{measure_time(lambda: boyer_moore_search(text1, pattern_existing)):<20.10f}|{measure_time(lambda: rabin_karp_search(text1, pattern_existing)):<20.10f}|"
        )
        print(
            f"|{'Non-Existing':<20}|{'text1':<10}|{measure_time(lambda: kmp_search(text1, pattern_non_existing)):<20.10f}|{measure_time(lambda: boyer_moore_search(text1, pattern_non_existing)):<20.10f}|{measure_time(lambda: rabin_karp_search(text1, pattern_non_existing)):<20.10f}|"
        )
        print(
            "|--------------------|----------|--------------------|--------------------|--------------------|"
        )
        print(
            f"|{'Existing':<20}|{'text2':<10}|{measure_time(lambda: kmp_search(text2, pattern_existing)):<20.10f}|{measure_time(lambda: boyer_moore_search(text2, pattern_existing)):<20.10f}|{measure_time(lambda: rabin_karp_search(text2, pattern_existing)):<20.10f}|"
        )
        print(
            f"|{'Non-Existing':<20}|{'text2':<10}|{measure_time(lambda: kmp_search(text2, pattern_non_existing)):<20.10f}|{measure_time(lambda: boyer_moore_search(text2, pattern_non_existing)):<20.10f}|{measure_time(lambda: rabin_karp_search(text2, pattern_non_existing)):<20.10f}|"
        )

    # Виведення результатів
    print_results()
