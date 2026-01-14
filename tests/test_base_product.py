import unittest
from abc import ABCMeta
from typing import Any

from src.base_product import BaseProduct  # Импортируем ваш модуль


class ConcreteProduct(BaseProduct):
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __add__(self, other: "ConcreteProduct") -> float:
        return self.price + other.price


class TestBaseProduct(unittest.TestCase):
    def setUp(self):
        self.product1 = ConcreteProduct("Laptop", 1000.0)
        self.product2 = ConcreteProduct("Headphones", 50.0)

    def test_instantiation_of_base_class_fails(self):
        # Проверяем невозможность создания экземпляра абстрактного класса
        with self.assertRaises(TypeError):
            instance = BaseProduct()

    def test_concrete_class_methods_are_implemented(self):
        # Проверяем, что производный класс реализовал абстрактные методы
        result = self.product1 + self.product2
        self.assertEqual(result, 1050.0)

    def test_addition_operation(self):
        # Проверяем операцию сложения экземпляров
        result = self.product1 + self.product2
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 1050.0)

    def test_init_is_called_correctly(self):
        # Проверяем, что конструктор работает корректно
        self.assertEqual(self.product1.name, "Laptop")
        self.assertEqual(self.product1.price, 1000.0)


if __name__ == "__main__":
    unittest.main()
