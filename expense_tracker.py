import calendar
import datetime
import os
import shutil
from expense import Expense

def main():
    print("Running Expense Tracker!")
    expense_file_path = "expense.csv"

    # Backup the existing expense file
    backup_file(expense_file_path)

    # Get user to input their budget with validation
    budget = get_valid_budget()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            # Add a new expense
            expense, expense_time = user_expense()
            save_expense_to_file(expense, expense_time, expense_file_path)
        elif choice == '2':
            # Edit an existing expense
            edit_expense(expense_file_path)
        elif choice == '3':
            # Delete an existing expense
            delete_expense(expense_file_path)
        elif choice == '4':
            # Summarize expenses
            summarize_expense(expense_file_path, budget)
        elif choice == '5':
            # Exit the program
            break
        else:
            print("Invalid choice. Please select a valid option.")

def backup_file(file_path):
    if os.path.exists(file_path):
        shutil.copy(file_path, f"{file_path}.backup")

def print_menu():
    print("\nMenu:")
    print("1. Add Expense")
    print("2. Edit Expense")
    print("3. Delete Expense")
    print("4. Summarize Expenses")
    print("5. Exit")

def get_valid_budget():
    while True:
        try:
            budget = float(input("Enter your budget for the month: RM"))
            if budget > 0:
                return budget
            else:
                print("Budget must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def user_expense():
    print("Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = get_valid_expense_amount()
    expense_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"You have entered {expense_name} for RM{red(expense_amount)} on {expense_time}")

    expense_categories = ["Food", "Home", "School", "Study"]
    selected_category = get_valid_category(expense_categories)
    new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
    return new_expense, expense_time

def get_valid_expense_amount():
    while True:
        try:
            expense_amount = float(input("Enter expense amount: RM"))
            if expense_amount > 0:
                return expense_amount
            else:
                print("Expense amount must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_valid_category(expense_categories):
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")
        try:
            selected_index = int(input(f"Enter a category number [1 - {len(expense_categories)}]: ")) - 1
            if selected_index in range(len(expense_categories)):
                return expense_categories[selected_index]
            else:
                print(f"Invalid category. Please choose a number from [1 - {len(expense_categories)}]")
        except ValueError:
            print(f"Invalid input. Please enter a number from [1 - {len(expense_categories)}]")

def save_expense_to_file(expense: Expense, expense_time, expense_file_path):
    print(f"Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category},{expense_time}\n")

def edit_expense(expense_file_path):
    expenses = read_expenses_from_file(expense_file_path)
    if not expenses:
        print("No expenses to edit.")
        return

    for i, (expense, expense_time) in enumerate(expenses):
        print(f"{i + 1}. {expense_time} - {expense.name}: RM{red(f'{expense.amount:.2f}')}, Category: {expense.category}")
    
    try:
        index = int(input("Enter the number of the expense to edit: ")) - 1
        if 0 <= index < len(expenses):
            new_expense, new_expense_time = user_expense()
            expenses[index] = (new_expense, new_expense_time)
            write_expenses_to_file(expenses, expense_file_path)
            print("Expense updated successfully.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def delete_expense(expense_file_path):
    expenses = read_expenses_from_file(expense_file_path)
    if not expenses:
        print("No expenses to delete.")
        return

    for i, (expense, expense_time) in enumerate(expenses):
        print(f"{i + 1}. {expense_time} - {expense.name}: RM{red(f'{expense.amount:.2f}')}, Category: {expense.category}")
    
    try:
        index = int(input("Enter the number of the expense to delete: ")) - 1
        if 0 <= index < len(expenses):
            expenses.pop(index)
            write_expenses_to_file(expenses, expense_file_path)
            print("Expense deleted successfully.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def read_expenses_from_file(expense_file_path):
    expenses = []
    if os.path.exists(expense_file_path):
        with open(expense_file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                expense_name, expense_amount, expense_category, expense_time = line.strip().split(",")
                line_expense = Expense(
                    name=expense_name,
                    amount=float(expense_amount),
                    category=expense_category
                )
                expenses.append((line_expense, expense_time))
    return expenses

def write_expenses_to_file(expenses, expense_file_path):
    with open(expense_file_path, "w") as f:
        for expense, expense_time in expenses:
            f.write(f"{expense.name},{expense.amount},{expense.category},{expense_time}\n")

def summarize_expense(expense_file_path, budget):
    print("Summarizing Expenses")
    expenses = read_expenses_from_file(expense_file_path)

    if not expenses:
        print("No expenses to summarize.")
        return

    amount_by_category = {}
    for expense, _ in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    for key, amount in amount_by_category.items():
        print(f"  {key}: RM{red(f'{amount:.2f}')}")

    total_spent = sum([x.amount for x, _ in expenses])
    print(f"Total Spent: RM{red(f'{total_spent:.2f}')}")

    remaining_budget = budget - total_spent
    print(f"Budget Remaining: RM{blue(f'{remaining_budget:.2f}')}")

    # Get the current date
    now = datetime.datetime.now()

    # Get the numbers of days in the current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]

    # Calculate the remaining number of days in the current month
    remaining_days = days_in_month - now.day

    print(f"Remaining days in the current month: {remaining_days}")

    daily_budget = remaining_budget / remaining_days
    print(f"Budget Per Day: RM{blue(f'{daily_budget:.2f}')}")

    for expense, expense_time in expenses:
        print(f"{expense_time} - {expense.name}: RM{red(f'{expense.amount:.2f}')}, Category: {expense.category}")
        budget -= expense.amount
        print(f"Budget left after this expense: RM{blue(f'{budget:.2f}')}")

    # Check if spending exceeds the budget
    if total_spent > budget:
        print(red("Warning: You have exceeded your budget!"))

def red(text):
    return f"\033[91m{text}\033[0m"

def blue(text):
    return f"\033[94m{text}\033[0m"

if __name__ == "__main__":
    main()
