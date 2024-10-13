def binary_search(arr, target):
    """
    Функція для бінарного пошуку елемента в відсортованому масиві з дробовими числами.

    Parameters:
    arr (list): Відсортований масив для пошуку.
    target: Елемент, який шукаємо.

    Returns:
    tuple: Кортеж з кількості ітерацій і верхньої межі.
    """
    left = 0  # Ліва межа масиву
    right = len(arr) - 1  # Права межа масиву
    iterations = 0  # Лічильник ітерацій
    upper_bound = None  # Верхня межа (найменший елемент, більший або рівний target)

    while left <= right:
        mid = (left + right) // 2  # Знаходимо середину масиву
        iterations += 1  # Збільшуємо кількість ітерацій

        if arr[mid] == target:
            upper_bound = arr[mid]
            return (
                iterations,
                upper_bound,
            )  # Якщо знайдено шуканий елемент, повертаємо його індекс і кількість ітерацій
        elif arr[mid] < target:
            left = mid + 1  # Якщо шуканий елемент більший, зміщуємо ліву межу
        else:
            upper_bound = arr[mid]  # Оновлюємо верхню межу
            right = mid - 1  # Якщо шуканий елемент менший, зміщуємо праву межу

    # Якщо елемент не знайдено, повертаємо кількість ітерацій і верхню межу
    return iterations, upper_bound


# Приклад використання
array = [1.2, 3.5, 6.7, 8.9, 12.1, 15.6, 18.3, 20.5, 25.6, 30.8]
target = 17.0
result = binary_search(array, target)

print(f"Кількість ітерацій: {result[0]}, Верхня межа: {result[1]}")
