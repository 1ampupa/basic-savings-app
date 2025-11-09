from modules.account import Account
from modules.data_handler import DataHandler
from modules.ascii_decorator import AsciiDecorator as Text

class Executor():

    # Account

    @staticmethod
    def execute_account_list() -> tuple:
        if len(Account.accounts) == 0:
            return True, f"{Text.YELLOW}There's no account in the system.{Text.RESET}"
        else:
            print(f"{Text.CYAN}All account in the system.{Text.RESET}")
            print(f"{Text.CYAN}{'-'*50}{Text.RESET}")
            print(f"{Text.CYAN}{'Account Name':<25} {'Account Id':<15} {'Balance':<10} {Text.RESET}")
            for account in Account.accounts:
                if account == Account.current_account:
                    # Current Account
                    print(f"{Text.BLACK}{Text.BG_WHITE}{account.name:<25} {account.id:<15} {float(account.balance):<10}{Text.RESET}")
                else:
                    print(f"{account.name:<25} {account.id:<15} {float(account.balance):<10}")
            return True, f"{Text.GREEN}Now using: {Account.current_account}{Text.RESET}"

    @staticmethod
    def execute_account_login(arguments=[]) -> tuple:
        # Check arguments
        if len(Account.accounts) == 0:
            return False, f"{Text.YELLOW}There's no account in the system.{Text.RESET}"
        if len(arguments) < 1:
            return False, f"{Text.YELLOW}Required an account name or account id to login.{Text.RESET}"
        if arguments[0].strip() == "":
            return False, f"{Text.YELLOW}Missing an argument for the account name or id.{Text.RESET}"
        if Account.current_account:
            # Already logged into request account.
            if arguments[0] == Account.current_account.name or arguments[0] == Account.current_account.id:
                return True, f"{Text.GREEN}You're already using this account.{Text.RESET}"
        # Find account
        account = Account.find_account(arguments[0])
        # Change current account
        if account:
            Account.current_account = account
            return True, f"{Text.GREEN}Successfully logged into {Account.current_account}{Text.RESET}"
        return False, f"{Text.YELLOW}There's no account named or using id {arguments[0]}.{Text.RESET}"
    
    @staticmethod
    def execute_account_create(arguments=[]) -> tuple:
        # Check arguments
        if len(arguments) < 1:
            return False, f"{Text.YELLOW}Required at least an argument to use this command.{Text.RESET}"
        if arguments[0].strip() == "":
            return False, f"{Text.YELLOW}Missing an argument for the account name.{Text.RESET}"
        # Create account
        account = Account.create_account(arguments[0])
        try:
            if DataHandler.exists_in_list(arguments, 1):
                account.balance = float(arguments[1])
        except:
            account.balance = 0
        Account.current_account = account
        return True, f"{Text.GREEN}Successfully created and logged into account named {account.name} with the balance of {account.balance}.{Text.RESET}"
    
    @staticmethod
    def execute_account_balance() -> tuple:
        if Account.current_account == None:
            return False, "You're not using any account."
        return True, f"{Text.GREEN}{Account.current_account.name} has the balance of {Account.current_account.balance}{Text.RESET}"
    
    @staticmethod
    def execute_account_modify(arguments=[]) -> tuple:
        # Check arguments
        if Account.current_account == None:
            return False, f"{Text.YELLOW}You're not using any account.{Text.RESET}"
        if len(arguments) < 2:
            return False, f"{Text.YELLOW}Required attribute and value arguments to use this command.{Text.RESET}"
        if arguments[0].strip() == "":
            return False, f"{Text.YELLOW}Missing an argument for the attribute.{Text.RESET}"
        if arguments[1].strip() == "":
            return False, f"{Text.YELLOW}Missing an argument for the value.{Text.RESET}"
        # TODO Edit account
        return True, "EDIT"
    
    @staticmethod
    def execute_account_delete(arguments=[]) -> tuple:
        # Check arguments
        if Account.current_account == None:
            return False, f"{Text.YELLOW}You're not using any account.{Text.RESET}"
        if len(arguments) < 1:
            return False, f"{Text.YELLOW}Required an account argument to use this command.{Text.RESET}"
        if arguments[0].strip() == "":
            return False, f"{Text.YELLOW}Missing an argument for the account.{Text.RESET}"
        # TODO Comfirmation
        # TODO Delete account
        return True, "DELETE"
    
    # Transaction

    @staticmethod
    def execute_transaction_deposit(arguments=[]) -> tuple:
        if Account.current_account == None:
            return False, f"{Text.YELLOW}You're not using any account.{Text.RESET}"
        # Check arguments
        if len(arguments) < 1:
            return False, f"{Text.YELLOW}Required at least an argument to use this command.{Text.RESET}"
        if arguments[0].strip() == "":
            return False, f"{Text.YELLOW}Missing an argument for the amount.{Text.RESET}"
        # Deposit
        try:
            amount = float(arguments[0])
            _, log = Account.current_account.deposit(amount, True)
            return True, log
        except Exception as e:
            from modules.parser import Parser
            if Parser.debug_mode:
                return False, Parser.traceback_exception(e)
                
        return False, f"{Text.YELLOW}Something went wrong, please try again later.{Text.RESET}"
    
    @staticmethod
    def execute_transaction_withdraw(arguments=[]) -> tuple:
        if Account.current_account == None:
            return False, f"{Text.YELLOW}You're not using any account.{Text.RESET}"
        # Check arguments
        if len(arguments) < 1:
            return False, f"{Text.YELLOW}Required at least an argument to use this command.{Text.RESET}"
        if arguments[0].strip() == "":
            return False, f"{Text.YELLOW}Missing an argument for the amount.{Text.RESET}"
        # Withdraw
        try:
            amount = float(arguments[0])
            _, log = Account.current_account.withdraw(amount, True)
            return True, log
        except Exception as e:
            from modules.parser import Parser
            if Parser.debug_mode:
                return False, Parser.traceback_exception(e)
                
        return False, f"{Text.YELLOW}Something went wrong, please try again later.{Text.RESET}"
    
    @staticmethod
    def execute_transaction_transfer(arguments=[]) -> tuple:
        if Account.current_account == None:
            return False, f"{Text.YELLOW}You're not using any account.{Text.RESET}"
        # Check arguments
        if len(arguments) < 2:
            return False, f"{Text.YELLOW}Required target account and amount arguments to use this command.{Text.RESET}"
        if arguments[0].strip() == "":
            return False, f"{Text.YELLOW}Missing an argument for the target account.{Text.RESET}"
        if arguments[1].strip() == "":
            return False, f"{Text.YELLOW}Missing an argument for the amount.{Text.RESET}"
        # TODO Transfer
        try:
            target_account = Account.find_account(arguments[0])
            if target_account:
                amount = float(arguments[1])
                _, log = Account.current_account.transfer(target_account, amount)
                return True, log
            else:
                return False, f"{Text.YELLOW}Targeted account to transfer can't be found.{Text.RESET}"
        except Exception as e:
            from modules.parser import Parser
            if Parser.debug_mode:
                return False, Parser.traceback_exception(e)
                
        return False, f"{Text.YELLOW}Something went wrong, please try again later.{Text.RESET}"
    
    # Help Command
    @staticmethod
    def command_help():
        from modules.parser import Parser

        # Header
        print(f"{Text.YELLOW}If you're seeing 'Text.YELLOW' message at the start of the message, that means your terminal doesn't support colour.{Text.RESET}")
        print("In order to see ASCII terminal colour, in Windows type this in your CMD with administrator privilege.")
        print("reg add HKCU\\Console /v VirtualTerminalLevel /t REG_DWORD /d 1")
        
        print(f"{Text.UNDERLINE}{Text.CYAN}List of commands.{Text.RESET}")
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
