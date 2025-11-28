
from loguru import logger
import sys
import os
import typing

# Удаляем стандартные обработчики
logger.remove()

# Настраиваем вывод в консоль (только INFO и выше)
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}"
)

# Настраиваем запись в файл с ротацией и сжатием
logger.add(
    "../logs/category.log",
    level="INFO",           # Только INFO и выше
    rotation="10 MB",       # Ротация при достижении 10 МБ
    retention="1 month",     # Удаление логов старше 1 месяца
    compression="gz",      # Сжатие старых логов
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"  # Формат файла
)

# Примеры сообщений
logger.debug("Это сообщение не появится (уровень DEBUG)")  # Не будет видно, т.к. уровень INFO
logger.info("Это сообщение появится в консоли и файле")
logger.warning("Это предупреждение также будет записано")



class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """
        Класс товара.

        Args:
            name: Название товара (строка)
            description: Описание товара (строка)
            price: Цена товара в рублях (число с плавающей точкой)
            quantity: Количество в наличии в штуках (целое число)
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт.\n"


    def __repr__(self):
        return self.__str__()


class Category:
    total_categories = 0
    total_products = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products
        Category.total_categories += 1

    def add_product(self, product: Product) -> None:
        self.__products.append(product)
        Category.total_products += 1  # Увеличиваем при добавлении
        logger.info("добавили продукт")

    def remove_product(self, product: Product) -> None:
        if product in self.__products:
            self.__products.remove(product)
            Category.total_products -= 1  # Уменьшаем при удалении!
        # Если товара нет — ничего не делаем (без ошибки)


    @property
    def products(self):
        return self.__products

if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    category1 = Category("Смартфоны",
                         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
                         [product1, product2, product3])

    print(category1.name == "Смартфоны")
    print(category1.description)

    print(category1.total_categories)
    print(category1.total_products)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category("Телевизоры",
                         "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
                         [product4])

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.total_categories)
    print(Category.total_products)



