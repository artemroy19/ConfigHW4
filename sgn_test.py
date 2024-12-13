import unittest
import os
from assembler import assembler, save_to_bin
from interpreter import interpreter
import csv

class TestSGNOperations(unittest.TestCase):

    def setUp(self):
        """
        Выполняется перед каждым тестом.
        Подготавливаем тестовые данные.
        """
        self.vector = [-5, 10, -15, 20, -25, 30]
        self.binary_file = "sgn_test_binary.bin"
        self.result_file = "sgn_test_result.csv"
        self.log_file = "sgn_test_log.csv"

    def generate_sgn_instructions(self, vector):
        """
        Генерирует инструкции для применения операции sgn() к каждому элементу вектора.
        Результат записывается обратно в тот же вектор.
        """
        instructions = []

        for i in range(len(vector)):
            # Загружаем значение в аккумулятор
            instructions.append({
                "operation": "load",  # Операция загрузки
                "args": [vector[i]]    # Загружаем значение в аккумулятор
            })
            
            # Применяем операцию sgn
            instructions.append({
                "operation": "sgn",  # Операция sgn
                "args": []            # Применяем sgn()
            })
            
            # Записываем результат в память по индексу i
            instructions.append({
                "operation": "write",  # Операция записи
                "args": [i]            # Записываем результат обратно в вектор по индексу i
            })

        return instructions

    def test_generate_sgn_instructions(self):
        """
        Проверяем, что генерация инструкций для операции sgn() работает корректно.
        """
        instructions = self.generate_sgn_instructions(self.vector)

        # Проверяем, что количество инструкций соответствует количеству элементов вектора.
        self.assertEqual(len(instructions), len(self.vector) * 3)

        # Проверяем, что первые 3 инструкции для первого элемента
        self.assertEqual(instructions[0], {'operation': 'load', 'args': [-5]})
        self.assertEqual(instructions[1], {'operation': 'sgn', 'args': []})
        self.assertEqual(instructions[2], {'operation': 'write', 'args': [0]})

    def test_interpreter(self):
        """
        Тестируем выполнение интерпретатором сгенерированных инструкций.
        """
        # Генерация инструкций
        instructions = self.generate_sgn_instructions(self.vector)

        # Сохраняем инструкции в бинарный файл через ассемблер
        save_to_bin(assembler(instructions, self.log_file), self.binary_file)

        # Запускаем интерпретатор для выполнения
        interpreter(self.binary_file, self.result_file, (0, len(self.vector) - 1))

        # Проверяем результат в CSV файле
        with open(self.result_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            result = list(reader)

        # Пропускаем первую строку с заголовками
        result_data = result[1:]

        # Проверяем, что результат соответствует ожидаемому
        expected_result = [
            ("0", "0"), ("1", "0"), ("2", "0"), ("3", "0"), ("4", "0"), ("5", "0"),]

        for idx, (address, value) in enumerate(expected_result):
            self.assertEqual(result_data[idx][0], address)
            self.assertEqual(result_data[idx][1], value)

    def tearDown(self):
        """
        Выполняется после каждого теста. Удаляем временные файлы.
        """
        if os.path.exists(self.binary_file):
            os.remove(self.binary_file)
        if os.path.exists(self.result_file):
            os.remove(self.result_file)


if __name__ == "__main__":
    unittest.main()
