from modules.account import Account
from modules.parser import Parser

loaded_accounts = Account.load_accounts()

print("Welcome to Basic Savings App on Python. Type help for list of commands.")

if len(Account.accounts) == 0:
    print("There's no account in system, please create one using 'ACCOUNT create [name] [<balance>]'")
elif len(Account.accounts) >= 1:
    Account.current_account = Account.accounts[0]
    print(f"Loaded {len(Account.accounts)} account(s).")
    print(f"Current Account: {Account.current_account}")

while True:
    user_command = input(">_ ")
    success, log = Parser.parse(user_command)
    print(log)
    if success and log.startswith("Stopping"):
        break
