from decimal import Decimal, ROUND_HALF_UP, getcontext

# Настройка Decimal: точность операций (задаём большой запас)
getcontext().prec = 28


def money(x) -> Decimal:
    """
    Преобразует вход (int/float/str/Decimal) в Decimal с 2 знаками после запятой.
    Бросает ValueError для некорректных входных данных.
    """
    try:
        # Если это строка — заменяем запятую на точку (пользователь мог ввести "100,50")
        if isinstance(x, str):
            x = x.replace(",", ".").strip()

        # Конвертация через str(x) защищает от проблем float-представления
        d = Decimal(str(x))
        # quantize — округляем до 2 десятичных знаков (копейки)
        return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except Exception as exc:
        raise ValueError(f"Некорректная денежная сумма: {x}") from exc


class BankAccount:
    """Модель банковского счёта — имя и баланс (Decimal)."""

    def __init__(self, name: str, balance=0):
        # Имя клиента (храним как передали)
        self.name = name
        # Баланс — хранится как Decimal через функцию money
        self._balance = money(balance)

    def deposit(self, amount):
        """Пополнение: принимает любую форму (int/float/str/Decimal)."""
        amt = money(amount)
        if amt <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self._balance += amt

    def withdraw(self, amount):
        """Снятие: проверяем положительность и достаточность средств."""
        amt = money(amount)
        if amt <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amt > self._balance:
            raise ValueError("Недостаточно средств для снятия")
        self._balance -= amt

    @property
    def balance(self):
        """Геттер баланса (возвращает Decimal)."""
        return self._balance

    def to_dict(self) -> dict:
        """Представление для сохранения в JSON: баланс — строка для безопасности."""
        return {"name": self.name, "balance": str(self._balance)}

    @classmethod
    def from_dict(cls, data: dict):
        """Создать BankAccount из словаря (используется при загрузке)."""
        return cls(data["name"], data["balance"])
