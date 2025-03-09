import random
from animals import Dog
from hero import HeroDog

class SmallEnemy(Dog):
    def __init__(self, name: str):
        super().__init__(name, hp=20)
        self.crit_chance = 0.08  # Шанс критического удара (8%)

    def do(self, target: HeroDog) -> None:
        damage = 5
        target.hp -= damage
        print(f"{self.name} кусает {target.name}! Нанесено {damage} урона. У {target.name} осталось {target.hp} здоровья.")

        is_critical = random.random() < self.crit_chance
        damage = 5 * (1.5 if is_critical else 1)  # Урон увеличивается на 150% при критическом ударе

        if is_critical:
            print(f"{self.name} наносит критический урон: {damage}!")
        else:
            print(f"{self.name} атакует и наносит урон: {damage}.")

        target.hp -= damage
        print(f"У {target.name} осталось {target.hp} здоровья.")

    def exp_reward(self) -> int:
        return 5

class BigEnemy(Dog):
    def __init__(self, name: str):
        super().__init__(name, hp=40)
        self.crit_chance = 0.08  # Шанс критического удара (8%)

    def do(self, target: HeroDog) -> None:
        damage = 10
        target.hp -= damage
        print(f"{self.name} с силой бьёт {target.name}! Нанесено {damage} урона. У {target.name} осталось {target.hp} здоровья.")

        is_critical = random.random() < self.crit_chance
        damage = 10 * (1.5 if is_critical else 1)  # Урон увеличивается на 150% при критическом ударе

        if is_critical:
            print(f"{self.name} наносит критический урон: {damage}!")
        else:
            print(f"{self.name} атакует и наносит урон: {damage}.")

        target.hp -= damage
        print(f"У {target.name} осталось {target.hp} здоровья.")

    def exp_reward(self) -> int:
        return 10

class SkilledEnemy(Dog):
    def __init__(self, name: str):
        super().__init__(name, hp=60)
        self.crit_chance = 0.08  # Шанс критического удара (8%)

    def do(self, target: HeroDog) -> None:
        damage = 15
        target.hp -= damage
        print(f"{self.name} проводит сложную атаку на {target.name}! Нанесено {damage} урона. У {target.name} осталось {target.hp} здоровья.")

        is_critical = random.random() < self.crit_chance
        damage = 15 * (1.5 if is_critical else 1)  # Урон увеличивается на 150% при критическом ударе

        if is_critical:
            print(f"{self.name} наносит критический урон: {damage}!")
        else:
            print(f"{self.name} атакует и наносит урон: {damage}.")

        target.hp -= damage
        print(f"У {target.name} осталось {target.hp} здоровья.")

    def exp_reward(self) -> int:
        return 20

class Boss(Dog):
    def __init__(self, name: str, hp: int, attack_power: int = 50):
        super().__init__(name, hp)
        self.attack_power = attack_power
        self.crit_chance = 0.1  # Шанс критического удара (10%)
        self.miss_chance = 0.015  # Шанс промаха (1.5%)
        self.dodge_chance = 0.05  # Шанс уворота (5%)

    def do(self, target: HeroDog) -> None:
        # Проверка промаха
        if random.random() < self.miss_chance:
            print(f"{self.name} промахивается!")
            return

        # Проверка критического удара
        is_critical = random.random() < self.crit_chance
        damage = self.attack_power * (1.5 if is_critical else 1)

        if is_critical:
            print(f"{self.name} наносит критический урон: {damage}!")
        else:
            print(f"{self.name} атакует и наносит урон: {damage}!")

        target.hp -= damage

        # Проверка состояния героя
        if target.hp <= 0:
            target.hp = 0
            print(f"{target.name} пал в бою!")

    def dodge(self) -> bool:
        return random.random() < self.dodge_chance