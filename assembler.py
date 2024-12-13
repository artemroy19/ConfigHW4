import argparse

# Функция для логирования операции
def log_operation(log_path, operation_code, B=None):
    if log_path:
        with open(log_path, "a", encoding="utf-8") as log_file:
            if B is not None:
                log_file.write(f"A={operation_code},B={B}\n")
            else:
                log_file.write(f"A={operation_code}\n")

# Функция для сериализации команды в бинарный формат
def serializer(cmd, fields, size):
    bits = cmd
    for value, offset in fields:
        bits |= (value << offset)
    return bits.to_bytes(size, "little")

# Основной ассемблер, который обрабатывает инструкции
def assembler(instructions, log_path=None):
    byte_code = []
    for operation, *args in instructions:
        if operation == "load":
            B = args[0]
            # Загрузка константы (команда load)
            byte_code += serializer(3, [(B, 3)], 3)  # Поле A: 3 бита, поле B: 16 бит, размер 3 байта
            log_operation(log_path, 3, B)
        elif operation == "read":
            B = args[0]
            # Чтение из памяти (команда read)
            byte_code += serializer(2, [(B, 3)], 2)  # Поле A: 3 бита, поле B: 11 бит, размер 2 байта
            log_operation(log_path, 2, B)
        elif operation == "write":
            B = args[0]
            # Запись в память (команда write)
            byte_code += serializer(6, [(B, 3)], 3)  # Поле A: 3 бита, поле B: 19 бит, размер 3 байта
            log_operation(log_path, 6, B)
        elif operation == "sgn":
            # Унарная операция (sgn)
            byte_code += serializer(4, [], 1)  # Поле A: 3 бита, размер 1 байт
            log_operation(log_path, 4)  # Логируем без B, так как для sgn B не используется
    return byte_code

# Функция для обработки инструкций из файла
def assemble(instructions_path: str, log_path=None):
    with open(instructions_path, "r", encoding="utf-8") as f:
        instructions = [[int(j) if j.isdigit() else j for j in i.split()] for i in f.readlines()]
    return assembler(instructions, log_path)

# Сохранение бинарного кода в файл
def save_to_bin(assembled_instructions, binary_path):
    with open(binary_path, "wb") as binary_file:
        binary_file.write(bytes(assembled_instructions))

# Основная функция для обработки командной строки
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembling the instructions file to the byte-code.")
    parser.add_argument("instructions_path", help="Path to the instructions file (txt)")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("log_path", help="Path to the log file (csv)")
    args = parser.parse_args()

    # Запись заголовка в лог-файл
    with open(args.log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"Operation code,Constant/Address\n")

    # Ассемблирование инструкций
    result = assemble(args.instructions_path, args.log_path)
    
    # Сохранение в бинарный файл
    save_to_bin(result, args.binary_path)
