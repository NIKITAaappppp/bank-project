from bank.bankmodels import BankAccount, money
from datetime import datetime

class Bank:
    """Класс-агрегатор: хранит аккаунты и историю транзакций."""

    def __init__(self):
        # Словарь: ключ — нормализованное имя (lower+strip), значение — BankAccount
        self._accounts: dict[str, BankAccount] = {}
        # Список транзакций (каждая транзакция — словарь)
        self.transactions: list[dict] = []

    def _key(self, name: str) -> str:
        """Нормализация имени для ключа словаря."""
        return name.strip().lower()

    def add_account(self, account: BankAccount):
        """Добавляет аккаунт; если имя уже есть — ValueError."""
        k = self._key(account.name)
        if k in self._accounts:
            raise ValueError(f"Account with name '{account.name}' already exists")
        self._accounts[k] = account

    def _log(self, kind: str, amount, src: str, dst: str | None = None):
        """
        Формирует и сохраняет запись транзакции.
        amount сохраняем как строку (чтобы JSON-дамп прошёл без проблем).
        """
        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "type": kind,
            "amount": str(money(amount)),
            "from": src,
            "to": dst,
        }
        self.transactions.append(entry)

    def get_account(self, name: str) -> BankAccount:
        """Ищет аккаунт по имени; если не найден — LookupError."""
        acc = self._accounts.get(self._key(name))
        if acc is None:
            raise LookupError(f"Account with name '{name}' does not exist")
        return acc

    def deposit(self, name: str, amount):
        """Пополнение по имени: находит аккаунт, кладёт деньги, логирует."""
        acc = self.get_account(name)
        acc.deposit(amount)  # BankAccount.deposit сам вызовет money() и проверит
        self._log("deposit", amount, acc.name)

    def withdraw(self, name: str, amount):
        """Снятие по имени: находит, снимает, логирует."""
        acc = self.get_account(name)
        acc.withdraw(amount)
        self._log("withdraw", amount, acc.name)

    def transfer(self, from_name: str, to_name: str, amount):
        """Перевод: снимаем со src, добавляем dst, логируем перевод."""
        src = self.get_account(from_name)
        dst = self.get_account(to_name)
        # Если один из вызовов выбросит — перевод отменится (исключение поднимется)
        src.withdraw(amount)
        dst.deposit(amount)
        self._log("transfer", amount, src.name, dst.name)

    def accounts(self) -> list[BankAccount]:
        """Возвращает список всех объектов BankAccount."""
        return list(self._accounts.values())

    def show_transactions(self):
        """Печатает пользователю форматированную историю транзакций."""
        if not self.transactions:
            print("История транзакций пуста.")
            return
        for t in self.transactions:
            ts = t.get("timestamp", "")
            typ = t.get("type", "")
            amt = t.get("amount", "0.00")
            src = t.get("from", "")
            dst = t.get("to", None)
            if typ == "deposit":
                print(f"[{ts}] {src} пополнил счёт на {amt}")
            elif typ == "withdraw":
                print(f"[{ts}] {src} снял {amt}")
            elif typ == "transfer":
                print(f"[{ts}] {src} перевёл {amt} → {dst}")
            else:
                print(f"[{ts}] {typ} {amt} ({src} → {dst})")
