import random

def difficult():
    print("1 - Лёгкий (1..100, 8 попыток)")
    print("2 - Средний (1..300, 6 попыток)")
    print("3 - Сложный (1..700, 4 попытки)")

    while True:
        choice = input("Ваш выбор (1/2/3): ").strip()
        if choice == "1":
            return 1, 100, 8
        elif choice == "2":
            return 1, 300, 6
        elif choice == "3":
            return 1, 700, 4
        else:
            print("Ошибка: введите 1, 2 или 3")

def game(min_num, max_num, attempts):
    secret = random.randint(min_num, max_num)
    print(f"\nДиапазон: от {min_num} до {max_num}")
    print(f"Количество попыток: {attempts}\n")

    for attempt in range(1, attempts + 1):
        print(f"Попытка {attempt} из {attempts}")

        while True:
            user_input = input("Ваше число: ").strip()

            try:
                guess = int(user_input)
                if guess < min_num or guess > max_num:
                    print(f"Число должно быть от {min_num} до {max_num}")
                    continue
                break
            except ValueError:
                print("Введите целое число")

        if guess == secret:
            print(f"\nВы угадали число {secret} за {attempt} попыток")
            return "win"
        elif guess < secret:
            print("Загаданное число БОЛЬШЕ >")
        else:
            print("Загаданное число МЕНЬШЕ <")

    print(f"\nЧисло попыток исчерпано")
    print(f"Было загадано: {secret}")
    return "lose"

def main():
    while True:
        min_num, max_num, attempts = difficult()
        result = game(min_num, max_num, attempts)

        while True:
            again = input("\nХотите сыграть ещё? (да/нет): ").strip().lower()

            if again == "да":
                print()
                break
            elif again == "нет":
                return
            else:
                print("Введите 'да' или 'нет'")

if __name__ == "__main__":
    main()