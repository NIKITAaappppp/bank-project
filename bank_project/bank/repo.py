import json
from bank.bankmodels import BankAccount

def save_bank(bank, filename: str = "bank.json"):
    """
    Сохраняет все аккаунты и историю в JSON-файл.
    Балансы и суммы сохраняются как строки, чтобы не ломать сериализацию Decimal.
    """
    data = {
        "accounts": [acc.to_dict() for acc in bank.accounts()],
        "transactions": bank.transactions,
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_bank(bank, filename: str = "bank.json"):
    """
    Загружает из JSON, создаёт аккаунты и подставляет транзакции.
    Если файла нет — тихо выходит (создаётся пустой банк).
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        for acc_data in data.get("accounts", []):
            acc = BankAccount.from_dict(acc_data)
            bank.add_account(acc)
        bank.transactions = data.get("transactions", [])
    except FileNotFoundError:
        # если файла нет — ничего не грузим (пустой банк)
        pass
