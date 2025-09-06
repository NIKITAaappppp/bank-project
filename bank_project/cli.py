from bank.bankmodels import BankAccount, money
from bank.bankservices import Bank
from bank.repo import save_bank, load_bank

def parse_amount(prompt: str):
    """
    Считывает ввод суммы, заменяет запятую на точку, пытается вернуть Decimal через money().
    Бросает ValueError при некорректном вводе.
    """
    raw = input(prompt).strip()
    if raw == "":
        raise ValueError("Пустая строка")
    # заменяем запятую на точку — часто пользователи вводят "100,50"
    raw = raw.replace(",", ".")
    return money(raw)

def menu():
    bank = Bank()
    load_bank(bank)  # загружаем, если есть файл

    while True:
        print("\n=== Меню банка ===")
        print("1. Добавить клиента")
        print("2. Показать всех клиентов")
        print("3. Найти клиента")
        print("4. Пополнить счёт")
        print("5. Снять деньги")
        print("6. Перевести деньги")
        print("7. Показать историю транзакций")
        print("8. Сохранить и выйти")

        choice = input("Выберите пункт: ").strip()

        try:
            if choice == "1":
                name = input("Имя клиента: ").strip()
                initial = parse_amount("Начальный депозит: ")
                account = BankAccount(name, initial)
                bank.add_account(account)
                print(f"✅ Счёт для {name} создан. Баланс: {account.balance}")

            elif choice == "2":
                accounts = bank.accounts()
                if not accounts:
                    print("Нет клиентов.")
                else:
                    for acc in accounts:
                        print(f"{acc.name}: {acc.balance}")

            elif choice == "3":
                name = input("Имя клиента для поиска: ").strip()
                acc = bank.get_account(name)
                print(f"Найден: {acc.name}. Баланс: {acc.balance}")

            elif choice == "4":
                name = input("Имя клиента: ").strip()
                amt = parse_amount("Сумма пополнения: ")
                bank.deposit(name, amt)
                print("✅ Пополнение выполнено.")

            elif choice == "5":
                name = input("Имя клиента: ").strip()
                amt = parse_amount("Сумма снятия: ")
                bank.withdraw(name, amt)
                print("✅ Снятие выполнено.")

            elif choice == "6":
                src = input("Отправитель: ").strip()
                dst = input("Получатель: ").strip()
                amt = parse_amount("Сумма перевода: ")
                bank.transfer(src, dst, amt)
                print("✅ Перевод выполнен.")

            elif choice == "7":
                bank.show_transactions()

            elif choice == "8":
                save_bank(bank)
                print("Данные сохранены. Выход.")
                break

            else:
                print("Неправильный пункт, попробуйте снова.")

        except Exception as e:
            # На CLI уровне ловим исключения и показываем понятное сообщение
            print("Ошибка:", e)


if __name__ == "__main__":
    menu()
