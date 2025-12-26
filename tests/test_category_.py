import logging
import unittest
from unittest.mock import patch

from src.category_ import Category, Product  # замените your_module на имя вашего файла

# Настройка логгера для перехвата сообщений
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestProductWithRealData(unittest.TestCase):

    def setUp(self):
        """Создаём тестовые данные на основе реальных JSON."""
        self.samsung = Product(
            name="Samsung Galaxy C23 Ultra", description="256GB, Серый цвет, 200MP камера", price=180000.0, quantity=5
        )
        self.iphone = Product(name="Iphone 15", description="512GB, Gray space", price=210000.0, quantity=8)
        self.xiaomi = Product(name="Xiaomi Redmi Note 11", description="1024GB, Синий", price=31000.0, quantity=14)
        self.tv = Product(name='55" QLED 4K', description="Фоновая подсветка", price=123000.0, quantity=7)

    def test_product_init(self):
        """Проверка инициализации продуктов на реальных данных."""
        self.assertEqual(self.samsung.name, "Samsung Galaxy C23 Ultra")
        self.assertEqual(self.samsung.price, 180000.0)
        self.assertEqual(self.samsung.quantity, 5)

        self.assertEqual(self.iphone.name, "Iphone 15")
        self.assertEqual(self.iphone.price, 210000.0)
        self.assertEqual(self.iphone.quantity, 8)

        self.assertEqual(self.xiaomi.name, "Xiaomi Redmi Note 11")
        self.assertEqual(self.xiaomi.price, 31000.0)
        self.assertEqual(self.xiaomi.quantity, 14)

        self.assertEqual(self.tv.name, '55" QLED 4K')
        self.assertEqual(self.tv.price, 123000.0)
        self.assertEqual(self.tv.quantity, 7)

    def test_product_str(self):
        """Проверка строкового представления продуктов."""
        expected_samsung = "Samsung Galaxy C23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        self.assertEqual(str(self.samsung), expected_samsung)

        expected_tv = '55" QLED 4K, 123000.0 руб. Остаток: 7 шт.\n'
        self.assertEqual(str(self.tv), expected_tv)

    @patch("logging.Logger.info")
    def test_new_product_create_from_dict(self, mock_log):
        """Создание продукта из словаря (новый товар)."""
        product_data = {"name": "Google Pixel 8", "description": "128GB, Чёрный", "price": 79000.0, "quantity": 3}
        product = Product.new_product(product_data, products_list=[])

        self.assertEqual(product.name, "Google Pixel 8")
        self.assertEqual(product.price, 79000.0)
        self.assertEqual(product.quantity, 3)

    @patch("logging.Logger.info")
    def test_new_product_merge_duplicate(self, mock_log):
        """Объединение дубликата: сумма количества, максимальная цена."""
        products_list = [self.samsung]  # Уже есть Samsung

        # Новый Samsung с другой ценой и количеством
        new_data = {
            "name": "Samsung Galaxy C23 Ultra",
            "description": "Обновлённое описание",
            "price": 190000.0,  # выше текущей цены
            "quantity": 10,
        }

        result = Product.new_product(new_data, products_list)

        # Проверяем, что вернулся существующий объект
        self.assertIs(result, self.samsung)
        # Количество: 5 + 10 = 15
        self.assertEqual(result.quantity, 15)
        # Цена: max(180000, 190000) = 190000
        self.assertEqual(result.price, 190000.0)
        # Описание обновлено
        self.assertEqual(result.description, "Обновлённое описание")

    def test_new_product_missing_key(self):
        """Ошибка при отсутствии обязательного ключа в словаре."""
        invalid_data = {"name": "Тест", "description": "Нет цены и количества"}
        with self.assertRaises(KeyError) as cm:
            Product.new_product(invalid_data, [])
        self.assertIn("price", str(cm.exception))


class TestCategoryWithRealData(unittest.TestCase):

    def setUp(self):
        """Сброс счётчиков и создание тестовых категорий."""
        Category.category_count = 0
        Category.product_count = 0

        # Создаём продукты
        self.products_smartphones = [
            Product("Samsung Galaxy C23 Ultra", "256GB, Серый", 180000.0, 5),
            Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
            Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14),
        ]
        self.products_tvs = [Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)]

        # Создаём категории
        self.smartphones = Category("Смартфоны", "Смартфоны для жизни", self.products_smartphones)
        self.tvs = Category("Телевизоры", "Современные телевизоры", self.products_tvs)

    def test_products_property(self):
        """Проверка свойства products (строковое представление всех товаров)."""
        result = self.smartphones.products

        # Проверяем, что все товары присутствуют в строке
        self.assertIn("Samsung Galaxy C23 Ultra, 180000.0 руб. Остаток: 5 шт.", result)
        self.assertIn("Iphone 15, 210000.0 руб. Остаток: 8 шт.", result)
        self.assertIn("Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.", result)

        # Проверяем количество строк (должно быть 3 товара → 3 строки)
        lines = result.strip().split("\n")
        self.assertEqual(len(lines), 3)

    def test_category_count_singleton(self):
        """Проверка, что category_count увеличивается только при создании новой категории."""
        # Создаём ещё одну категорию
        another_category = Category("Ноутбуки", "Мобильные компьютеры", [])
        self.assertEqual(Category.category_count, 3)  # 2 было + 1 новая


class TestProductAdd(unittest.TestCase):

    def test_add_returns_correct_sum(self):
        """Проверяет, что __add__ возвращает правильную сумму произведений."""
        p1 = Product("Товар 1", "Описание 1", price=10.0, quantity=2)
        p2 = Product("Товар 2", "Описание 2", price=5.0, quantity=3)

        result = p1 + p2

        # Ожидаемое: (10 * 5) + (2 * 3) = 50 + 6 = 56
        expected = 35.0
        self.assertEqual(result, expected)

    def test_add_with_zero_values(self):
        """Проверяет поведение при нулевых цене/количестве."""
        p1 = Product("Товар 1", "Описание 1", price=0.0, quantity=5)
        p2 = Product("Товар 2", "Описание 2", price=10.0, quantity=0)

        result = p1 + p2

        # Ожидаемое: (0 * 10) + (5 * 0) = 0 + 0 = 0
        expected = 0.0
        self.assertEqual(result, expected)


class TestCategoryStr(unittest.TestCase):

    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.samsung = None

    def setUp(self):
        """Создаём тестовые данные перед каждым тестом."""
        self.p1 = Product("iPhone", "Смартфон", 99990.0, 5)
        self.p2 = Product("Samsung", "Смартфон", 89990.0, 3)
        self.category = Category("Смартфоны", "Мобильные устройства", [self.p1, self.p2])

    def test_str_returns_correct_format(self):
        """Проверяет формат строки."""
        result = str(self.category)
        expected = "Смартфоны, количество продуктов 8 шт\n"  # 5 + 3 = 8
        self.assertEqual(result, expected)

    def test_str_with_empty_products_list(self):
        """Проверяет строку для категории без товаров."""
        empty_category = Category("Пустая категория", "Нет товаров", [])
        result = str(empty_category)
        expected = "Пустая категория, количество продуктов 0 шт\n"
        self.assertEqual(result, expected)

    def test_str_with_single_product(self):
        """Проверяет строку для категории с одним товаром."""
        single_product = Product("Ноутбук", "Игровой", 120000.0, 1)
        category = Category("Ноутбуки", "Компьютеры", [single_product])
        result = str(category)
        expected = "Ноутбуки, количество продуктов 1 шт\n"
        self.assertEqual(result, expected)

    def test_str_calls_implicitly(self):
        """Проверяет, что str() и print() используют __str__."""
        result_str = str(self.category)
        result_print = self.category.__str__()  # прямой вызов
        self.assertEqual(result_str, result_print)

    def test_product_price_setter(self):
        """Проверка: изменение цены работает корректно."""
        product = Product("Товар", "Описание", 100, 5)
        product.price = 100
        self.assertEqual(product.price, 100)

    def test_product_quantity_setter(self):
        """Проверка: изменение количества работает корректно."""
        product = Product("Товар", "Описание", 100, 5)
        product.quantity = 10
        self.assertEqual(product.quantity, 10)

    def test_product_inequality(self):
        """Проверка: продукты с разными атрибутами не равны."""
        p1 = Product("iPhone", "Смартфон", 100000, 2)
        p2 = Product("Galaxy", "Смартфон", 90000, 3)
        self.assertNotEqual(p1, p2)


if __name__ == "__main__":
    unittest.main()
