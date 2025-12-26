import unittest
from unittest.mock import patch
from src.category_ import Product
from src.smartphone import Smartphone


class TestSmartphone(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом."""
        self.smartphone = Smartphone(
            name="iPhone 15",
            description="Флагман Apple",
            price=100000,
            quantity=2,
            efficiency=95.0,
            model="15 Pro Max",
            memory=512,
            color="Чёрный",
        )

    # 1. Проверка инициализации

    def test_init_valid_data(self):
        """Тест: корректная инициализация объекта."""
        self.assertEqual(self.smartphone.name, "iPhone 15")
        self.assertEqual(self.smartphone.price, 100000)
        self.assertEqual(self.smartphone.quantity, 2)
        self.assertEqual(self.smartphone.efficiency, 95.0)
        self.assertEqual(self.smartphone.model, "15 Pro Max")
        self.assertEqual(self.smartphone.memory, 512)
        self.assertEqual(self.smartphone.color, "Чёрный")

    def test_init_zero_price(self):
        """Тест: цена = 0."""
        phone = Smartphone("Тест", "Описание", 0, 5, 90.0, "Модель", 128, "Цвет")
        self.assertEqual(phone.price, 0)

    def test_init_zero_quantity(self):
        """Тест: количество = 0."""
        phone = Smartphone("Тест", "Описание", 1000, 0, 90.0, "Модель", 128, "Цвет")
        self.assertEqual(phone.quantity, 0)

    def test_init_min_efficiency(self):
        """Тест: efficiency = 0.0."""
        phone = Smartphone("Тест", "Описание", 1000, 1, 0.0, "Модель", 64, "Цвет")
        self.assertEqual(phone.efficiency, 0.0)

    def test_init_max_values(self):
        """Тест: граничные значения (большие числа)."""
        phone = Smartphone(
            name="Макс",
            description="Максимум",
            price=1_000_000,
            quantity=10_000,
            efficiency=100.0,
            model="MaxModel",
            memory=8192,
            color="Золотой",
        )
        self.assertEqual(phone.price, 1_000_000)
        self.assertEqual(phone.quantity, 10_000)
        self.assertEqual(phone.efficiency, 100.0)
        self.assertEqual(phone.memory, 8192)

    # 2. Наследование от Product

    def test_inherits_from_product(self):
        """Тест: Smartphone — подкласс Product."""
        self.assertTrue(issubclass(Smartphone, Product))
        self.assertIsInstance(self.smartphone, Product)

    # 3. Метод __add__

    def test_add_valid(self):
        """Тест: сложение двух смартфонов → корректная сумма."""
        other = Smartphone("Galaxy", "Описание", 90000, 3, 94.5, "S24", 256, "Серый")
        total = self.smartphone + other
        expected = (100000 * 2) + (90000 * 3)  # 200_000 + 270_000 = 470_000
        self.assertEqual(total, expected)

    def test_add_with_none_raises_typeerror(self):
        """Тест: сложение с None → TypeError."""
        with self.assertRaises(TypeError) as context:
            self.smartphone + None
        self.assertIn("Нельзя сложить Smartphone и NoneType", str(context.exception))

    def test_add_with_string_raises_typeerror(self):
        """Тест: сложение со строкой → TypeError."""
        with self.assertRaises(TypeError) as context:
            self.smartphone + "не смартфон"
        self.assertIn("Нельзя сложить Smartphone и str", str(context.exception))

    def test_add_with_product_raises_typeerror(self):
        """Тест: сложение с Product (не Smartphone) → TypeError."""
        product = Product("Чехол", "Описание", 1000, 10)
        with self.assertRaises(TypeError) as context:
            self.smartphone + product
        self.assertIn("Нельзя сложить Smartphone и Product", str(context.exception))

    def test_add_with_different_class_raises_typeerror(self):
        """Тест: сложение с объектом другого класса → TypeError."""

        class Dummy:
            pass

        with self.assertRaises(TypeError) as context:
            self.smartphone + Dummy()
        self.assertIn("Нельзя сложить Smartphone и Dummy", str(context.exception))

    def test_add_does_not_modify_operands(self):
        """Тест: сложение не меняет исходные объекты."""
        orig_price = self.smartphone.price
        orig_qty = self.smartphone.quantity

        other = Smartphone("Galaxy", "Описание", 90000, 3, 94.5, "S24", 256, "Серый")
        _ = self.smartphone + other

        self.assertEqual(self.smartphone.price, orig_price)
        self.assertEqual(self.smartphone.quantity, orig_qty)

    def test_price_is_float_or_int(self):
        """Тест: price — число (int/float)."""
        self.assertIsInstance(self.smartphone.price, (int, float))

    def test_quantity_is_int(self):
        """Тест: quantity — целое число."""
        self.assertIsInstance(self.smartphone.quantity, int)

    def test_efficiency_is_float(self):
        """Тест: efficiency — float."""
        self.assertIsInstance(self.smartphone.efficiency, float)

    def test_memory_is_int(self):
        """Тест: memory — целое число."""
        self.assertIsInstance(self.smartphone.memory, int)

    def test_name_and_description_are_strings(self):
        """Тест: name и description — строки."""
        self.assertIsInstance(self.smartphone.name, str)
        self.assertIsInstance(self.smartphone.description, str)

    def test_model_and_color_are_strings(self):
        """Тест: model и color — строки."""
        self.assertIsInstance(self.smartphone.model, str)
        self.assertIsInstance(self.smartphone.color, str)

    def test_eq_same_instance(self):
        """Тест: объект равен самому себе."""
        self.assertTrue(self.smartphone == self.smartphone)

    def test_eq_different_attrs(self):
        """Тест: объекты с разными атрибутами не равны."""
        phone1 = Smartphone("iPhone", "Описание", 100000, 2, 95.0, "15 Pro Max", 512, "Чёрный")
        phone2 = Smartphone("Galaxy", "Описание", 90000, 3, 94.5, "S24", 256, "Серый")
        self.assertFalse(phone1 == phone2)

    # 10. Проверка __hash__ (если реализован)
    # Если __hash__ не определён, пропустите
    def test_hash_is_consistent(self):
        """Тест: hash объекта не меняется."""
        h1 = hash(self.smartphone)
        h2 = hash(self.smartphone)
        self.assertEqual(h1, h2)

    # 11. Проверка документации (docstring)
    def test_add_method_has_docstring(self):
        """Тест: метод __add__ имеет docstring."""
        doc = self.smartphone.__add__.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("Складывает стоимость двух смартфонов", doc)
