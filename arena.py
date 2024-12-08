import time
import random
from io_module import io  # Импортируем наш модуль для ввода/вывода

# Функция для задержанного вывода текста
# удалена за ненадобностью - теперь весь вывод в io_module
# def delay_print(text, delay=2):
#     """Вывод текста с задержкой."""
#     print(text)
#     time.sleep(delay)

# класс предметов
class Item:
    def __init__(self, name, description, debuffs=None, throw_damage=0):
        self.name = name
        self.description = description
        self.debuffs = debuffs if debuffs else []
        self.throw_damage = throw_damage

    def use(self, user):
        raise NotImplementedError("Метод использования должен быть переопределён.")

# Класс инвентаря
class Inventory:
    def __init__(self):
        self.items = {}  # Словарь {название_предмета: количество}
        self.debuffs = []  # Список активных дебаффов

    def add_item(self, item_name, quantity=1):
        """Добавление предмета в инвентарь"""
        if item_name in self.items:
            self.items[item_name] += quantity  # Увеличиваем количество, если предмет уже есть
        else:
            self.items[item_name] = quantity  # Добавляем новый предмет
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Добавлено {quantity}x {item_name}. Всего: {self.items[item_name]}.")

    def remove_item(self, item_name, quantity=1):
        """Удаление предмета из инвентаря"""
        if item_name in self.items:
            self.items[item_name] -= quantity
            if self.items[item_name] <= 0:
                del self.items[item_name]
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"Удалено {quantity}x {item_name}.")
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"Предмет {item_name} отсутствует в инвентаре.")

    def show_inventory(self):
        """Вывод содержимого инвентаря"""
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("=====:Ваш инвентарь:=====")
        if not self.items:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print("Пусто")
        for item_name, quantity in self.items.items():
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{item_name}: {quantity}")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("=========================")

    def view_item_properties(self, item_name):
        """Просмотр свойств предмета"""
        if item_name not in self.items:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"Предмет {item_name} отсутствует в инвентаре.")
            return
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Название: {item_name}")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Количество: {self.items[item_name]}")
        # Для демонстрации дебаффов
        if "debuff" in item_name.lower():
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print("Дебафф: снижает скорость восстановления здоровья.")

    def use_item(self, item_name, user):
        """Использование предмета"""
        if "NoHealing" in [d["type"] for d in self.debuffs]:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print("Вы не можете использовать зелья лечения из-за дебаффа!")
            return
        if item_name not in self.items or self.items[item_name] <= 0:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"Предмет {item_name} отсутствует в инвентаре.")
            return
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"{user} использовал {item_name}!")
        self.remove_item(item_name)

    def discard_item(self, item_name):
        """Выбрасывание предмета"""
        if item_name in self.items:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"Вы выбросили {item_name}.")
            del self.items[item_name]
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"Предмет {item_name} отсутствует в инвентаре.")

    def throw_item(self, item_name, target):
        """Бросок предмета в противника"""
        if "damage" not in item_name.lower():
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print("Этот предмет нельзя бросить!")
            return
        damage = 10  # Условный урон от броска
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Вы бросили {item_name} в {target}, нанеся {damage} урона!")
        self.remove_item(item_name)




# Базовый класс животных
class Animal:
    def __init__(self, name, hp, color="неизвестный"):
        self.name = name
        self.hp = hp
        self.color = color

# Класс псов, наследует от Animal
class Dog(Animal):
    def do(self, target):
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"{self.name} атакует {target.name} -> Гав!")

# Класс главного героя — пёс Аркадий
class HeroDog(Dog):
    def __init__(self, name, hp, color="чёрный"):
        super().__init__(name, hp, color)
        self.level = 1
        self.exp = 0
        self.max_hp = hp  # Максимальное здоровье героя
        self.attack_power = 10  # Инициализация силы атаки
        self.miss_chance = 0.2  # Начальный шанс промаха (20%)
        self.crit_chance = 0.05  # Шанс критического удара (5%)
        self.inventory = Inventory()  # Инвентарь

    def gain_exp(self, amount):
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"{self.name} получает {amount} опыта!")
        self.exp += amount
        if self.exp >= 10 * self.level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= 10 * (self.level - 1)  # Оставляем "излишек" опыта после повышения уровня
        self.max_hp += 30  # Увеличение максимального здоровья
        self.hp = self.max_hp  # Полное восстановление здоровья при повышении уровня
        self.attack_power += 5  # Увеличение силы атаки
        self.miss_chance = max(0, self.miss_chance - 0.005)  # Уменьшаем шанс промаха, минимум 0%
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"{self.name} повысил уровень!")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Уровень: {self.level}, здоровье: {self.hp}, сила атаки: {self.attack_power}, шанс промаха: {self.miss_chance * 100:.1f}%")

    def heal(self):
        heal_amount = int(self.max_hp * 0.2)  # Восстановление 20% от максимального здоровья
        self.hp = min(self.max_hp, self.hp + heal_amount)  # Здоровье не может превышать максимум
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"{self.name} восстанавливает {heal_amount} здоровья. Текущее здоровье: {self.hp}/{self.max_hp}")

    def print_stats(self):
        exp_needed = 10 * self.level - self.exp
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"\n=== Статистика Аркадия ===")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Уровень: {self.level}")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Опыт: {self.exp}")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Опыт до следующего уровня: {exp_needed}")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Текущее здоровье: {self.hp}/{self.max_hp}")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Сила атаки: {self.attack_power}")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Шанс промаха: {self.miss_chance * 100:.1f}%")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("==========================\n")

    def do(self, target):
        if random.random() < self.miss_chance:  # Шанс промаха
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} атакует {target.name}, но промахивается!")
        else:
            damage = self.attack_power
            target.hp -= damage
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} атакует {target.name}! Нанесено {damage} урона. У {target.name} осталось {target.hp} здоровья.")

        # Проверка критического удара
        is_critical = random.random() < self.crit_chance
        damage = self.attack_power * (2 if is_critical else 1)

        if is_critical:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} наносит критический урон: {damage}!")
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} атакует и наносит урон: {damage}!")

        target.hp -= damage

        if target.hp <= 0:
            target.hp = 0
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{target.name} пал в бою!")

    def finish_off(self, target):
        if target.hp <= 0:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} добивает {target.name} в эффектном прыжке!")
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} не может добить {target.name}, потому что он ещё жив!")

    def activate_cheat(self):
        cheat_menu(self)

    def print_stats(self):
        exp_needed = 10 * self.level - self.exp
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"\n=== Статистика Аркадия ===")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Уровень: {self.level}")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Опыт: {self.exp}")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Опыт до следующего уровня: {exp_needed}")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Текущее здоровье: {self.hp}/{self.max_hp}")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Сила атаки: {self.attack_power}")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"Шанс промаха: {self.miss_chance * 100:.1f}%")
        self.inventory.show_inventory()



def cheat_menu(self):
    while True:
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("\n--- Чит-меню ---")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("1. Изменить здоровье")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("2. Изменить уровень")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("3. Изменить атаку")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("4. Изменить шанс промаха")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("5. Выход из чит-меню")
        # ИЗМЕНЕНИЕ: используем io.input вместо input
        choice = io.input("Выберите действие: ")

        if choice == "1":
            try:
                # ИЗМЕНЕНИЕ: используем io.input вместо input
                new_health = int(io.input("Введите новое значение здоровья: "))
                if new_health < 0:
                    # ИЗМЕНЕНИЕ: используем io.print вместо print
                    io.print("Ошибка: значение здоровья не может быть отрицательным.")
                else:
                    self.health = new_health
                    self.max_health = new_health
                    # ИЗМЕНЕНИЕ: используем io.print вместо print
                    io.print(f"Здоровье героя установлено на {new_health}.")
            except ValueError:
                # ИЗМЕНЕНИЕ: используем io.print вместо print
                io.print("Ошибка: необходимо ввести целое число.")

        elif choice == "2":
            try:
                # ИЗМЕНЕНИЕ: используем io.input вместо input
                new_level = int(io.input("Введите новый уровень: "))
                if new_level < 1:
                    # ИЗМЕНЕНИЕ: используем io.print вместо print
                    io.print("Ошибка: уровень должен быть не менее 1.")
                else:
                    self.level = new_level
                    self.attack += 5 * (new_level - 1)
                    # ИЗМЕНЕНИЕ: используем io.print вместо print
                    io.print(f"Уровень героя установлен на {new_level}.")
            except ValueError:
                # ИЗМЕНЕНИЕ: используем io.print вместо print
                io.print("Ошибка: необходимо ввести целое число.")

        elif choice == "3":
            try:
                # ИЗМЕНЕНИЕ: используем io.input вместо input
                new_attack = int(io.input("Введите новое значение атаки: "))
                if new_attack < 0:
                    # ИЗМЕНЕНИЕ: используем io.print вместо print
                    io.print("Ошибка: значение атаки не может быть отрицательным.")
                else:
                    self.attack = new_attack
                    # ИЗМЕНЕНИЕ: используем io.print вместо print
                    io.print(f"Сила атаки героя установлена на {new_attack}.")
            except ValueError:
                # ИЗМЕНЕНИЕ: используем io.print вместо print
                io.print("Ошибка: необходимо ввести целое число.")

        elif choice == "4":
            try:
                # ИЗМЕНЕНИЕ: используем io.input вместо input
                new_miss_chance = float(io.input("Введите новый шанс промаха (в процентах): "))
                if new_miss_chance < 0 or new_miss_chance > 100:
                    # ИЗМЕНЕНИЕ: используем io.print вместо print
                    io.print("Ошибка: шанс промаха должен быть в пределах от 0 до 100.")
                else:
                    self.miss_chance = new_miss_chance
                    # ИЗМЕНЕНИЕ: используем io.print вместо print
                    io.print(f"Шанс промаха установлен на {new_miss_chance}%.")
            except ValueError:
                # ИЗМЕНЕНИЕ: используем io.print вместо print
                io.print("Ошибка: необходимо ввести число.")

        elif choice == "5":
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print("Выход из чит-меню.")
            break
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print("Ошибка: неверный выбор. Попробуйте снова.")

# Враги с уникальными атаками
class SmallEnemy(Dog):
    def __init__(self, name):
        super().__init__(name, hp=20)
        self.crit_chance = 0.08  # Шанс критического удара (8%)

    def do(self, target):
        damage = 5
        target.hp -= damage
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"{self.name} кусает {target.name}! Нанесено {damage} урона. У {target.name} осталось {target.hp} здоровья.")

        is_critical = random.random() < self.crit_chance
        damage = 5 * (1.5 if is_critical else 1)  # Урон увеличивается на 150% при критическом ударе

        if is_critical:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} наносит критический урон: {damage}!")
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} атакует и наносит урон: {damage}.")

        target.hp -= damage
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"У {target.name} осталось {target.hp} здоровья.")

    def exp_reward(self):
        return 5

class BigEnemy(Dog):
    def __init__(self, name):
        super().__init__(name, hp=40)
        self.crit_chance = 0.08  # Шанс критического удара (8%)

    def do(self, target):
        damage = 10
        target.hp -= damage
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"{self.name} с силой бьёт {target.name}! Нанесено {damage} урона. У {target.name} осталось {target.hp} здоровья.")

        is_critical = random.random() < self.crit_chance
        damage = 10 * (1.5 if is_critical else 1)  # Урон увеличивается на 150% при критическом ударе

        if is_critical:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} наносит критический урон: {damage}!")
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} атакует и наносит урон: {damage}.")

        target.hp -= damage
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"У {target.name} осталось {target.hp} здоровья.")

    def exp_reward(self):
        return 10

class SkilledEnemy(Dog):
    def __init__(self, name):
        super().__init__(name, hp=60)
        self.crit_chance = 0.08  # Шанс критического удара (8%)

    def do(self, target):
        damage = 15
        target.hp -= damage
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"{self.name} проводит сложную атаку на {target.name}! Нанесено {damage} урона. У {target.name} осталось {target.hp} здоровья.")

        is_critical = random.random() < self.crit_chance
        damage = 15 * (1.5 if is_critical else 1)  # Урон увеличивается на 150% при критическом ударе

        if is_critical:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} наносит критический урон: {damage}!")
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} атакует и наносит урон: {damage}.")

        target.hp -= damage
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print(f"У {target.name} осталось {target.hp} здоровья.")

    def exp_reward(self):
        return 20

# Главный босс — Пёс Павел
class Boss(Dog):
    def __init__(self, name, hp, attack_power=50):
        super().__init__(name, hp)
        self.attack_power = attack_power
        self.crit_chance = 0.1  # Шанс критического удара (10%)
        self.miss_chance = 0.015  # Шанс промаха (1.5%)
        self.dodge_chance = 0.05  # Шанс уворота (5%)

    def do(self, target):
        # Проверка промаха
        if random.random() < self.miss_chance:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} промахивается!")
            return

        # Проверка критического удара
        is_critical = random.random() < self.crit_chance
        damage = self.attack_power * (1.5 if is_critical else 1)

        if is_critical:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} наносит критический урон: {damage}!")
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{self.name} атакует и наносит урон: {damage}!")

        target.hp -= damage

        # Проверка состояния героя
        if target.hp <= 0:
            target.hp = 0
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{target.name} пал в бою!")

    def dodge(self):
        return random.random() < self.dodge_chance

# Система тренировок
def training(hero):
    enemies = [
        SmallEnemy("Маленький враг"),
        BigEnemy("Большой враг"),
        SkilledEnemy("Опытный враг"),
    ]
    while True:
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("\nВыберите врага для тренировки:")
        for i, enemy in enumerate(enemies, 1):
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{i}. {enemy.name} (Здоровье: {enemy.hp}, Опыт за победу: {enemy.exp_reward()})")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("0. Закончить тренировки и идти на главного босса")

        # ИЗМЕНЕНИЕ: используем io.input вместо input
        choice = io.input("Ваш выбор: ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                # ИЗМЕНЕНИЕ: используем io.print вместо print
                io.print("\nАркадий решает закончить тренировки и готовится к встрече с Павлом!")
                break
            elif 1 <= choice <= len(enemies):
                enemy = enemies[choice - 1]
                battle(hero, enemy)
                if enemy.hp <= 0:
                    enemies[choice - 1] = type(enemy)(enemy.name)
            else:
                # ИЗМЕНЕНИЕ: используем io.print вместо print
                io.print("Неверный выбор. Попробуйте снова.")
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print("Пожалуйста, введите число.")

# Сражение
def battle(hero, enemy):
    # ИЗМЕНЕНИЕ: используем io.delay_print вместо delay_print
    io.delay_print(f"\n--- Сражение: {hero.name} против {enemy.name} ---", 2)
    while enemy.hp > 0 and hero.hp > 0:
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("\nВаш ход:")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("1. Атаковать")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("2. Защищаться")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("3. Бежать")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("4. Проверить инвентарь")
        # ИЗМЕНЕНИЕ: используем io.input вместо input
        choice = io.input("Ваш выбор: ")

        if choice == "1":
            hero.do(enemy)
        elif choice == "2":
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{hero.name} защищается и снижает входящий урон.")
            hero.hp = min(hero.hp + 5, hero.max_hp)  # Восстановление здоровья
        elif choice == "3":
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{hero.name} пытается убежать...")
            if random.random() > 0.5:
                # ИЗМЕНЕНИЕ: используем io.print вместо print
                io.print("Успешный побег!")
                return
            else:
                # ИЗМЕНЕНИЕ: используем io.print вместо print
                io.print("Побег не удался!")
        elif choice == "4":
            hero.inventory.show_inventory()
            continue
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print("Неверный выбор, попробуйте снова.")
            continue

        if enemy.hp > 0:
            enemy.do(hero)

        if hero.hp <= 0:
            # ИЗМЕНЕНИЕ: используем io.delay_print вместо delay_print
            io.delay_print(f"\n{hero.name} пал в бою с {enemy.name}. Игра окончена!", 3)
            exit()

    if enemy.hp <= 0:
        hero.finish_off(enemy)
        hero.gain_exp(enemy.exp_reward())

    hero.heal()
    hero.print_stats()

# Финальная битва
def final_battle(hero):
    boss = Boss("Павел", 500)  # ХП 500, урон 50
    # ИЗМЕНЕНИЕ: используем io.delay_print вместо delay_print
    io.delay_print(f"\n--- Финальная битва: {hero.name} против {boss.name}! ---", 2)

    while boss.hp > 0 and hero.hp > 0:
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("\nВаш ход:")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("1. Атаковать")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("2. Защищаться")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("3. Бежать")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("4. Проверить инвентарь")
        # ИЗМЕНЕНИЕ: используем io.input вместо input
        choice = io.input("Ваш выбор: ")

        if choice == "1":
            # Проверка уворота босса
            if boss.dodge():
                # ИЗМЕНЕНИЕ: используем io.print вместо print
                io.print(f"{boss.name} уклоняется от атаки!")
            else:
                hero.do(boss)
        elif choice == "2":
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{hero.name} защищается и снижает входящий урон.")
            hero.hp = min(hero.hp + 5, hero.max_hp)  # Восстановление здоровья
        elif choice == "3":
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print(f"{hero.name} пытается убежать...")
            if random.random() > 0.5:
                # ИЗМЕНЕНИЕ: используем io.print вместо print
                io.print("Успешный побег! Но финальная битва неизбежна.")
                return
            else:
                # ИЗМЕНЕНИЕ: используем io.print вместо print
                io.print("Побег не удался!")
        elif choice == "4":
            hero.inventory.show_inventory()
            continue
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print("Неверный выбор, попробуйте снова.")
            continue

        # Атака босса
        if boss.hp > 0:
            boss.do(hero)

        if hero.hp <= 0:
            # ИЗМЕНЕНИЕ: используем io.delay_print вместо delay_print
            io.delay_print(f"\n{hero.name} пал в битве с {boss.name}. Игра окончена!", 3)
            exit()

    if boss.hp <= 0:
        # ИЗМЕНЕНИЕ: используем io.delay_print вместо delay_print
        io.delay_print(f"\nПоздравляем! {hero.name} победил {boss.name} и стал настоящим героем!", 3)
        hero.gain_exp(50)  # Награда за победу
        hero.print_stats()

# Игра
def main():
    arkady = HeroDog("Аркадий", 100)
    arkady.inventory.add_item("Лечебное зелье", 3)  # Добавляем стартовые предметы
    # ИЗМЕНЕНИЕ: используем io.print вместо print
    io.print("\n--- Аркадий готовится к встрече с Павлом! ---")
    while True:
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("\nЧто вы хотите сделать?")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("1. Тренироваться с мобами")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("2. Идти на главного босса")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("3. Ввести чит-команду")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("4. Проверить инвентарь")
        # ИЗМЕНЕНИЕ: используем io.print вместо print
        io.print("5. Выйти из игры")
        # ИЗМЕНЕНИЕ: используем io.input вместо input
        choice = io.input("Ваш выбор: ")

        if choice == "1":
            training(arkady)
        elif choice == "2":
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print("\nАркадий решает идти на встречу с Павлом!")
            final_battle(arkady)
            break
        elif choice == "3":
            # ИЗМЕНЕНИЕ: используем io.input вместо input
            cheat_code = io.input("Введите чит-команду: ")
            if cheat_code == "PAVEL_BOG":
                arkady.activate_cheat()
            else:
                # ИЗМЕНЕНИЕ: используем io.print вместо print
                io.print("Неверная чит-команда.")
        elif choice == "4":
            arkady.inventory.show_inventory()
        elif choice == "5":
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print("Игра завершена. До новых встреч!")
            break
        else:
            # ИЗМЕНЕНИЕ: используем io.print вместо print
            io.print("Неверный выбор. Попробуйте снова.")

main()