# import pytest
# from typing import List
#
# # Импортируем классы (предполагаем, что они в файле category.py)
# from src.category_ import Product, Category
#
#
# class TestProduct:
#     def test_product_initialization(self):
#         """Проверяем корректную инициализацию Product."""
#         product = Product(
#             name="Тест-товар",
#             description="Описание теста",
#             price=100.50,
#             quantity=10
#         )
#
#         assert product.name == "Тест-товар"
#         assert product.description == "Описание теста"
#         assert product.price == 100.50
#         assert product.quantity == 10
#
#     def test_product_types(self):
#         """Проверяем типы атрибутов Product."""
#         product = Product("Товар", "Описание", 50.0, 5)
#
#         assert isinstance(product.name, str)
#         assert isinstance(product.description, str)
#         assert isinstance(product.price, float)
#         assert isinstance(product.quantity, int)
#
#
# class TestCategory:
#     def test_setup_method(self):
#         """Очищаем счётчики перед каждым тестом."""
#         Category.total_categories = 0
#         Category.total_products = 0
#
#     def test_category_initialization(self):
#         """Проверяем корректную инициализацию Category."""
#         category = Category(
#             name="Тесты",
#             description="Категория для тестирования"
#         )
#
#         assert category.name == "Тесты"
#         assert category.description == "Категория для тестирования"
#         assert isinstance(category.products, list)
#         assert len(category.products) == 0
#
#     def test_total_categories_counter(self):
#         """Проверяем подсчёт количества категорий."""
#         cat1 = Category("Кат1", "Описание 1")
#         cat2 = Category("Кат2", "Описание 2")
#
#         assert Category.total_categories == 2
#
#     def test_add_product_updates_counter(self):
#         """Проверяем, что добавление товара увеличивает счётчик."""
#         category = Category("Товары", "Описание")
#         product = Product("Продукт", "Описание", 10.0, 1)
#
#         category.add_product(product)
#
#         assert len(category.products) == 1
#         assert Category.total_products == 1
#
#     def test_remove_product_decreases_counter(self):
#         """Проверяем, что удаление товара уменьшает счётчик."""
#         category = Category("Товары", "Описание")
#         product = Product("Продукт", "Описание", 10.0, 1)
#
#         category.add_product(product)
#         category.remove_product(product)
#
#         assert len(category.products) == 0
#         assert Category.total_products == 0
#
#     def test_multiple_categories_product_count(self):
#         """Проверяем общий счётчик товаров в нескольких категориях."""
#         cat1 = Category("Кат1", "Описание")
#         cat2 = Category("Кат2", "Описание")
#
#         p1 = Product("P1", "Desc", 1.0, 1)
#         p2 = Product("P2", "Desc", 2.0, 2)
#         p3 = Product("P3", "Desc", 3.0, 3)
#
#         cat1.add_product(p1)
#         cat1.add_product(p2)
#         cat2.add_product(p3)
#
#         assert Category.total_products == 3
#         assert len(cat1.products) == 2
#         assert len(cat2.products) == 1
import unittest
from unittest.mock import patch, MagicMock
from typing import List


# Импортируем ваши классы (предполагаем, что они в category.py)
from src.category_  import Product, Category



class TestProduct(unittest.TestCase):
    def test_product_init(self):
        """Проверяет инициализацию Product."""
        product = Product("Ноутбук", "Игровой", 79999.99, 3)
        self.assertEqual(product.name, "Ноутбук")
        self.assertEqual(product.description, "Игровой")
        self.assertEqual(product.price, 79999.99)
        self.assertEqual(product.quantity, 3)



class TestCategory(unittest.TestCase):
    def setUp(self):
        """Сброс счётчиков перед каждым тестом."""
        Category.total_categories = 0
        Category.total_products = 0

    def test_category_init(self):
        """Проверяет инициализацию Category."""
        category = Category("Электроника", "Гаджеты", [])
        self.assertEqual(category.name, "Электроника")
        self.assertEqual(category.description, "Гаджеты")
        self.assertIsInstance(category.products, list)
        self.assertEqual(len(category.products), 0)
        self.assertEqual(Category.total_categories, 1)

    def test_add_product_increments_counter(self):
        """Проверяет, что add_product увеличивает total_products."""
        category = Category("Книги", "Художественная литература", [])
        product = Product("Война и мир", "Роман", 899.00, 7)

        with patch.object(Category, 'total_products', new_callable=MagicMock) as mock_counter:
            mock_counter.__get__ = MagicMock(return_value=0)
            mock_counter.__set__ = MagicMock()


            category.add_product(product)

            # Проверяем, что счётчик увеличился на 1
            self.assertEqual(mock_counter.__set__.call_count, 1)
            args, _ = mock_counter.__set__.call_args
            self.assertEqual(args[1], 1)  # новое значение счётчика


    @patch.object(Category, 'total_products')
    def test_remove_product_decrements_counter(self, mock_total_products):
        """Проверяет, что remove_product уменьшает total_products."""
        mock_total_products.__get__ = MagicMock(return_value=1)
        mock_total_products.__set__ = MagicMock()


        category = Category("Спорт", "Инвентарь", [])
        product = Product("Мяч", "Футбольный", 1490.00, 5)
        category.add_product(product)  # теперь total_products = 1 (по логике)


        category.remove_product(product)

        # Проверяем, что счётчик уменьшился
        self.assertEqual(mock_total_products.__set__.call_count, 1)
        args, _ = mock_total_products.__set__.call_args
        self.assertEqual(args[1], 0)  # новое значение счётчика


    def test_remove_product_not_in_list_no_error(self):
        """Проверяет удаление товара, которого нет в списке — без ошибок."""
        category = Category("Техника", "Бытовая техника", [])
        product = Product("Чайник", "Электрический", 2490.00, 8)


        # Не добавляем в категорию — пытаемся удалить
        category.remove_product(product)


        self.assertEqual(len(category.products), 0)
        self.assertEqual(Category.total_products, 0)


    @patch('builtins.print')  # Мокируем print, если в коде есть отладочные print
    def test_add_product_calls_append(self, mock_print):
        """Проверяет, что add_product вызывает list.append."""
        category = Category("Игры", "Видеоигры", [])
        product = Product("The Witcher 3", "RPG", 1299.00, 100)


        # Мокируем список products, чтобы отследить вызов append
        mock_products = MagicMock()
        mock_products.append = MagicMock()
        category.products = mock_products

        category.add_product(product)

        # Проверяем, что был вызван append
        self.assertTrue(mock_products.append.called)
        args, _ = mock_products.append.call_args
        self.assertEqual(args[0], product)

    def test_total_categories_increments_on_init(self):
        """Проверяет, что total_categories растёт при создании категории."""
        cat1 = Category("Еда", "Продукты", [])
        cat2 = Category("Мебель", "Для дома", [])


        self.assertEqual(Category.total_categories, 2)


    @patch.object(Product, '__init__', return_value=None)
    def test_category_with_products_init_calls_product_init(self, mock_product_init):
        """
        Проверяет, что при передаче списка продуктов в __init__ Category,
        не происходит лишних вызовов __init__ у Product (продукты уже созданы).
        """
        p1 = Product("Товар1", "Описание1", 100.0, 5)
        p2 = Product("Товар2", "Описание2", 200.0, 3)

        # Создаём категорию с уже готовыми продуктами
        category = Category("Товары", "Разные товары", [p1, p2])

        # Убеждаемся, что __init__ Product не вызывался повторно
        self.assertFalse(mock_product_init.called)

    def test_isolation_between_categories(self):
        """Проверяет изоляцию между разными категориями."""
        cat1 = Category("Игры", "Видеоигры", [])
        cat2 = Category("Фильмы", "DVD", [])

        p1 = Product("The Witcher 3", "RPG", 1299.00, 100)
        p2 = Product("Inception", "Sci-Fi", 499.00, 50)

        cat1.add_product(p1)
        cat2.add_product(p2)

        self.assertIn(p1, cat1.products)
        self.assertNotIn(p1, cat2.products)
        self.assertIn(p2, cat2.products)
        self.assertNotIn(p2, cat1.products)
