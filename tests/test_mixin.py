import unittest

from src.mixin import PrintMixin  # Замените your_module на реальный путь


class TestClass(PrintMixin):
    def __init__(self, name=None, description=None, price=None, quantity=None):
        self.name = name
        self.description = description
        self._price = price  # Приватное поле
        self.quantity = quantity

    @property
    def price(self):
        return self._price  # Геттер для private поля _price


class TestPrintMixin(unittest.TestCase):
    def test_repr_empty_object(self):
        obj = TestClass()
        expected_output = "TestClass(name=None, description=None, price=None, quantity=None)"
        self.assertEqual(str(obj), expected_output)

    def test_repr_special_price_handling(self):
        obj = TestClass(price=200)
        expected_output = "TestClass(name=None, description=None, price=200, quantity=None)"
        self.assertEqual(str(obj), expected_output)

    def test_repr_with_all_attributes(self):
        obj = TestClass(name="TestName", description="TestDescription", price=100, quantity=5)
        expected_output = "TestClass(name=TestName, description=TestDescription, price=100, quantity=5)"
        self.assertEqual(str(obj), expected_output)

    def test_repr_without_some_attributes(self):
        obj = TestClass(description="Only Description")
        expected_output = "TestClass(name=None, description=Only Description, price=None, quantity=None)"
        self.assertEqual(str(obj), expected_output)


if __name__ == "__main__":
    unittest.main()
