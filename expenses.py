import os
import sqlite3
from datetime import datetime


class Expense:
    def __init__(self, amount: float, category: str, date: str = None):
        self.amount = amount
        self.category = category
        self.date = date if date else datetime.now().strftime('%Y-%m-%d')

    def __str__(self):
        return f"{self.date} | {self.category} | {self.amount:.2f} руб."


class ExpenseTracker:
    def __init__(self, db_name: str = "expenses.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.current_table = self._get_current_month_table()
        self._create_month_table_if_not_exists()

    def _get_current_month_table(self) -> str:
        now = datetime.now()
        return f"expenses_{now.year}_{now.month:02d}"

    def _create_month_table_if_not_exists(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.current_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL
            )
        """)
        self.conn.commit()

    def add_expense(self, expense: Expense):
        self.cursor.execute(f"""
            INSERT INTO {self.current_table} (date, category, amount)
            VALUES (?, ?, ?)
        """, (expense.date, expense.category, expense.amount))
        self.conn.commit()

    def show_expenses(self):
        self.cursor.execute(f"SELECT date, category, amount FROM {self.current_table}")
        rows = self.cursor.fetchall()
        if not rows:
            print("Расходов пока нет.")
        else:
            for row in rows:
                print(f"{row[0]} | {row[1]} | {row[2]:.2f} руб.")

    def total_current_month(self):
        self.cursor.execute(f"SELECT SUM(amount) FROM {self.current_table}")
        total = self.cursor.fetchone()[0]
        total = total if total else 0
        print(f"Общие расходы за месяц: {total:.2f} руб.")

    def close(self):
        self.conn.close()


def main():
    print("🔍 Проверка базы данных...")
    if not os.path.exists("expenses.db"):
        print("📁 База данных не найдена. Создаю новую...")
    else:
        print("✅ База данных найдена.")

    tracker = ExpenseTracker()

    while True:
        print("\n--- Учет расходов ---")
        print("1. Добавить расход")
        print("2. Показать все расходы")
        print("3. Общая сумма за месяц")
        print("4. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            try:
                amount = float(input("Сумма: "))
                category = input("Категория: ")
                tracker.add_expense(Expense(amount, category))
                print("✔ Расход добавлен.")
            except ValueError:
                print("❌ Ошибка: введите число.")

        elif choice == '2':
            tracker.show_expenses()

        elif choice == '3':
            tracker.total_current_month()

        elif choice == '4':
            tracker.close()
            print("💾 Данные сохранены. До свидания!")
            break

        else:
            print("❌ Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
1
2
3
4
5
6
7
