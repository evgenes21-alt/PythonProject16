import json
from typing import List, Dict, Any

from src.category_ import Category, Product


def load_data_from_json(filepath: str) -> Dict[str, List[Category]]:
    """
    Загружает данные из JSON-файла и создаёт объекты Product и Category.

    Args:
        filepath: путь к JSON-файлу

    Returns:
        Словарь с ключом 'categories' — списком объектов Category
    """
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories: List[Category] = []

    for cat_data in data["categories"]:
        # Создаём категорию
        category = Category(name=cat_data["name"], description=cat_data["description"])

        # Добавляем товары в категорию
        for prod_data in cat_data.get("products", []):
            product = Product(
                name=prod_data["name"],
                description=prod_data["description"],
                price=float(prod_data["price"]),
                quantity=int(prod_data["quantity"]),
            )
            category.add_product(product)

        categories.append(category)

    return {"categories": categories}
