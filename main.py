from modules.account import Account
from modules.parser import Parser

Account.load_accounts()

print("Welcome to Basic Savings App on Python. Type help for list of commands.")

while True:
    user_command = input(">_ ")
    success, log = Parser.parse(user_command)
    print(log)
    if success and log.startswith("EXITING"):
        break
