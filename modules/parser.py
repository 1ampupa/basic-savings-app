import os, platform, shlex, traceback
from modules.account import Account
from modules.commands import Commands

class Parser:
    
    prefix_aliases = {
        Commands.DEBUG: ["DEBUG", "DEV", "TEST"],
        Commands.EXIT: ["EXIT", "QUIT", "STOP", "END", "Q"],
        Commands.HELP: ["HELP", "?"],
        Commands.CLEAR: ["CLS", "CLEAR"],
        Commands.ACCOUNT: ["ACCOUNT", "ACC", "A"],
        Commands.TRANSACTION: ["TRANSACTION", "TRANS", "T"]
    }

    account_sub_command_aliases = {
        Commands.ACC_LOGIN: ["login", "session", "use"],
        Commands.ACC_CREATE: ["create", "new", "add", "open"],
        Commands.ACC_BALANCE: ["balance", "b", "money", "get"],
        Commands.ACC_EDIT: ["edit", "modify"],
        Commands.ACC_DELETE: ["delete", "del", "remove", "close"],

        
    }

    transaction_sub_command_aliases = {
        Commands.T_DEPOSIT: ["deposit", "add", "+"],
        Commands.T_WITHDRAW: ["withdraw", "remove", "-"],
        Commands.T_TRANSFER: ["transfer", "move", ">"]
    }

    command: str = ""
    prefix: str | Commands = Commands.NONE
    sub_command: str = ""
    arguments : list[str] = []
    
    # Debug mode
    debug_mode = False

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
        # Account
        for key, alias in cls.account_sub_command_aliases.items():
            if sub_command in alias:
                return key
        # Transaction
        for key, alias in cls.transaction_sub_command_aliases.items():
            if sub_command in alias:
                return key
        return Commands.NONE

    # Check Prefix

    @classmethod
    def parse_prefix(cls) -> tuple:
        match (cls.prefix):
            case Commands.DEBUG:
                cls.debug_mode = not cls.debug_mode
                return False, f"Toggled Debug mode to {cls.debug_mode}"
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
    def parse_sub_command(cls) -> tuple:
        # Check command arguments length
        if len(cls.arguments) < 3:
            return Commands.NONE, f"This command prefix required a subcommand and at least an argument. Try using 'HELP' command"
        
        # Check empty subcommand
        sub_command = cls.arguments[1].strip()
        cls.sub_command = sub_command
        if sub_command == "": 
            return Commands.NONE, f"Missing or empty subcommand. Try using 'HELP' command"
        
        # Get aliases
        sub_command = cls.check_sub_command_aliases(cls.sub_command)

        return sub_command, "Parsed subcommand sucessfully"
    
    # Executor

    @classmethod
    def execute(cls, sub_command) -> tuple:
        match (sub_command):
            # Account
            case Commands.ACC_LOGIN:
                success, log = cls.execute_account_login()
                return success, log
            case Commands.ACC_CREATE:
                success, log = cls.execute_account_create()
                return success, log
            case Commands.ACC_BALANCE:
                success, log = cls.execute_account_balance()
                return success, log
            case Commands.ACC_EDIT:
                success, log = cls.execute_account_edit()
                return success, log
            case Commands.ACC_DELETE:
                success, log = cls.execute_account_delete()
                return success, log
                
            # Transaction
            case Commands.T_DEPOSIT:
                success, log = cls.execute_transaction_deposit()
                return success, log
            case Commands.T_WITHDRAW:
                success, log = cls.execute_transaction_withdraw()
                return success, log
            case Commands.T_TRANSFER:
                success, log = cls.execute_transaction_transfer()
                return success, log

        return False, f"Unknown command given: {cls.command}. Try using 'HELP' command"

    # ACC_LOGIN
    @classmethod
    def execute_account_login(cls) -> tuple:
        # TODO Change account
        print(Account.current_account)
        return True, "LOGIN"

    # ACC_CREATE
    @classmethod
    def execute_account_create(cls) -> tuple:
        # TODO Create account
        return True, "CREATE"

    # ACC_BALANCE
    @classmethod
    def execute_account_balance(cls) -> tuple:
        if Account.current_account == None:
            return False, "You're not using any account."
        return True, f"{Account.current_account.name} has the balance of {Account.current_account.balance}"

    # ACC_EDIT
    @classmethod
    def execute_account_edit(cls) -> tuple:
        if Account.current_account == None:
            return False, "You're not using any account."
        # TODO Edit account
        return True, "EDIT"

    # ACC_DELETE
    @classmethod
    def execute_account_delete(cls) -> tuple:
        if Account.current_account == None:
            return False, "You're not using any account."
        # TODO Comfirmation
        # TODO Delete account
        return True, "DELETE"

    # T_DEPOSIT
    @classmethod
    def execute_transaction_deposit(cls) -> tuple:
        if Account.current_account == None:
            return False, "You're not using any account."
        # TODO Deposit
        return True, "DEPOSIT"

    # T_WITHDRAW
    @classmethod
    def execute_transaction_withdraw(cls) -> tuple:
        if Account.current_account == None:
            return False, "You're not using any account."
        # TODO Withdraw
        return True, "WITHDRAW"

    # T_TRANSFER
    @classmethod
    def execute_transaction_transfer(cls) -> tuple:
        if Account.current_account == None:
            return False, "You're not using any account."
        # TODO Transfer
        return True, "TRANSFER"

    # Traceback
    @staticmethod
    def traceback_exception(exception: Exception) -> str:
        return "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))

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
            chain_command, log = cls.parse_prefix()
            
            # Check Sub command
            if chain_command:
                sub_command, log = cls.parse_sub_command()
                if sub_command == Commands.NONE:
                    return False, log
                success, log = cls.execute(sub_command)
            else:
                success = True

            return success, log
        except Exception as e:
            if cls.debug_mode:
                return False, cls.traceback_exception(e)
            else:
                return False, f"An error occurred while parsing {command}."

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
            "DEBUG": "Toggle debug mode for developer.",
            "HELP": "Show help message.",
            "ACCOUNT": "Account related commands.",
            "TRANSACTION": "Transaction related commands.",
            "CLEAR": "Clear the terminal.",
            "EXIT": "Exit the program."
        }

        # Prefix
        for prefix, aliases in Parser.prefix_aliases.items():
            alias_string = ", ".join(aliases)
            description = descriptions.get(prefix.name, "")
            print(f"{GREEN}{prefix.name:<20}{RESET} {alias_string:<30} {description:<50}")

        # Account Subcommand
        print(f"{RED}\nAccount Subcommand")
        print(f"{RED}{'TYPE':<20} {'ALIASES':<30} {'DESCRIPTION':<50}{RESET}")
        print(f"{RED}{'-'*100}{RESET}")
        for sub_command, aliases in Parser.account_sub_command_aliases.items():
            alias_string = ", ".join(aliases)
            #description = descriptions.get(prefix.name, "")
            print(f"{GREEN}{sub_command.name:<20}{RESET} {alias_string:<30}")

        # Transaction Subcommand
        print(f"{RED}\nTransaction Subcommand")
        print(f"{RED}{'TYPE':<20} {'ALIASES':<30} {'DESCRIPTION':<50}{RESET}")
        print(f"{RED}{'-'*100}{RESET}")
        for sub_command, aliases in Parser.transaction_sub_command_aliases.items():
            alias_string = ", ".join(aliases)
            #description = descriptions.get(prefix.name, "")
            print(f"{GREEN}{sub_command.name:<20}{RESET} {alias_string:<30}")
        print(f"{RESET}")
