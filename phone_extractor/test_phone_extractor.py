#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from phone_extractor import PhoneExtractor


class TestPhoneExtractor(unittest.TestCase):
    """Тесты для класса PhoneExtractor."""

    def setUp(self):
        """Подготовка к тестам."""
        self.extractor = PhoneExtractor()

    def test_extract_common_formats(self):
        """Тест извлечения телефонов в стандартных форматах."""
        text = """
        Связаться с нами можно по телефону +7 912-345-67-89 или 8 (495) 123 45 67.
        Также работает WhatsApp: +7(903) 456 78 90.
        """
        self.extractor.load_text(text)
        phones = self.extractor.extract_phones()

        expected = [
            "+7(912)345-67-89",
            "+7(495)123-45-67",
            "+7(903)456-78-90"
        ]
        
        self.assertEqual(phones, expected)

    def test_extract_unusual_formats(self):
        """Тест извлечения телефонов в нестандартных форматах."""
        text = """
        Звоните по номеру 8 (900) 123 45 67 или +7-900-123-45-67.
        А ещё есть +7 (999) 888.77.66 — это второй номер.
        """
        self.extractor.load_text(text)
        phones = self.extractor.extract_phones()

        expected = [
            "+7(900)123-45-67",
            "+7(999)888-77-66"
        ]
        
        self.assertEqual(phones, expected)

    def test_extract_duplicates(self):
        """Тест обработки дубликатов номеров."""
        text = """
        Первый номер: +7 912-345-67-89
        Второй номер: 8 (912) 345 67 89
        """
        self.extractor.load_text(text)
        phones = self.extractor.extract_phones()

        expected = ["+7(912)345-67-89"]
        
        self.assertEqual(phones, expected)

    def test_extract_incomplete_numbers(self):
        """Тест обработки неполных номеров."""
        text = """
        Иногда оставляют так: 8-900-111-22
        А вот и еще: +74991234ABCD
        """
        self.extractor.load_text(text)
        phones = self.extractor.extract_phones()

        # Эти номера не должны быть извлечены, так как они неполные или содержат нецифровые символы
        self.assertEqual(phones, [])

    def test_empty_text(self):
        """Тест обработки пустого текста."""
        self.extractor.load_text("")
        phones = self.extractor.extract_phones()
        
        self.assertEqual(phones, [])


if __name__ == "__main__":
    unittest.main() 