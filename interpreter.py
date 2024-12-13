import argparse
import csv

# Функция для выполнения операции sgn()
def sgn(value):
    """Унарная операция sgn: меняет знак значения в аккумуляторе."""
    if value > 0:
        return 1
    elif value < 0:
        return -1
    return 0

# Интерпретатор
def interpreter(binary_path, result_path, memory_range):
    # Инициализация памяти и регистров
    memory = [0] * 64   # Память из 64 ячеек
    register = 0        # Регистр аккумулятор (A)

    # Чтение бинарного файла
    with open(binary_path, "rb") as binary_file:
        byte_code = binary_file.read()

    i = 0
    prev_memory = memory.copy()
    prev_register = register
    while i < len(byte_code):
        # Извлекаем код операции (первые 3 бита)
        opcode = byte_code[i] & 0x07  # Биты 0-2 для кода операции
        
        if opcode == 3:  # load (Загрузка константы)
            # Извлекаем константу (биты 3-18), два байта
            B = int.from_bytes(byte_code[i+1:i+3], "little")  # Биты 3-18 (константа)
            register = B  # Загружаем константу в аккумулятор
            i += 3  # Переход к следующей команде

        elif opcode == 2:  # read (Чтение значения из памяти)
            # Извлекаем смещение (биты 3-13), один байт
            B = byte_code[i+1]  # Биты 3-13 (смещение), считываем 1 байт
            address = register + B  # Адрес = регистр + смещение
            if 0 <= address < len(memory):
                register = memory[address]  # Читаем из памяти в регистр
            i += 2  # Переход к следующей команде

        elif opcode == 6:  # write (Запись значения в память)
            # Извлекаем адрес (биты 3-22), два байта
            B = int.from_bytes(byte_code[i+1:i+3], "little")  # Биты 3-22 (адрес)
            if 0 <= B < len(memory):
                memory[B] = register  # Записываем в память по адресу
            i += 3  # Переход к следующей команде

        elif opcode == 4:  # sgn (Унарная операция: sgn)
            register = sgn(register)  # Применяем операцию sgn
            i += 1  # Переход к следующей команде

        else:
            raise ValueError(f"Неизвестная команда: {opcode}")

        # Печать состояния только если произошло изменение
        if memory != prev_memory or register != prev_register:
            prev_memory = memory.copy()
            prev_register = register

    # Запись результатов в CSV файл
    with open(result_path, "w", encoding="utf-8", newline='') as result_file:
        writer = csv.writer(result_file)
        writer.writerow(["Address", "Value"])
        for address in range(memory_range[0], memory_range[1] + 1):
            writer.writerow([address, memory[address]])


# Основная функция для обработки аргументов командной строки
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Интерпретатор для бинарного кода.")
    parser.add_argument("binary_path", help="Путь к бинарному файлу с байт-кодом")
    parser.add_argument("result_path", help="Путь к результирующему CSV файлу")
    parser.add_argument("first_index", type=int, help="Первый индекс памяти для вывода")
    parser.add_argument("last_index", type=int, help="Последний индекс памяти для вывода")
    args = parser.parse_args()

    # Запуск интерпретатора
    interpreter(args.binary_path, args.result_path, (args.first_index, args.last_index))
