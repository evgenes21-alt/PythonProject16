from src.category_ import Product


class Smartphone(Product):
    def __init__(
        self,
        name,
        description,
        price,
        quantity,
        efficiency,
        model,
        memory,
        color,
    ) -> None:
        super().__init__(name, description, price, quantity)

        self.price = price
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other):
        """
        Складывает стоимость двух смартфонов (цена × количество).

        Args:
            other (Smartphone): Второй смартфон для сложения.

        Returns:
            float: Общая стоимость обоих смартфонов.

        Raises:
            TypeError: Если other не является экземпляром Smartphone.
        """
        if type(other) is not Smartphone:

            raise TypeError(f"Нельзя сложить Smartphone и {type(other).__name__}")
        return (self.price * self.quantity) + (other.price * other.quantity)


if __name__ == "__main__":
    smartphone1 = Smartphone(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый"
    )
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    smartphone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")

    print(smartphone1.name)
    print(smartphone1.description)
    print(smartphone1.price)
    print(smartphone1.quantity)
    print(smartphone1.efficiency)
    print(smartphone1.model)
    print(smartphone1.memory)
    print(smartphone1.color)

    print(smartphone2.name)
    print(smartphone2.description)
    print(smartphone2.price)
    print(smartphone2.quantity)
    print(smartphone2.efficiency)
    print(smartphone2.model)
    print(smartphone2.memory)
    print(smartphone2.color)

    print(smartphone3.name)
    print(smartphone3.description)
    print(smartphone3.price)
    print(smartphone3.quantity)
    print(smartphone3.efficiency)
    print(smartphone3.model)
    print(smartphone3.memory)
    print(smartphone3.color)
    smartphone_sum = smartphone1 + smartphone2
    print(smartphone_sum)
