# main.py

# Импортируем классы
from src.category_ import Product
from src.smartphone import Smartphone
from src.lawngrass import LawnGrass
from src.category_ import Category

# Если используете логирование, добавьте:
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Создаём объекты смартфонов
smartphone1 = Smartphone(
    name="Samsung Galaxy S23 Ultra",
    description="256GB, Серый цвет, 200MP камера",
    price=180000.0,
    quantity=5,
    efficiency=95.5,
    model="S23 Ultra",
    memory=256,
    color="Серый"
)

smartphone2 = Smartphone(
    name="Iphone 15",
    description="512GB, Gray space",
    price=210000.0,
    quantity=8,
    efficiency=98.2,
    model="15",
    memory=512,
    color="Gray space"
)

smartphone3 = Smartphone(
    name="Xiaomi Redmi Note 11",
    description="1024GB, Синий",
    price=31000.0,
    quantity=14,
    efficiency=90.3,
    model="Note 11",
    memory=1024,
    color="Синий"
)

# 2. Создаём объекты газонной травы
grass1 = LawnGrass(
    name="Газонная трава",
    description="Элитная трава для газона",
    price=500.0,
    quantity=20,
    country="Россия",
    germination_period="7 дней",
    color="Зеленый"
)


grass2 = LawnGrass(
    name="Газонная трава 2",
    description="Выносливая трава",
    price=450.0,
    quantity=15,
    country="США",
    germination_period="5 дней",
    color="Темно-зеленый"
)


# 3. Проверяем сложение однотипных объектов
print("=== Сложение товаров ===")

smartphone_sum = smartphone1 + smartphone2
print(f"Сумма смартфонов: {smartphone_sum} руб.")  # 180000×5 + 2100000×8


grass_sum = grass1 + grass2
print(f"Сумма травы: {grass_sum} руб.")  # 500×20 + 450×15


# 4. Проверяем ошибку при сложении разных типов
print("\n=== Проверка ошибки сложения ===")
try:
    invalid_sum = smartphone1 + grass1
except TypeError as e:
    print(f"Ошибка: {e}")
else:
    print("Не возникла ошибка TypeError при попытке сложения")


# 5. Создаём категории
print("\n=== Создание категорий ===")
category_smartphones = Category(
    name="Смартфоны",
    description="Высокотехнологичные смартфоны",
    products=[smartphone1, smartphone2]
)


category_grass = Category(
    name="Газонная трава",
    description="Различные виды газонной травы",
    products=[grass1, grass2]
)


print(f"Категория '{category_smartphones.name}' создана.")
print(f"Категория '{category_grass.name}' создана.")


# 6. Добавляем новый товар в категорию
print("\n=== Добавление товара в категорию ===")
try:
    category_smartphones.add_product(smartphone3)
    print("Товар успешно добавлен в категорию 'Смартфоны'.")
except TypeError as e:
    print(f"Ошибка при добавлении: {e}")


# 7. Выводим список товаров в категории
print("\n=== Товары в категориях ===")
print("Категория 'Смартфоны':")
print(category_smartphones.products)


print("\nКатегория 'Газонная трава':")
print(category_grass.products)


# 8. Выводим общее количество товаров во всех категориях
print("\n=== Статистика ===")
print(f"Общее количество категорий: {Category.category_count}")
print(f"Общее количество товаров во всех категориях: {Category.product_count}")


# 9. Проверяем ошибку при добавлении не-продукта
print("\n=== Проверка ошибки добавления не-продукта ===")
try:
    category_smartphones.add_product("Not a product")
except TypeError as e:
    print(f"!Ошибка: {e}")
else:
    print("Не возникла ошибка TypeError при добавлении не продукта")
