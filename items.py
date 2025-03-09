from characters import HeroDog

class Item:
    def __init__(self, name: str, description: str, debuffs: list = None, throw_damage: int = 0):
        self.name = name
        self.description = description
        self.debuffs = debuffs if debuffs else []
        self.throw_damage = throw_damage

    def use(self, user: HeroDog) -> None:
        raise NotImplementedError("Метод использования должен быть переопределён.")