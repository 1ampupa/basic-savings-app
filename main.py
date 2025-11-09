from modules.account import Account
from modules.parser import Parser
from modules.ascii_decorator import AsciiDecorator as Text

loaded_accounts = Account.load_accounts()

print(f"{Text.BG_GREEN}{Text.WHITE}Welcome to Basic Savings App Version {Parser.program_version}.{Text.RESET}\nType help for list of commands.")

if len(Account.accounts) == 0:
    print(f"{Text.YELLOW}Warning: There's no account in system.{Text.RESET}\nPlease create one using 'acc new [name] [<balance>]'")
elif len(Account.accounts) >= 1:
    Account.current_account = Account.accounts[0]
    print(f"Loaded {len(Account.accounts)} account(s).")
    print(f"Current Account: {Account.current_account.name}")

while True:
    user_command = input(">_ ")
    success, log = Parser.parse(user_command)
    print(log)
    if success and log.startswith("Stopping"):
        break
