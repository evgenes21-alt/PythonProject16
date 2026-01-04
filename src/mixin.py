class PrintMixin:
    def __repr__(self):
        attrs = []
        for attr in ["name", "description", "price", "quantity"]:
            value = getattr(self, attr, None)  # Получаем значение атрибута или None
            attrs.append(f"{attr}={value}")  # Включаем атрибут независимо от его значения

        return f"{self.__class__.__name__}({', '.join(attrs)})"
