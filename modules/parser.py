import os, platform, shlex, traceback
from types import FunctionType
from modules.commands import Commands
from modules.executor import Executor
from modules.ascii_decorator import AsciiDecorator as Text

class Parser:

    command: str = ""
    prefix: str | Commands = Commands.NONE
    sub_command: str = ""
    arguments : list[str] = []
    
    program_version = "Release Version 1"

    # Debug mode
    debug_mode = False


    prefix_aliases = {
        Commands.DEBUG: ["DEBUG", "DEV", "TEST"],
        Commands.HELP: ["HELP", "?"],
        Commands.CLEAR: ["CLS", "CLEAR"],
        Commands.VERSION: ["VER", "VERSION", "ABOUT", "PATCH"],
        Commands.EXIT: ["EXIT", "QUIT", "STOP", "END", "Q"],
        
        Commands.ACCOUNT: ["ACCOUNT", "ACC", "A"],
        Commands.TRANSACTION: ["TRANSACTION", "TRAN", "T"],

        Commands.SOB: ["SOB", ":(", "D:", "cry"]
    }

    sub_command_aliases = {
        # ACCOUNT
        Commands.ACC_LIST: ["list", "query", "all", "*"],
        Commands.ACC_LOGIN: ["login", "log", "session", "use", "in"],
        Commands.ACC_CREATE: ["create", "new", "add", "open"],
        Commands.ACC_BALANCE: ["balance", "b", "money", "get"],
        Commands.ACC_MODIFY: ["edit", "modify", "change"],
        Commands.ACC_DELETE: ["delete", "del", "remove", "close"],

        # TRANSACTION

        Commands.T_DEPOSIT: ["deposit", "add", "+"],
        Commands.T_WITHDRAW: ["withdraw", "remove", "-"],
        Commands.T_TRANSFER: ["transfer", "move", ">"],
        Commands.T_QUERY: ["get", "query"],
        Commands.T_CLEAR: ["clear", "cls"]
    }


    executor_map: dict[Commands, tuple[FunctionType, bool]] = { # Commands: [method, require_arguments]
        # ACCOUNT
        Commands.ACC_LIST: (Executor.execute_account_list, False),
        Commands.ACC_LOGIN: (Executor.execute_account_login, True),
        Commands.ACC_CREATE: (Executor.execute_account_create, True),
        Commands.ACC_BALANCE: (Executor.execute_account_balance, False),
        Commands.ACC_MODIFY: (Executor.execute_account_modify, True),
        Commands.ACC_DELETE: (Executor.execute_account_delete, True),

        # TRANSACTION
        Commands.T_DEPOSIT: (Executor.execute_transaction_deposit, True),
        Commands.T_WITHDRAW: (Executor.execute_transaction_withdraw, True),
        Commands.T_TRANSFER: (Executor.execute_transaction_transfer, True),
        Commands.T_QUERY: (Executor.execute_transaction_query, True),
        Commands.T_CLEAR: (Executor.execute_transaction_clear, True)
    }

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
        for key, alias in cls.sub_command_aliases.items():
            if sub_command in alias:
                return key, "Valid Subcommand."
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
        try:
            execute_function = cls.executor_map.get(sub_command)
            if not execute_function: return False, "Unknown subcommand. Try using 'HELP' command."
            command, require_arguments = execute_function
            arguments = cls.arguments[2:] if require_arguments else []
            if require_arguments:
                return command(arguments)
            else:
                return command()
        except Exception as e:
            if cls.debug_mode:
                return False, cls.traceback_exception(e)
            
        return False, f"{Text.BG_RED}{Text.WHITE}Something went wrong, please try again later.{Text.RESET}"
                

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
    def command_help(): Executor.command_help()
