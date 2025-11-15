import json
import csv
import zipfile
import os
from typing import Dict, List, Any
from pathlib import Path


class FileHandler:
    """Утилита для работы с файлами"""

    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """Чтение JSON файла"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any]):
        """Запись в JSON файл"""
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, str]]:
        """Чтение CSV файла"""
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)

    @staticmethod
    def write_csv(file_path: str, data: List[Dict[str, str]], fieldnames: List[str]):
        """Запись в CSV файл"""
        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def create_zip(zip_path: str, files: List[str]):
        """Создание ZIP архива"""
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in files:
                zipf.write(file, os.path.basename(file))

    @staticmethod
    def extract_zip(zip_path: str, extract_to: str):
        """Извлечение ZIP архива"""
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(extract_to)

    @staticmethod
    def list_zip_contents(zip_path: str) -> List[str]:
        """Список файлов в архиве"""
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            return zipf.namelist()
