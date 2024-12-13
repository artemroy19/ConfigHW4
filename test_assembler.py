import unittest
import io
from assembler import assembler, log_operation, serializer, save_to_bin

class TestAssembler(unittest.TestCase):
    
    def test_load_constant(self):
        """Тест для загрузки константы (A=3, B=42). Ожидаем 0x53, 0x01, 0x00"""
        instructions = [("load", 42)]
        expected_output = [0x53, 0x01, 0x00]
        
        # Запускаем ассемблер и проверяем результат
        result = assembler(instructions)
        
        self.assertEqual(result, expected_output)

    def test_read_value(self):
        """Тест для чтения значения из памяти (A=2, B=307). Ожидаем 0x9A, 0x09"""
        instructions = [("read", 307)]
        expected_output = [0x9A, 0x09]
        
        # Запускаем ассемблер и проверяем результат
        result = assembler(instructions)
        
        self.assertEqual(result, expected_output)

    def test_write_value(self):
        """Тест для записи значения в память (A=6, B=604). Ожидаем 0xE6, 0x12, 0x00"""
        instructions = [("write", 604)]
        expected_output = [0xE6, 0x12, 0x00]
        
        # Запускаем ассемблер и проверяем результат
        result = assembler(instructions)
        
        self.assertEqual(result, expected_output)

    def test_sgn_operation(self):
        """Тест для унарной операции sgn (A=4). Ожидаем 0x04"""
        instructions = [("sgn",)]
        expected_output = [0x04]
        
        # Запускаем ассемблер и проверяем результат
        result = assembler(instructions)
        
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
