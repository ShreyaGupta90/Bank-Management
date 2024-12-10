import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("bank_management.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM accounts")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='accounts'")
conn.commit()
conn.close()

conn = sqlite3.connect("bank_management.db")
cursor = conn.cursor()

# Creating tables if not already present
def create_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        account_type TEXT NOT NULL,
        balance REAL NOT NULL
    )''')
    conn.commit()

# Function to create a new account
def create_account(name, age, account_type, initial_balance):
    cursor.execute("INSERT INTO accounts (name, age, account_type, balance) VALUES (?, ?, ?, ?)",
                   (name, age, account_type, initial_balance))
    conn.commit()
    print("Account created successfully!")

# Function to view account details
def view_account(account_id):
    cursor.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,))
    account = cursor.fetchone()
    if account:
        print("Account Details:")
        print(f"ID: {account[0]}, Name: {account[1]}, Age: {account[2]}, Type: {account[3]}, Balance: {account[4]}")
    else:
        print("Account not found.")

# Function to deposit money into an account
def deposit(account_id, amount):
    cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,))
    account = cursor.fetchone()
    if account:
        new_balance = account[0] + amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", (new_balance, account_id))
        conn.commit()
        print("Deposit successful!")
    else:
        print("Account not found.")

# Function to withdraw money from an account
def withdraw(account_id, amount):
    cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,))
    account = cursor.fetchone()
    if account:
        if account[0] >= amount:
            new_balance = account[0] - amount
            cursor.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", (new_balance, account_id))
            conn.commit()
            print("Withdrawal successful!")
        else:
            print("Insufficient balance.")
    else:
        print("Account not found.")

# Function to check balance
def check_balance(account_id):
    cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,))
    account = cursor.fetchone()
    if account:
        print(f"Current Balance: {account[0]}")
    else:
        print("Account not found.")

# Function to delete an account
def delete_account(account_id):
    cursor.execute("DELETE FROM accounts WHERE account_id = ?", (account_id,))
    conn.commit()
    print("Account deleted successfully!")

# Main program
def main():
    create_table()
    while True:
        print("\n=== Bank Management System ===")
        print("1. Create Account")
        print("2. View Account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Check Balance")
        print("6. Delete Account")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            account_type = input("Enter account type (Savings/Current): ")
            initial_balance = float(input("Enter initial deposit amount: "))
            create_account(name, age, account_type, initial_balance)
            
        elif choice == "2":
            account_id = int(input("Enter account ID: "))
            view_account(account_id)
            
        elif choice == "3":
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter amount to deposit: "))
            deposit(account_id, amount)
            
        elif choice == "4":
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter amount to withdraw: "))
            withdraw(account_id, amount)
            
        elif choice == "5":
            account_id = int(input("Enter account ID: "))
            check_balance(account_id)
            
        elif choice == "6":
            account_id = int(input("Enter account ID: "))
            delete_account(account_id)
            
        elif choice == "7":
            print("Thank you for using the Bank Management System!")
            break
            
        else:
            print("Invalid choice. Please try again.")

# main function
main()
conn.close()