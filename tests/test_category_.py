
import unittest
from unittest.mock import patch, MagicMock, PropertyMock
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
        self.assertIsInstance(category.__products, list)
        self.assertEqual(len(category.__products), 0)
        self.assertEqual(Category.total_categories, 1)

    def test_add_product_increments_counter(self):

        category = Category("Книги", "Художественная литература", [])
        product = Product("Война и мир", "Роман", 899.00, 7)

        category.add_product(product)

        # Проверяем, что значение изменилось (не вызов __set__, а результат)
        self.assertEqual(Category.total_products, 1)


    def test_remove_product_decrements_counter(self):
        # Обнуляем счётчики (если не сделано в setUp)
        Category.total_categories = 0
        Category.total_products = 0

        category = Category("Спорт", "Инвентарь", [])
        product = Product("Мяч", "Футбольный", 1490.00, 5)

        category.add_product(product)  # total_products → 1
        category.remove_product(product)  # total_products → 0

        self.assertEqual(Category.total_products, 0)  # Теперь проверит реальное значение!

    def test_remove_product_not_in_list_no_error(self):
        """Проверяет удаление товара, которого нет в списке — без ошибок."""
        category = Category("Техника", "Бытовая техника", [])
        product = Product("Чайник", "Электрический", 2490.00, 8)


        # Не добавляем в категорию — пытаемся удалить
        category.remove_product(product)


        self.assertEqual(len(category.__products), 0)
        self.assertEqual(Category.total_products, 0)


    @patch('builtins.print')  # Мокируем print, если в коде есть отладочные print
    def test_add_product_calls_append(self, mock_print):
        """Проверяет, что add_product вызывает list.append."""
        category = Category("Игры", "Видеоигры", [])
        product = Product("The Witcher 3", "RPG", 1299.00, 100)


        # Мокируем список products, чтобы отследить вызов append
        mock_products = MagicMock()
        mock_products.append = MagicMock()
        category.__products = mock_products

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
            # Создаём продукты ПОСЛЕ патча — тогда мок их «увидит»
            p1 = Product("Товар1", "Описание1", 100.0, 5)
            p2 = Product("Товар2", "Описание2", 200.0, 3)

            category = Category("Товары", "Разные товары", [p1, p2])

            # Теперь проверяем, что __init__ НЕ вызывался повторно при создании категории
            self.assertFalse(mock_product_init.call_count > 0)



    def test_isolation_between_categories(self):
        """Проверяет изоляцию между разными категориями."""
        cat1 = Category("Игры", "Видеоигры", [])
        cat2 = Category("Фильмы", "DVD", [])

        p1 = Product("The Witcher 3", "RPG", 1299.00, 100)
        p2 = Product("Inception", "Sci-Fi", 499.00, 50)

        cat1.add_product(p1)
        cat2.add_product(p2)

        self.assertIn(p1, cat1.__products)
        self.assertNotIn(p1, cat2.__products)
        self.assertIn(p2, cat2.__products)
        self.assertNotIn(p2, cat1.__products)
