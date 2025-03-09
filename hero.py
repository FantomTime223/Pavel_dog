import random
from characters import Animal, Dog

class HeroDog(Dog):
    def __init__(self, name: str, hp: int, color: str = "чёрный"):
        super().__init__(name, hp, color)
        self.level = 1
        self.exp = 0
        self.exp_to_level = 10  # Добавляем атрибут exp_to_level
        self.attack_power = 10
        self.miss_chance = 0.2  # Шанс промаха (20%)
        self.crit_chance = 0.1  # Шанс критического удара (10%)
        self.max_hp = hp
        self.inventory = None  # Инвентарь будет инициализирован позже

    def initialize_inventory(self):
        from inventory import Inventory
        self.inventory = Inventory()

    def gain_exp(self, amount: int) -> None:
        print(f"{self.name} получает {amount} опыта!")
        self.exp += amount
        if self.exp >= 10 * self.level:
            self.level_up()

    def level_up(self) -> None:
        self.level += 1
        self.exp -= 10 * (self.level - 1)  # Оставляем "излишек" опыта после повышения уровня
        self.max_hp += 30  # Увеличение максимального здоровья
        self.hp = self.max_hp  # Полное восстановление здоровья при повышении уровня
        self.attack_power += 5  # Увеличение силы атаки
        self.miss_chance = max(0, self.miss_chance - 0.005)  # Уменьшаем шанс промаха, минимум 0%
        print(f"{self.name} повысил уровень!")
        print(f"Уровень: {self.level}, здоровье: {self.hp}, сила атаки: {self.attack_power}, шанс промаха: {self.miss_chance * 100:.1f}%")

    def heal(self) -> None:
        heal_amount = int(self.max_hp * 0.2)  # Восстановление 20% от максимального здоровья
        self.hp = min(self.max_hp, self.hp + heal_amount)  # Здоровье не может превышать максимум
        print(f"{self.name} восстанавливает {heal_amount} здоровья. Текущее здоровье: {self.hp}/{self.max_hp}")

    def print_stats(self) -> None:
        exp_needed = 10 * self.level - self.exp
        print(f"\n=== Статистика {self.name} ===")
        print(f"Уровень: {self.level}")
        print(f"Опыт: {self.exp}")
        print(f"Опыт до следующего уровня: {exp_needed}")
        print(f"Текущее здоровье: {self.hp}/{self.max_hp}")
        print(f"Сила атаки: {self.attack_power}")
        print(f"Шанс промаха: {self.miss_chance * 100:.1f}%")
        if self.inventory:
            self.inventory.show_inventory()

    def do(self, target: Animal) -> None:
        if random.random() < self.miss_chance:  # Шанс промаха
            print(f"{self.name} атакует {target.name}, но промахивается!")
        else:
            # Проверка критического удара
            is_critical = random.random() < self.crit_chance
            damage = self.attack_power * (2 if is_critical else 1)

            if is_critical:
                print(f"{self.name} наносит критический урон: {damage}!")
            else:
                print(f"{self.name} атакует и наносит урон: {damage}!")

            target.hp -= damage
            print(f"У {target.name} осталось {target.hp} здоровья.")

            if target.hp <= 0:
                target.hp = 0
                print(f"{target.name} пал в бою!")

    def finish_off(self, target: Animal) -> None:
        if target.hp <= 0:
            print(f"{self.name} добивает {target.name} в эффектном прыжке!")
        else:
            print(f"{self.name} не может добить {target.name}, потому что он ещё жив!")

    def activate_cheat(self) -> None:
        cheat_menu(self)

def cheat_menu(hero: HeroDog) -> None:
    while True:
        print("\n--- Чит-меню ---")
        print("1. Изменить здоровье")
        print("2. Изменить уровень")
        print("3. Изменить атаку")
        print("4. Изменить шанс промаха")
        print("5. Выход из чит-меню")
        choice = input("Выберите действие: ")

        if choice == "1":
            try:
                new_health = int(input("Введите новое значение здоровья: "))
                if new_health < 0:
                    print("Ошибка: значение здоровья не может быть отрицательным.")
                else:
                    hero.hp = new_health
                    hero.max_hp = new_health
                    print(f"Здоровье героя установлено на {new_health}.")
            except ValueError:
                print("Ошибка: необходимо ввести целое число.")

        elif choice == "2":
            try:
                new_level = int(input("Введите новый уровень: "))
                if new_level < 1:
                    print("Ошибка: уровень должен быть не менее 1.")
                else:
                    hero.level = new_level
                    hero.attack_power += 5 * (new_level - 1)
                    print(f"Уровень героя установлен на {new_level}.")
            except ValueError:
                print("Ошибка: необходимо ввести целое число.")

        elif choice == "3":
            try:
                new_attack = int(input("Введите новое значение атаки: "))
                if new_attack < 0:
                    print("Ошибка: значение атаки не может быть отрицательным.")
                else:
                    hero.attack_power = new_attack
                    print(f"Сила атаки героя установлена на {new_attack}.")
            except ValueError:
                print("Ошибка: необходимо ввести целое число.")

        elif choice == "4":
            try:
                new_miss_chance = float(input("Введите новый шанс промаха (в процентах): "))
                if new_miss_chance < 0 or new_miss_chance > 100:
                    print("Ошибка: шанс промаха должен быть в пределах от 0 до 100.")
                else:
                    hero.miss_chance = new_miss_chance / 100
                    print(f"Шанс промаха установлен на {new_miss_chance}%.")
            except ValueError:
                print("Ошибка: необходимо ввести число.")

        elif choice == "5":
            print("Выход из чит-меню.")
            break
        else:
            print("Ошибка: неверный выбор. Попробуйте снова.")