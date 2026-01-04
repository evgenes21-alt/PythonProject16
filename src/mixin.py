
class PrintMixin:
    def __repr__(self):
        attrs = []
        for attr in ['name', 'description']:
            if hasattr(self, attr):
                attrs.append(f"{attr}={getattr(self, attr)}")

        # Явно добавляем price через свойство (не через getattr)
        if hasattr(self, 'price'):
            attrs.append(f"price={self.price}")

        if hasattr(self, 'quantity'):
            attrs.append(f"quantity={getattr(self, 'quantity')}")

        return f"{self.__class__.__name__}({', '.join(attrs)})"


