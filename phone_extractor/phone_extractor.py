#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import List, Set, Optional
from pathlib import Path
from loguru import logger


class PhoneExtractor:
    """
    Класс для извлечения телефонных номеров из текстового файла
    и преобразования их в единый формат.
    """

    def __init__(self, file_path: Optional[str] = None):
        """
        Инициализация экстрактора телефонных номеров.
        
        Args:
            file_path: Путь к текстовому файлу
        """
        self.file_path = file_path
        self.text_content = ""
        
        # Регулярное выражение для поиска номеров телефонов
        # Ищем различные форматы номеров: +7, 8, скобки, дефисы, пробелы и т.д.
        self.phone_pattern = re.compile(
            r'(?:\+7|8)[\s\-\.]?\(?(\d{3})\)?[\s\-\.]?(\d{3})[\s\-\.]?(\d{2})[\s\-\.]?(\d{2})'
            r'|'
            r'\+7[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{2}[\s\-\.]?\d{2}'
        )
        
        logger.info("PhoneExtractor инициализирован")
    
    def load_file(self, file_path: Optional[str] = None) -> None:
        """
        Загрузка содержимого текстового файла.
        
        Args:
            file_path: Путь к текстовому файлу
        """
        if file_path:
            self.file_path = file_path
            
        if not self.file_path:
            raise ValueError("Путь к файлу не указан")
            
        path = Path(self.file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {self.file_path}")
            
        logger.info(f"Загрузка файла: {self.file_path}")
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.text_content = file.read()
        
        logger.info(f"Файл загружен, размер содержимого: {len(self.text_content)} символов")
        
    def load_text(self, text: str) -> None:
        """
        Загрузка текста для извлечения номеров.
        
        Args:
            text: Строка с текстом
        """
        self.text_content = text
        logger.info(f"Загружен текст, размер: {len(self.text_content)} символов")
        
    def _normalize_phone(self, phone_match: re.Match) -> str:
        """
        Нормализация номера телефона в формат +7(YYY)XXX-XX-XX.
        
        Args:
            phone_match: Найденное совпадение регулярного выражения
            
        Returns:
            str: Номер телефона в формате +7(YYY)XXX-XX-XX
        """
        phone_str = phone_match.group(0)
        
        # Удаляем все нецифровые символы
        digits_only = re.sub(r'\D', '', phone_str)
        
        # Если номер начинается с 8, заменяем на 7
        if digits_only.startswith('8') and len(digits_only) == 11:
            digits_only = '7' + digits_only[1:]
            
        # Если номер не начинается с 7, это может быть не российский номер
        # или неполный номер - пропускаем
        if not digits_only.startswith('7') or len(digits_only) != 11:
            return ""
            
        # Форматируем номер в нужный вид
        return f"+{digits_only[0]}({digits_only[1:4]}){digits_only[4:7]}-{digits_only[7:9]}-{digits_only[9:11]}"
        
    def extract_phones(self) -> List[str]:
        """
        Извлечение телефонных номеров из текста.
        
        Returns:
            List[str]: Список уникальных номеров телефонов в формате +7(YYY)XXX-XX-XX
        """
        if not self.text_content:
            logger.warning("Текст для извлечения номеров не загружен")
            return []
            
        # Поиск всех совпадений регулярного выражения
        matches = self.phone_pattern.finditer(self.text_content)
        
        unique_phones: Set[str] = set()
        result_phones: List[str] = []
        
        for match in matches:
            normalized_phone = self._normalize_phone(match)
            if normalized_phone and normalized_phone not in unique_phones:
                unique_phones.add(normalized_phone)
                result_phones.append(normalized_phone)
                logger.debug(f"Найден номер: {normalized_phone}")
                
        logger.info(f"Всего найдено уникальных номеров: {len(result_phones)}")
        return result_phones


if __name__ == "__main__":
    import click
    
    @click.command()
    @click.argument('file_path', type=click.Path(exists=True))
    @click.option('--log-level', type=click.Choice(['DEBUG', 'INFO', 'WARNING']), default='INFO', 
                  help='Уровень логирования')
    def main(file_path: str, log_level: str) -> None:
        """
        Извлечение телефонных номеров из текстового файла.
        """
        # Настройка логирования
        logger.remove()
        logger.add(
            sink=lambda msg: click.echo(msg, err=True),
            level=log_level,
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
        )
        
        try:
            extractor = PhoneExtractor()
            extractor.load_file(file_path)
            phones = extractor.extract_phones()
            
            if phones:
                click.echo("Найденные номера телефонов:")
                for phone in phones:
                    click.echo(phone)
            else:
                click.echo("Номера телефонов не найдены")
                
        except Exception as e:
            logger.error(f"Ошибка при обработке файла: {e}")
            raise
    
    main() 