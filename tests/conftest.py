import pytest

from src.category_ import Product, Category


@pytest.fixture(scope="function")
def product_samsung():
    yield Product("Samsung", "Супертелефон", 120000.0, 5)


@pytest.fixture(scope="function")
def product_poco():
    yield Product("POCO", "Телефон с хорошей камерой", 90000.0, 12)


@pytest.fixture(scope="function")
def product_huawey():
    yield Product("Huawey", "Флагман с удобной доставкой", 144000.0, 3)


@pytest.fixture(scope="function")
def category_notebooks():
    yield Category("Ноутбуки", "Ультрабуки, планшеты", ["ASUS", "SONY"])


@pytest.fixture(scope="function")
def category_phones():
    yield Category("Телефоны", "Современные телефоны", ["Samsung", "POCO", "HUAWEI"])


@pytest.fixture(scope="function")
def category_washing_mashines():
    yield Category("Стиральные машины", "Современные стиралки", ["Indesit", "Midea", "LG"])
