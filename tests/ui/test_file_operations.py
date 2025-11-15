import pytest
import allure
import os
import tempfile
from utils.file_handler import FileHandler


@allure.epic("Тестирование работы с файлами")
@allure.feature("Файловые операции")
class TestFileOperations:
    """Тесты для работы с файлами"""

    @allure.story("JSON файлы")
    @allure.title("Чтение JSON файла с тестовыми данными")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("files", "regression")
    @pytest.mark.regression
    def test_read_json_file(self):
        """Тест: Чтение JSON файла с тестовыми данными"""
        with allure.step("Чтение JSON файла"):
            test_data_path = "tests/resources/test_data.json"
            data = FileHandler.read_json(test_data_path)
        
        with allure.step("Проверка структуры данных"):
            assert "books" in data, "Отсутствует ключ 'books'"
            assert "test_users" in data, "Отсутствует ключ 'test_users'"
        
        with allure.step("Проверка количества книг"):
            assert len(data["books"]) > 0, "Список книг пустой"
        
        with allure.step("Проверка полей книги"):
            first_book = data["books"][0]
            required_fields = ["id", "title", "author", "price"]
            for field in required_fields:
                assert field in first_book, f"Отсутствует поле '{field}'"
        
        # Прикрепляем файл к Allure отчету
        with open(test_data_path, 'r', encoding='utf-8') as f:
            allure.attach(
                f.read(),
                name="test_data.json",
                attachment_type=allure.attachment_type.JSON
            )

    @allure.story("JSON файлы")
    @allure.title("Запись и чтение JSON файла")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("files", "regression")
    @pytest.mark.regression
    def test_write_and_read_json(self):
        """Тест: Запись и чтение JSON файла"""
        test_data = {
            "cart_items": [
                {"id": 1, "title": "Test Book 1"},
                {"id": 2, "title": "Test Book 2"}
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            temp_file_path = tmp_file.name
        
        try:
            with allure.step("Запись данных в JSON файл"):
                FileHandler.write_json(temp_file_path, test_data)
            
            with allure.step("Чтение данных из JSON файла"):
                read_data = FileHandler.read_json(temp_file_path)
            
            with allure.step("Проверка что данные совпадают"):
                assert read_data == test_data, "Данные не совпадают"
        
        finally:
            os.unlink(temp_file_path)

    @allure.story("CSV файлы")
    @allure.title("Запись и чтение CSV файла")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("files", "regression")
    @pytest.mark.regression
    def test_csv_operations(self):
        """Тест: Работа с CSV файлами"""
        test_data = [
            {"id": "1", "title": "Book 1", "author": "Author 1"},
            {"id": "2", "title": "Book 2", "author": "Author 2"}
        ]
        fieldnames = ["id", "title", "author"]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            temp_file_path = tmp_file.name
        
        try:
            with allure.step("Запись данных в CSV файл"):
                FileHandler.write_csv(temp_file_path, test_data, fieldnames)
            
            with allure.step("Чтение данных из CSV файла"):
                read_data = FileHandler.read_csv(temp_file_path)
            
            with allure.step("Проверка количества записей"):
                assert len(read_data) == len(test_data), "Количество записей не совпадает"
            
            with allure.step("Проверка содержимого"):
                for i, row in enumerate(read_data):
                    assert row == test_data[i], f"Строка {i} не совпадает"
        
        finally:
            os.unlink(temp_file_path)

    @allure.story("ZIP архивы")
    @allure.title("Создание и чтение ZIP архива")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("files", "regression")
    @pytest.mark.regression
    def test_zip_operations(self):
        """Тест: Работа с ZIP архивами"""
        # Создаем временные файлы
        temp_files = []
        for i in range(3):
            tmp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
            tmp_file.write(f"Test content {i}")
            tmp_file.close()
            temp_files.append(tmp_file.name)
        
        zip_path = tempfile.mktemp(suffix='.zip')
        extract_dir = tempfile.mkdtemp()
        
        try:
            with allure.step("Создание ZIP архива"):
                FileHandler.create_zip(zip_path, temp_files)
            
            with allure.step("Проверка содержимого архива"):
                contents = FileHandler.list_zip_contents(zip_path)
                assert len(contents) == 3, f"Ожидалось 3 файла, получено {len(contents)}"
            
            with allure.step("Извлечение архива"):
                FileHandler.extract_zip(zip_path, extract_dir)
            
            with allure.step("Проверка извлеченных файлов"):
                extracted_files = os.listdir(extract_dir)
                assert len(extracted_files) == 3, "Не все файлы извлечены"
        
        finally:
            # Удаляем временные файлы
            for f in temp_files:
                if os.path.exists(f):
                    os.unlink(f)
            if os.path.exists(zip_path):
                os.unlink(zip_path)
            import shutil
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)

    @allure.story("Параметризация")
    @allure.title("Чтение книг из JSON с параметризацией")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("files", "regression")
    @pytest.mark.regression
    @pytest.mark.parametrize("book_index", [0, 1, 2])
    def test_read_books_parametrized(self, book_index):
        """Тест: Чтение конкретной книги из JSON файла"""
        with allure.step("Чтение JSON файла"):
            test_data_path = "tests/resources/test_data.json"
            data = FileHandler.read_json(test_data_path)
        
        with allure.step(f"Получение книги с индексом {book_index}"):
            book = data["books"][book_index]
        
        with allure.step("Проверка полей книги"):
            assert "id" in book, "Отсутствует поле 'id'"
            assert "title" in book, "Отсутствует поле 'title'"
            assert "author" in book, "Отсутствует поле 'author'"
            assert "price" in book, "Отсутствует поле 'price'"
        
        with allure.step(f"Проверка что цена > 0"):
            assert book["price"] > 0, f"Цена книги должна быть больше 0"
