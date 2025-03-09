"""
Модуль с базовыми классами персонажей игры.
Содержит иерархию классов от базового Animal до специализированных подклассов.
"""

class Animal:
    """
    Базовый класс для всех животных в игре.
    Определяет основные атрибуты и методы, общие для всех животных.
    """
    def __init__(self, name: str, hp: int, color: str = "белый"):
        """
        Инициализация животного.

        Args:
            name: Имя животного
            hp: Начальное количество здоровья
            color: Цвет животного (по умолчанию "белый")
        """
        self.name = name
        self.hp = hp
        self.color = color

class Dog(Animal):
    """
    Класс собаки, наследующийся от Animal.
    Добавляет базовые боевые характеристики и методы.
    """
    def __init__(self, name: str, hp: int, color: str = "коричневый"):
        """
        Инициализация собаки.

        Args:
            name: Имя собаки
            hp: Начальное количество здоровья
            color: Цвет собаки (по умолчанию "коричневый")
        """
        super().__init__(name, hp, color)
        self.attack_power = 10  # Базовая сила атаки
        self.miss_chance = 0.2  # Базовый шанс промаха (20%)

    def do(self, target: Animal) -> None:
        """
        Базовый метод атаки для собаки.

        Args:
            target: Цель атаки (объект класса Animal или его наследников)
        """
        print(f"{self.name} атакует {target.name} -> Гав!")

class HeroDog(Dog):
    """
    Класс героя-собаки, управляемого игроком.
    Расширяет базовый класс Dog дополнительными возможностями и характеристиками.
    """
    def __init__(self, name: str, hp: int, color: str = "чёрный"):
        """
        Инициализация героя-собаки.

        Args:
            name: Имя героя
            hp: Начальное здоровье
            color: Цвет героя (по умолчанию "чёрный")
        """
        super().__init__(name, hp, color)
        self.level = 1  # Начальный уровень героя
        self.exp = 0  # Начальный опыт
        self.exp_to_level = 100  # Опыт, необходимый для повышения уровня
        self.max_hp = hp  # Максимальное здоровье
        self.crit_chance = 0.05  # Шанс критического удара (5%)
        self.inventory = None  # Инвентарь будет инициализирован позже

    def initialize_inventory(self):
        """
        Инициализирует инвентарь героя.
        Должен быть вызван после создания героя.
        """
        from player_inventory import Inventory
        self.inventory = Inventory()

    def gain_exp(self, amount: int) -> None:
        """
        Получение опыта героем.
        Если накоплено достаточно опыта, вызывает повышение уровня.

        Args:
            amount: Количество получаемого опыта
        """
        self.exp += amount
        print(f"{self.name} получает {amount} опыта. Всего: {self.exp}/{self.exp_to_level}")
        if self.exp >= self.exp_to_level:
            self.level_up()

    def level_up(self) -> None:
        """
        Повышение уровня героя.
        Увеличивает характеристики и сбрасывает счетчик опыта.
        """
        self.level += 1
        self.exp -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack_power += 5
        self.miss_chance *= 0.9  # Уменьшаем шанс промаха на 10%
        print(f"{self.name} достигает {self.level} уровня!")
        print(f"Уровень: {self.level}, здоровье: {self.hp}, сила атаки: {self.attack_power}, шанс промаха: {self.miss_chance * 100:.1f}%")

    def heal(self) -> None:
        """
        Восстановление здоровья героя.
        Восстанавливает часть максимального здоровья.
        """
        if self.hp >= self.max_hp:
            print(f"{self.name} уже имеет максимальное здоровье.")
            return

        heal_amount = int(self.max_hp * 0.2)  # Восстанавливаем 20% от максимального здоровья
        self.hp = min(self.hp + heal_amount, self.max_hp)
        print(f"{self.name} восстанавливает {heal_amount} здоровья. Текущее здоровье: {self.hp}/{self.max_hp}")

    def print_stats(self) -> None:
        """
        Вывод статистики героя.
        Отображает все основные характеристики и содержимое инвентаря.
        """
        print(f"\n--- Статистика {self.name} ---")
        print(f"Уровень: {self.level}")
        print(f"Опыт: {self.exp}/{self.exp_to_level}")
        print(f"Здоровье: {self.hp}/{self.max_hp}")
        print(f"Сила атаки: {self.attack_power}")
        print(f"Шанс промаха: {self.miss_chance * 100:.1f}%")
        print(f"Шанс крита: {self.crit_chance * 100:.1f}%")
        if self.inventory:
            self.inventory.show_inventory()

    def do(self, target: Animal) -> None:
        """
        Метод атаки героя.
        Включает логику промахов и критических ударов.

        Args:
            target: Цель атаки (объект класса Animal или его наследников)
        """
        import random
        if random.random() < self.miss_chance:  # Шанс промаха
            print(f"{self.name} атакует {target.name}, но промахивается!")
        else:
            # Проверка критического удара
            is_critical = random.random() < self.crit_chance
            damage = self.attack_power * 2 if is_critical else self.attack_power
            target.hp -= damage
            print(f"{self.name} атакует {target.name} -> Нанесено {damage} урона!")
            if is_critical:
                print("Критический удар!")

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