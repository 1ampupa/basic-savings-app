import os, platform, shlex, traceback
from modules.commands import Commands
from modules.executor import Executor
from modules.ascii_decorator import AsciiDecorator as Text

class Parser:
    
    program_version = "Test Version 1"

    prefix_aliases = {
        Commands.DEBUG: ["DEBUG", "DEV", "TEST"],
        Commands.HELP: ["HELP", "?"],
        Commands.CLEAR: ["CLS", "CLEAR"],
        Commands.VERSION: ["VER", "VERSION", "ABOUT", "PATCH"],
        Commands.EXIT: ["EXIT", "QUIT", "STOP", "END", "Q"],
        
        Commands.ACCOUNT: ["ACCOUNT", "ACC", "A"],
        Commands.TRANSACTION: ["TRANSACTION", "TRANS", "T"],

        Commands.SOB: ["SOB", ":(", "D:", "cry"]
    }

    account_sub_command_aliases = {
        Commands.ACC_LOGIN: ["login", "log", "session", "use", "in"],
        Commands.ACC_CREATE: ["create", "new", "add", "open"],
        Commands.ACC_BALANCE: ["balance", "b", "money", "get"],
        Commands.ACC_MODIFY: ["edit", "modify", "change"],
        Commands.ACC_DELETE: ["delete", "del", "remove", "close"],
    }

    transaction_sub_command_aliases = {
        Commands.T_DEPOSIT: ["deposit", "add", "+"],
        Commands.T_WITHDRAW: ["withdraw", "remove", "-"],
        Commands.T_TRANSFER: ["transfer", "move", ">"]
    }

    executor_map = {
        # ACCOUNT
        Commands.ACC_LOGIN: Executor.execute_account_login,
        Commands.ACC_CREATE: Executor.execute_account_create,
        Commands.ACC_BALANCE: Executor.execute_account_balance,
        Commands.ACC_MODIFY: Executor.execute_account_modify,
        Commands.ACC_DELETE: Executor.execute_account_delete,

        # TRANSACTION
        Commands.T_DEPOSIT: Executor.execute_transaction_deposit,
        Commands.T_WITHDRAW: Executor.execute_transaction_withdraw,
        Commands.T_TRANSFER: Executor.execute_transaction_transfer
    }

    executor_function_required_arguments = {
        # ACCOUNT
        Commands.ACC_LOGIN: Executor.execute_account_login,
        Commands.ACC_CREATE: Executor.execute_account_create,
        Commands.ACC_MODIFY: Executor.execute_account_modify,
        Commands.ACC_DELETE: Executor.execute_account_delete,

        # TRANSACTION
        Commands.T_DEPOSIT: Executor.execute_transaction_deposit,
        Commands.T_WITHDRAW: Executor.execute_transaction_withdraw,
        Commands.T_TRANSFER: Executor.execute_transaction_transfer
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
    def check_sub_command_aliases(cls) -> tuple:
        sub_command = cls.sub_command.lower()
        # Account
        for key, alias in cls.account_sub_command_aliases.items():
            if sub_command in alias:
                return key, "Account Subcommand."
        # Transaction
        for key, alias in cls.transaction_sub_command_aliases.items():
            if sub_command in alias:
                return key, "Transaction Subcommand."
        return Commands.NONE, f"{Text.YELLOW}Unknown Subcommand. Try using 'HELP' command.{Text.RESET}"

    # Check Prefix

    @classmethod
    def parse_prefix(cls) -> tuple:
        match (cls.prefix):
            case Commands.DEBUG:
                cls.debug_mode = not cls.debug_mode
                return False, f"Toggled Debug mode to {cls.debug_mode}"
            case Commands.EXIT:
                return False, f"Stopping..."
            case Commands.HELP:
                cls.command_help()
                return False, "Displayed available commands. Learn more at https://github.com/1ampupa/basic-savings-app"
            case Commands.CLEAR:
                if platform.system() == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")
                return False, f"{Text.BG_GREEN}{Text.WHITE}Welcome to Basic Savings App Version {Parser.program_version}.{Text.RESET}\nType help for list of commands."
            case Commands.VERSION:
                return False, f"Basic Savings App Version {cls.program_version}"
            case Commands.ACCOUNT:
                return True, "Parsing Account-related command."    
            case Commands.TRANSACTION:
                return True, "Parsing Transaction-related command."    
            case Commands.SOB:
                return False, "it's okay."

        return False, f"{Text.YELLOW}Unknown command prefix given. Try using 'HELP' command.{Text.RESET}"

    # Check sub command

    @classmethod
    def parse_sub_command(cls) -> tuple:
        # Check command arguments length
        if len(cls.arguments) < 2:
            return Commands.NONE, f"{Text.YELLOW}This command prefix required a subcommand. Try using 'HELP' command.{Text.RESET}"
        
        # Check empty subcommand
        sub_command = cls.arguments[1].strip()
        cls.sub_command = sub_command
        if sub_command == "": 
            return Commands.NONE, f"{Text.YELLOW}Missing or empty subcommand. Try using 'HELP' command.{Text.RESET}"
        
        # Get aliases
        sub_command, log = cls.check_sub_command_aliases()
        return sub_command, log
    
    # Executor

    @classmethod
    def execute(cls, sub_command: Commands) -> tuple:
        execute_function = cls.executor_map.get(sub_command)
        if execute_function:
            arguments = cls.arguments[2:] if sub_command in cls.executor_function_required_arguments else []
            try:
                success, log = execute_function(arguments) if arguments else execute_function()
                return success, log
            except Exception as e:
                if cls.debug_mode:
                    return False, cls.traceback_exception(e)
        
        return False, f"{Text.RED}Something went wrong, please try again later.{Text.RESET}"
        

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
            return False, f"{Text.YELLOW}Please enter a command, or typing help for list of commands.{Text.RESET}"

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
                    return False, log or f"{Text.YELLOW}Unknown command given: {cls.command}. Try using 'HELP' command.{Text.RESET}"
                success, log = cls.execute(sub_command)
            else:
                success = True

            return success, log
        except Exception as e:
            if cls.debug_mode:
                return False, cls.traceback_exception(e)
            else:
                return False, f"{Text.RED}An error occurred while parsing {command}.{Text.RESET}"
        finally:
            # Reset
            cls.command = ""
            cls.prefix = Commands.NONE
            cls.sub_command = ""
            cls.arguments = []
            

    # Help command

    @staticmethod
    def command_help():
        Executor.command_help()
