from modules import transaction
from modules.account import Account
from modules.data_handler import DataHandler
from modules.ascii_decorator import AsciiDecorator as Text
from modules.commands import Commands

class Executor():

    # Account

    @staticmethod
    def execute_account_login(arguments) -> tuple:
        # Check arguments
        if len(arguments) < 1:
            return False, "Required at least an argument to use this command."
        # TODO Change current account
        print(Account.current_account)
        return True, "LOGIN"
    
    @staticmethod
    def execute_account_create(arguments) -> tuple:
        # Check arguments
        if len(arguments) < 1:
            return False, "Required at least an argument to use this command."
        if arguments[0].strip() == "":
            return False, "Missing an argument for the account name."
        # TODO Create account
        account = Account.create_account(arguments[0])
        try:
            if DataHandler.exists_in_list(arguments, 1):
                account.balance = float(arguments[1])
        except:
            return False, f"Account balance has to be a number. {account.name} now has the balance of 0."
        Account.current_account = account
        return True, f"Successfully created and logged into account named {account.name} with the balance of {account.balance}."
    
    @staticmethod
    def execute_account_balance() -> tuple:
        if Account.current_account == None:
            return False, "You're not using any account."
        return True, f"{Account.current_account.name} has the balance of {Account.current_account.balance}"
    
    @staticmethod
    def execute_account_modify(arguments) -> tuple:
        # Check arguments
        if Account.current_account == None:
            return False, "You're not using any account."
        if len(arguments) < 2:
            return False, "Required at least 2 arguments to use this command."
        # TODO Edit account
        return True, "EDIT"
    
    @staticmethod
    def execute_account_delete(arguments) -> tuple:
        # Check arguments
        if Account.current_account == None:
            return False, "You're not using any account."
        if len(arguments) < 1:
            return False, "Required at least an argument to use this command."
        # TODO Comfirmation
        # TODO Delete account
        return True, "DELETE"
    
    # Transaction

    @staticmethod
    def execute_transaction_deposit(arguments) -> tuple:
        if Account.current_account == None:
            return False, "You're not using any account."
        # Check arguments
        if len(arguments) < 1:
            return False, "Required at least an argument to use this command."
        # TODO Deposit
        return True, "DEPOSIT"
    
    @staticmethod
    def execute_transaction_withdraw(arguments) -> tuple:
        if Account.current_account == None:
            return False, "You're not using any account."
        # Check arguments
        if len(arguments) < 1:
            return False, "Required at least an argument to use this command."
        # TODO Withdraw
        return True, "WITHDRAW"
    
    @staticmethod
    def execute_transaction_transfer(arguments) -> tuple:
        if Account.current_account == None:
            return False, "You're not using any account."
        # Check arguments
        if len(arguments) < 1:
            return False, "Required at least an argument to use this command."
        # TODO Transfer
        return True, "TRANSFER"
    
    # Help Command
    @staticmethod
    def command_help():
        from modules.parser import Parser
        # Type this into your Windows CMD if the colour isn't present
        # reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1

        # Header
        print(f"{Text.CYAN}{'PREFIX':<20} {'ALIASES':<30} {'DESCRIPTION':<40}{Text.RESET}")
        print(f"{Text.CYAN}{'-'*100}{Text.RESET}")

        # Description
        prefix_descriptions = {
            "DEBUG": "Toggle debug mode for developer.",
            "HELP": "Show help message.",
            "CLEAR": "Clear the terminal.",
            "VERSION": "Show the program version",
            "EXIT": "Exit the program.",
            "ACCOUNT": "Account related commands.",
            "TRANSACTION": "Transaction related commands.", 
            "SOB": ":("
        }

        account_sub_command_description = {
            "ACC_LOGIN": "Log into an account.",
            "ACC_CREATE": "Create an new account",
            "ACC_BALANCE": "Query an existing account balance.",
            "ACC_MODIFY": "Modify an existing account data.",
            "ACC_DELETE": "Delete an existing account."
        }

        account_sub_command_syntax = {
            "ACC_LOGIN": "acc log [Account Name]",
            "ACC_CREATE": "acc new [Account Name] [<Starting Balance>]",
            "ACC_BALANCE": "acc balance",
            "ACC_MODIFY": "acc edit [Account Name] [Attribute] [Value]",
            "ACC_DELETE": "acc del [Account Name]",}

        transaction_sub_command_description = {
            "T_DEPOSIT": "Deposit money into an existing account.",
            "T_WITHDRAW": "Withdraw money from an existing account.",
            "T_TRANSFER": "Transfer money from A to B account."
        }

        transaction_sub_command_syntax = {
            "T_DEPOSIT": "t + [Amount]",
            "T_WITHDRAW": "t - [Amount]",
            "T_TRANSFER": "t > [Target Account] [Amount]"
        }

        # Prefix
        for prefix, aliases in Parser.prefix_aliases.items():
            alias_string = ", ".join(aliases)
            description = prefix_descriptions.get(prefix.name, "")
            print(f"{Text.GREEN}{prefix.name:<20}{Text.RESET} {alias_string:<30} {description:<40}")

        # Account Subcommand
        print(f"{Text.RED}\nAccount Subcommand")
        print(f"{Text.RED}{'TYPE':<20} {'ALIASES':<30} {'DESCRIPTION':<40} {'SYNTAX':<40} {Text.RESET}")
        print(f"{Text.RED}{'-'*140}{Text.RESET}")
        for sub_command, aliases in Parser.account_sub_command_aliases.items():
            alias_string = ", ".join(aliases)
            description = account_sub_command_description.get(sub_command.name, "")
            syntax = account_sub_command_syntax.get(sub_command.name, "")
            print(f"{Text.GREEN}{sub_command.name:<20}{Text.RESET} {alias_string:<30} {description:<40} {syntax:<20}")

        # Transaction Subcommand
        print(f"{Text.RED}\nTransaction Subcommand")
        print(f"{Text.RED}{'TYPE':<20} {'ALIASES':<30} {'DESCRIPTION':<40} {'SYNTAX':<40} {Text.RESET}")
        print(f"{Text.RED}{'-'*140}{Text.RESET}")
        for sub_command, aliases in Parser.transaction_sub_command_aliases.items():
            alias_string = ", ".join(aliases)
            description = transaction_sub_command_description.get(sub_command.name, "")
            syntax = transaction_sub_command_syntax.get(sub_command.name, "")
            print(f"{Text.GREEN}{sub_command.name:<20}{Text.RESET} {alias_string:<30} {description:<40} {syntax:<20}")

        print(f"{Text.RESET}")
