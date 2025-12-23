import unittest
from src.category_ import Product
from src.Smartphone import Smartphone



class TestSmartphone(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом."""
        self.smartphone1 = Smartphone(
            name="iPhone 15",
            description="Флагман Apple",
            price=100000,
            quantity=2,
            efficiency=95.0,
            model="15 Pro Max",
            memory=512,
            color="Чёрный"
        )
        self.smartphone2 = Smartphone(
            name="Galaxy S24",
            description="Флагман Samsung",
            price=90000,
            quantity=3,
            efficiency=94.5,
            model="S24 Ultra",
            memory=256,
            color="Серый"
        )

    def test_initialization(self):
        """Тест: объект Smartphone создаётся корректно."""
        self.assertEqual(self.smartphone1.name, "iPhone 15")
        self.assertEqual(self.smartphone1.price, 100000)
        self.assertEqual(self.smartphone1.quantity, 2)
        self.assertEqual(self.smartphone1.efficiency, 95.0)
        self.assertEqual(self.smartphone1.model, "15 Pro Max")
        self.assertEqual(self.smartphone1.memory, 512)
        self.assertEqual(self.smartphone1.color, "Чёрный")

    def test_inherits_from_product(self):
        """Тест: Smartphone является подклассом Product."""
        self.assertTrue(issubclass(Smartphone, Product))
        self.assertIsInstance(self.smartphone1, Product)

    def test_add_smartphones_valid(self):
        """Тест: сложение двух смартфонов возвращает корректную сумму."""
        total = self.smartphone1 + self.smartphone2
        expected = (100000 * 2) + (90000 * 3)  # 200_000 + 270_000 = 470_000
        self.assertEqual(total, expected)

    def test_add_with_non_smartphone_raises_typeerror(self):
        """Тест: при сложении с не-Smartphone выбрасывается TypeError."""
        with self.assertRaises(TypeError) as context:
            self.smartphone1 + "не смартфон"

        self.assertIn("Нельзя сложить Smartphone и str", str(context.exception))

    def test_add_with_none_raises_typeerror(self):
        """Тест: сложение с None вызывает TypeError."""
        with self.assertRaises(TypeError) as context:
            self.smartphone1 + None

        self.assertIn("Нельзя сложить Smartphone и NoneType", str(context.exception))

    def test_add_with_product_instance_raises_typeerror(self):
        """Тест: сложение с экземпляром Product (но не Smartphone) вызывает ошибку."""
        # Создаём простой Product (не смартфон)
        product = Product(
            name="Чехол",
            description="Силиконовый чехол",
            price=1000,
            quantity=10
        )

        with self.assertRaises(TypeError) as context:
            self.smartphone1 + product

        self.assertIn("Нельзя сложить Smartphone и Product", str(context.exception))






if __name__ == '__main__':
    unittest.main()
