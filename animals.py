class Animal:
    def __init__(self, name: str, hp: int, color: str = "неизвестный"):
        self.name = name
        self.hp = hp
        self.color = color

class Dog(Animal):
    def do(self, target: 'Animal') -> None:
        print(f"{self.name} атакует {target.name} -> Гав!")