


from abc import ABC, abstractmethod



class AbstractEntity(ABC):
    def __init__(self, name: str):
        self.name = name
        """Для классов «Заказ» и «Категория» выделиk общие свойства и вынес их в общий абстрактный класс."""


    @abstractmethod
    def info(self) -> str:
        pass

class Order(AbstractEntity):

    def __init__(self, name: str, product_link: str, quantity: int, final_cost: float):

        """ класс «Заказ», в котором есть ссылка на то, какой товар был куплен,

                количество купленного товара, а также итоговая стоимость.

                В заказе может быть указан только один товар."""

        super().__init__(name)
        self.product_link = product_link
        self.quantity = quantity
        self.final_cost = final_cost

    def info(self) -> str:
        """Выводит карточку заказа"""

        return (
            f"Заказ: {self.name}\n"
            f"Товар: {self.product_link}\n"
            f"Количество: {self.quantity}\n"
            f"Итоговая стоимость: {self.final_cost:.2f} руб."
        )

