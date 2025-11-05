import os
import platform
import shlex
from modules.commands import Commands

class Parser:
    
    prefix_aliases = {
        Commands.EXIT: ["EXIT", "QUIT", "STOP", "END", "Q"],
        Commands.HELP: ["HELP", "?"],
        Commands.CLEAR: ["CLS", "CLEAR"],
        Commands.ACCOUNT: ["ACCOUNT", "ACC", "A"],
        Commands.TRANSACTION: ["TRANSACTION", "TRANS", "T"]
    }

    sub_command_aliases = {
        # ACCOUNT
        Commands.ACC_LOGIN: ["login", "session", "use"],
        Commands.ACC_CREATE: ["create", "new", "add", "open"],
        Commands.ACC_BALANCE: ["balance", "b", "money", "get"],
        Commands.ACC_EDIT: ["edit", "modify"],
        Commands.ACC_DELETE: ["delete", "del", "remove", "close"],

        # TRANSACTION
        Commands.T_DEPOSIT: ["deposit", "add", "+"],
        Commands.T_WITHDRAW: ["withdraw", "remove", "-"],
        Commands.T_TRANSFER: ["transfer", "move", ">"]
    }

    command: str = ""
    prefix: str | Commands = Commands.NONE
    sub_command: str = ""
    arguments : list[str] = []

    # Aliases checker

    @classmethod
    def check_prefix_aliases(cls, prefix: str) -> Commands:
        prefix = prefix.upper()
        for key, alias in cls.prefix_aliases.items():
            if prefix in alias:
                return key
        return Commands.NONE

    @classmethod
    def check_sub_command_aliases(cls, sub_command: str) -> Commands:
        sub_command = sub_command.lower()
        for key, alias in cls.sub_command_aliases.items():
            if sub_command in alias:
                return key
        return Commands.NONE

    # Check Prefix

    @classmethod
    def parse_prefix(cls):
        match (cls.prefix):
            case Commands.EXIT:
                return False, "Stopping..."
            case Commands.HELP:
                cls.command_help()
                return False, "Displayed available commands."
            case Commands.CLEAR:
                if platform.system() == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")
                return False, "Cleared Terminal."
            case Commands.ACCOUNT:
                return True, "Parsing Account-related command."    
            case Commands.TRANSACTION:
                return True, "Parsing Transaction-related command."    

        return False, f"Unknown command given: {cls.command}. Try using 'HELP' command"

    # Check sub command

    @classmethod
    def parse_sub_command(cls):
        # Check command arguments length
        if len(cls.arguments) < 3:
            return False, f"This command prefix required a subcommand and at least an argument. Try using 'HELP' command"
        
        # Check empty subcommand
        sub_command = cls.arguments[1].strip()
        if sub_command == "": 
            return False, f"Missing or empty subcommand. Try using 'HELP' command"
        
        # Get aliases
        sub_command = cls.check_sub_command_aliases(cls.sub_command)

        return sub_command
    
    # Executor

    @classmethod
    def execute(cls, sub_command):
        match (sub_command):
            # Account
            case Commands.ACC_LOGIN:
                success, log = cls.execute_account_login()
                return success, log
            case Commands.ACC_CREATE:
                success, log = cls.execute_account_login()
                return success, log
            case Commands.ACC_BALANCE:
                success, log = cls.execute_account_login()
                return success, log
            case Commands.ACC_EDIT:
                success, log = cls.execute_account_login()
                return success, log
            case Commands.ACC_DELETE:
                success, log = cls.execute_account_login()
                return success, log
                
            # Transaction
            case Commands.T_DEPOSIT:
                success, log = cls.execute_account_login()
                return success, log
            case Commands.T_WITHDRAW:
                success, log = cls.execute_account_login()
                return success, log
            case Commands.T_TRANSFER:
                success, log = cls.execute_account_login()
                return success, log

        return False, f"Unknown command given: {cls.command}. Try using 'HELP' command"

    # ACC_LOGIN
    @staticmethod
    def execute_account_login() -> tuple: return ()

    # ACC_CREATE
    @staticmethod
    def execute_account_create() -> tuple: return ()

    # ACC_BALANCE
    @staticmethod
    def execute_account_balance() -> tuple: return ()

    # ACC_EDIT
    @staticmethod
    def execute_account_edit() -> tuple: return ()

    # ACC_DELETE
    @staticmethod
    def execute_account_delete() -> tuple: return ()

    # T_DEPOSIT
    @staticmethod
    def execute_transaction_deposit() -> tuple: return ()

    # T_WITHDRAW
    @staticmethod
    def execute_transaction_withdraw() -> tuple: return ()

    # T_TRANSFER
    @staticmethod
    def execute_transaction_transfer() -> tuple: return ()

    # Parser

    @classmethod
    def parse(cls, command: str) -> tuple:
        cls.command = command
        # Check Empty
        if command.strip() == "": 
            return False, "Please enter a command, or typing help for list of commands."

        try:
            # Get Arguments list
            cls.arguments = shlex.split(command)

            # Get Prefix
            cls.prefix = cls.arguments[0]

            # Check Prefix
            cls.prefix = cls.check_prefix_aliases(cls.prefix)
            single_command, log = cls.parse_prefix()
            
            # Check Sub command
            if single_command:
                sub_command = cls.parse_sub_command()
                success, log = cls.execute(sub_command)
            else:
                success = True

            return success, log
        except ValueError as e:
            return False, f"A ValueError occurred while parsing: >_ {command}.\n{e}"
        except TypeError as e:
            return False, f"A TypeError occurred while parsing: >_ {command}.\n{e}"
        except Exception as e:
            return False, f"An unexpected error occurred while parsing: >_ {command}\n{e}"

    # Help command

    @staticmethod
    def command_help():
        # Type this into your Windows CMD if the colour isn't present
        # reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1

        RED = "\033[91m"
        GREEN = "\033[92m"
        CYAN = "\033[96m"
        RESET = "\033[0m"

        # Header
        print(f"{CYAN}{'PREFIX':<20} {'ALIASES':<30} {'DESCRIPTION':<50}{RESET}")
        print(f"{CYAN}{'-'*100}{RESET}")

        # Description
        descriptions = {
            "HELP": "Show help message.",
            "ACCOUNT": "Account related commands.",
            "TRANSACTION": "Transaction related commands.",
            "CLEAR": "Clear the terminal.",
            "EXIT": "Exit the program."
        }

        for prefix, aliases in Parser.prefix_aliases.items():
            alias_string = ", ".join(aliases)
            description = descriptions.get(prefix.name, "")
            print(f"{GREEN}{prefix.name:<20}{RESET} {alias_string:<30} {description:<50}")
