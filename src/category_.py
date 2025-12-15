import sys

from loguru import logger

# Удаляем стандартные обработчики
logger.remove()

# Настраиваем вывод в консоль (только INFO и выше)
logger.add(
    sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}"
)

# Настраиваем запись в файл с ротацией и сжатием
logger.add(
    "../logs/category.log",
    level="INFO",  # Только INFO и выше
    rotation="10 MB",  # Ротация при достижении 10 МБ
    retention="1 month",  # Удаление логов старше 1 месяца
    compression="gz",  # Сжатие старых логов
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",  # Формат файла
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
        self.__price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт.\n"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def new_product(cls, product_dict: dict, products_list: list):
        """
        Создаёт экземпляр класса Product на основе словаря с данными.
        Если товар с таким именем уже есть в списке, объединяет количество и выбирает максимальную цену.

        Args:
            cls: Ссылка на класс (передаётся автоматически декоратором @classmethod)
            product_dict: Словарь с ключами 'name', 'description', 'price', 'quantity'
            products_list: Список существующих товаров для поиска дубликатов (опционально)

        Returns:
            Product: Новый или обновлённый экземпляр класса Product

        Raises:
            KeyError: Если в словаре отсутствуют обязательные ключи
            TypeError: Если типы данных не соответствуют ожидаемым
        """
        # Проверяем наличие всех обязательных ключей
        required_keys = ["name", "description", "price", "quantity"]
        for key in required_keys:
            if key not in product_dict:
                raise KeyError(f"Словарь должен содержать ключ '{key}'")

        # Проверяем типы данных
        if not isinstance(product_dict["name"], str):
            raise TypeError("name должен быть строкой")
        if not isinstance(product_dict["description"], str):
            raise TypeError("description должен быть строкой")
        if not isinstance(product_dict["price"], (int, float)):
            raise TypeError("price должен быть числом")
        if not isinstance(product_dict["quantity"], int):
            raise TypeError("quantity должен быть целым числом")

        name = product_dict["name"]

        # Если список товаров не передан или пуст — просто создаём новый товар
        if not products_list:
            return cls(
                name=name,
                description=product_dict["description"],
                price=product_dict["price"],
                quantity=product_dict["quantity"],
            )

        # Ищем товар с таким же именем в списке
        existing_product = None
        for product in products_list:
            if product.name == name:
                existing_product = product
                break

        if existing_product:
            # Объединяем количество
            new_quantity = existing_product.quantity + product_dict["quantity"]
            # Выбираем максимальную цену
            new_price = max(existing_product.__price, product_dict["price"])
            # Обновляем существующий товар
            existing_product.quantity = new_quantity
            existing_product.__price = new_price
            # Обновляем описание (можно оставить старое или взять новое — здесь берём новое)
            existing_product.description = product_dict["description"]
            return existing_product
        else:
            # Товара с таким именем нет — создаём новый
            return cls(
                name=name,
                description=product_dict["description"],
                price=product_dict["price"],
                quantity=product_dict["quantity"],
            )

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price >= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.price = new_price

    def __add__(self, other):
        total_price = self.__price * self.quantity
        total_quantity = other.__price * other.quantity
        total_sum = total_price + total_quantity
        return total_sum


class Category:
    category_count = 0  # "Общее количество категорий"
    product_count = 0  # Всего товаров во всех отделах

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        self.name = name  # Название отдела
        self.description = description  # Описание
        self.__products = products  # Сохраняем список товаров # Список товаров

        # Увеличиваем счётчик категорий
        Category.category_count += 1  # +1 к общему числу отделов

        # Автоматически считаем количество товаров в этой категории
        self._product_count = len(self.__products)  # Сколько товаров в этом отделе

        # Добавляем к глобальному счётчику
        Category.product_count += self._product_count  # + к общему числу товаров

    def get_product_count(self) -> int:
        """Возвращает количество товаров в данной категории."""
        return self._product_count  # Сколько у вас товаров сейчас?

    @classmethod
    def get_total_product_count(cls) -> int:
        """Возвращает общее количество товаров во всех категориях."""
        return cls.product_count  # Всего товаров во всех отделах

    @classmethod
    def get_category_count(cls) -> int:
        """Возвращает общее количество категорий."""
        return cls.category_count  # Всего отделов в магазине

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию."""
        self.__products.append(product)  # Добавляем товар в список
        self._product_count += 1  # +1 к счёту в отделе
        Category.product_count += 1  # +1 к общему счёту
        logger.info("Добавляем новый продукт")

    def remove_product(self, product: Product) -> bool:
        """Удаляет товар из категории. Возвращает True при успехе."""
        if product in self.__products:
            self.__products.remove(product)
            self._product_count -= 1
            Category.product_count -= 1
            logger.info("Удаляем продукт")
            return True
        return False

    #        """ геттер """

    @property
    def products(self) -> str:
        """Строковое представление списка товаров."""
        if not self.__products:
            return "Нет товаров"  # Формируем строку с перечнем

        products_str = ""
        for prod in self.__products:
            products_str += f"{prod.name}, {prod.price} руб. Остаток: {prod.quantity} шт.\n"
        return products_str.rstrip()

    def __str__(self):
        total_quantity = 0
        for product in self.__products:
            total_quantity += product.quantity
        return f"{self.name}, количество продуктов {total_quantity} шт\n"


if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)

    # product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    # product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    # product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    #
    # print(product1.name)
    # print(product1.description)
    # print(product1.price)
    # print(product1.quantity)
    #
    # print(product2.name)
    # print(product2.description)
    # print(product2.price)
    # print(product2.quantity)
    #
    # print(product3.name)
    # print(product3.description)
    # print(product3.price)
    # print(product3.quantity)
    #
    # category1 = Category(
    #     "Смартфоны",
    #     "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
    #     [product1, product2, product3],
    # )
    #
    # print(category1.name == "Смартфоны")
    # print(category1.description)
    # print(len(category1.products))
    # print(category1.category_count)
    # print(category1.product_count)
    #
    # product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    # category2 = Category(
    #     "Телевизоры",
    #     "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
    #     [product4],
    # )
    #
    # print(category2.name)
    # print(category2.description)
    # print(len(category2.products))
    # print(category2.products)
    #
    # print(Category.category_count)
    # print(Category.product_count)
