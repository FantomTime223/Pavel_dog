from characters import Animal, HeroDog

class Inventory:
    def __init__(self) -> None:
        self.items = {}  # Словарь {название_предмета: количество}
        self.debuffs = []  # Список активных дебаффов

    def add_item(self, item_name: str, quantity: int = 1) -> None:
        """Добавление предмета в инвентарь"""
        if item_name in self.items:
            self.items[item_name] += quantity  # Увеличиваем количество, если предмет уже есть
        else:
            self.items[item_name] = quantity  # Добавляем новый предмет
        print(f"Добавлено {quantity}x {item_name}. Всего: {self.items[item_name]}.")

    def remove_item(self, item_name: str, quantity: int = 1) -> None:
        """Удаление предмета из инвентаря"""
        if item_name in self.items:
            self.items[item_name] -= quantity
            if self.items[item_name] <= 0:
                del self.items[item_name]
            print(f"Удалено {quantity}x {item_name}.")
        else:
            print(f"Предмет {item_name} отсутствует в инвентаре.")

    def show_inventory(self) -> None:
        """Вывод содержимого инвентаря"""
        print("=====:Ваш инвентарь:=====")
        if not self.items:
            print("Пусто")
        for item_name, quantity in self.items.items():
            print(f"{item_name}: {quantity}")
        print("=========================")

    def view_item_properties(self, item_name: str) -> None:
        """Просмотр свойств предмета"""
        if item_name not in self.items:
            print(f"Предмет {item_name} отсутствует в инвентаре.")
            return
        print(f"Название: {item_name}")
        print(f"Количество: {self.items[item_name]}")
        # Для демонстрации дебаффов
        if "debuff" in item_name.lower():
            print("Дебафф: снижает скорость восстановления здоровья.")

    def use_item(self, item_name: str, user: HeroDog) -> None:
        """Использование предмета"""
        if "NoHealing" in [d["type"] for d in self.debuffs]:
            print("Вы не можете использовать зелья лечения из-за дебаффа!")
            return
        if item_name not in self.items or self.items[item_name] <= 0:
            print(f"Предмет {item_name} отсутствует в инвентаре.")
            return
        print(f"{user.name} использовал {item_name}!")
        self.remove_item(item_name)

    def discard_item(self, item_name: str) -> None:
        """Выбрасывание предмета"""
        if item_name in self.items:
            print(f"Вы выбросили {item_name}.")
            del self.items[item_name]
        else:
            print(f"Предмет {item_name} отсутствует в инвентаре.")

    def throw_item(self, item_name: str, target: Animal) -> None:
        """Бросок предмета в противника"""
        if "damage" not in item_name.lower():
            print("Этот предмет нельзя бросить!")
            return
        damage = 10  # Условный урон от броска
        print(f"Вы бросили {item_name} в {target.name}, нанеся {damage} урона!")
        self.remove_item(item_name)