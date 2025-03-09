from characters import Dog
from hero import HeroDog
from enemies import SkilledEnemy 

def delay_print(text: str, delay: int = 2) -> None:
    """Вывод текста с задержкой."""
    print(text)
    time.sleep(delay)

def battle(hero: HeroDog, enemy: Dog) -> None:
    delay_print(f"\n--- Сражение: {hero.name} против {enemy.name} ---", 2)
    while enemy.hp > 0 and hero.hp > 0:
        print("\nВаш ход:")
        print("1. Атаковать")
        print("2. Защищаться")
        print("3. Бежать")
        print("4. Проверить инвентарь")
        choice = input("Ваш выбор: ")

        if choice == "1":
            hero.do(enemy)
        elif choice == "2":
            print(f"{hero.name} защищается и снижает входящий урон.")
            hero.hp = min(hero.hp + 5, hero.max_hp)  # Восстановление здоровья
        elif choice == "3":
            print(f"{hero.name} пытается убежать...")
            if random.random() > 0.5:
                print("Успешный побег!")
                return
            else:
                print("Побег не удался!")
        elif choice == "4":
            hero.inventory.show_inventory()
            continue
        else:
            print("Неверный выбор, попробуйте снова.")
            continue

        if enemy.hp > 0:
            enemy.do(hero)

        if hero.hp <= 0:
            delay_print(f"\n{hero.name} пал в бою с {enemy.name}. Игра окончена!", 3)
            exit()

    if enemy.hp <= 0:
        hero.finish_off(enemy)
        hero.gain_exp(enemy.exp_reward())

    hero.heal()
    hero.print_stats()

def training(hero: HeroDog) -> None:
    enemies = [
        SmallEnemy("Маленький враг"),
        BigEnemy("Большой враг"),
        SkilledEnemy("Опытный враг"),
    ]
    while True:
        print("\nВыберите врага для тренировки:")
        for i, enemy in enumerate(enemies, 1):
            print(f"{i}. {enemy.name} (Здоровье: {enemy.hp}, Опыт за победу: {enemy.exp_reward()})")
        print("0. Закончить тренировки и идти на главного босса")

        choice = input("Ваш выбор: ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                print("\nАркадий решает закончить тренировки и готовится к встрече с Павлом!")
                break
            elif 1 <= choice <= len(enemies):
                enemy = enemies[choice - 1]
                battle(hero, enemy)
                if enemy.hp <= 0:
                    enemies[choice - 1] = type(enemy)(enemy.name)
            else:
                print("Неверный выбор. Попробуйте снова.")
        else:
            print("Пожалуйста, введите число.")

def final_battle(hero: HeroDog) -> None:
    boss = Boss("Павел", 500)  # ХП 500, урон 50
    delay_print(f"\n--- Финальная битва: {hero.name} против {boss.name}! ---", 2)

    while boss.hp > 0 and hero.hp > 0:
        print("\nВаш ход:")
        print("1. Атаковать")
        print("2. Защищаться")
        print("3. Бежать")
        print("4. Проверить инвентарь")
        choice = input("Ваш выбор: ")

        if choice == "1":
            # Проверка уворота босса
            if boss.dodge():
                print(f"{boss.name} уклоняется от атаки!")
            else:
                hero.do(boss)
        elif choice == "2":
            print(f"{hero.name} защищается и снижает входящий урон.")
            hero.hp = min(hero.hp + 5, hero.max_hp)  # Восстановление здоровья
        elif choice == "3":
            print(f"{hero.name} пытается убежать...")
            if random.random() > 0.5:
                print("Успешный побег! Но финальная битва неизбежна.")
                return
            else:
                print("Побег не удался!")
        elif choice == "4":
            hero.inventory.show_inventory()
            continue
        else:
            print("Неверный выбор, попробуйте снова.")
            continue

        # Атака босса
        if boss.hp > 0:
            boss.do(hero)

        if hero.hp <= 0:
            delay_print(f"\n{hero.name} пал в битве с {boss.name}. Игра окончена!", 3)
            exit()

    if boss.hp <= 0:
        delay_print(f"\nПоздравляем! {hero.name} победил {boss.name} и стал настоящим героем!", 3)
        hero.gain_exp(50)  # Награда за победу
        hero.print_stats()