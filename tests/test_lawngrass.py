import unittest
from src.category_ import Product
from src.lawngrass import LawnGrass


class TestLawnGrass(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом."""
        self.grass1 = LawnGrass(
            name="Мятлик луговой",
            description="Высококачественная газонная трава",
            price=500,
            quantity=20,
            country="Россия",
            germination_period="7–10 дней",
            color="Зелёный",
        )
        self.grass2 = LawnGrass(
            name="Овсяница красная",
            description="Теневыносливая газонная трава",
            price=450,
            quantity=15,
            country="Германия",
            germination_period="5–8 дней",
            color="Тёмно‑зелёный",
        )

    def test_initialization(self):
        """Тест: объект LawnGrass создаётся корректно."""
        self.assertEqual(self.grass1.name, "Мятлик луговой")
        self.assertEqual(self.grass1.price, 500)
        self.assertEqual(self.grass1.quantity, 20)
        self.assertEqual(self.grass1.country, "Россия")
        self.assertEqual(self.grass1.germination_period, "7–10 дней")
        self.assertEqual(self.grass1.color, "Зелёный")

    def test_inherits_from_product(self):
        """Тест: LawnGrass является подклассом Product."""
        self.assertTrue(issubclass(LawnGrass, Product))
        self.assertIsInstance(self.grass1, Product)

    def test_add_lawngrasses_valid(self):
        """Тест: сложение двух LawnGrass возвращает корректную сумму."""
        total = self.grass1 + self.grass2
        expected = (500 * 20) + (450 * 15)  # 10 000 + 6 750 = 16 750
        self.assertEqual(total, expected)

    def test_add_with_non_lawngrass_raises_typeerror(self):
        """Тест: при сложении с не-LawnGrass выбрасывается TypeError."""
        with self.assertRaises(TypeError) as context:
            self.grass1 + "не трава"

        self.assertIn("Нельзя сложить LawnGrass и str", str(context.exception))

    def test_add_with_none_raises_typeerror(self):
        """Тест: сложение с None вызывает TypeError."""
        with self.assertRaises(TypeError) as context:
            self.grass1 + None

        self.assertIn("Нельзя сложить LawnGrass и NoneType", str(context.exception))

    def test_add_with_product_instance_raises_typeerror(self):
        """Тест: сложение с экземпляром Product (но не LawnGrass) вызывает ошибку."""
        # Создаём простой Product (не траву)
        product = Product(name="Семена цветов", description="Набор семян", price=200, quantity=5)

        with self.assertRaises(TypeError) as context:
            self.grass1 + product

        self.assertIn("Нельзя сложить LawnGrass и Product", str(context.exception))

    # def test_repr_and_str(self):
    #     """Тест: строковое представление объекта."""
    #     expected_str = "Мятлик луговой, 500 руб. Остаток: 20 шт.\n"
    #     self.assertEqual(str(self.grass1), expected_str)
    #     self.assertEqual(repr(self.grass1), expected_str)
    def test_str(self):
        """Тест: str() должен возвращать удобное строковое представление."""
        expected = "Мятлик луговой, 500 руб. Остаток: 20 шт.\n"
        self.assertEqual(str(self.grass1), expected)

    def test_repr(self):
        """Тест: repr() должен возвращать детальное представление объекта."""
        expected = (
            "LawnGrass(name=Мятлик луговой, "
            "description=Высококачественная газонная трава, "
            "price=500, "
            "quantity=20)"
        )
        self.assertEqual(repr(self.grass1), expected)


if __name__ == "__main__":
    unittest.main()
