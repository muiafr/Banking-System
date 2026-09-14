from banking.db import ensure_tables
from banking.profile.user_inf import user_info
from banking.profile.user_transactions.transaction_menu import transaction_menu
from banking.profile.user_transactions.deposit import deposit

from fastapi import FastAPI

from banking.routes import users
from banking.routes import transactions
from banking.routes import deposits

app = FastAPI()

app.include_router(users.router)
#app.include_router(transactions.router)
#app.include_router(deposits.router)


def main():
    ensure_tables()
    while True:
        print("Welcome to Banking")
        print("What do you want to do: ")
        print("1. User Info")
        print("2. User Transactions")
        print("3. User Deposits")
        print("4. Exit")
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                user_info()
            case "2":
                transaction_menu()
            case "3":
                deposit()
            case "4":
                print("Thank you for your time")
                break
            case _:
                print("Invalid choice")






if __name__ == "__main__":
    main()

