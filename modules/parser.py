import os
import platform
import shlex
from modules.commands import Commands

class Parser:
    
    prefix_aliases = {
        Commands.EXIT: ["EXIT", "QUIT", "END", "Q"],
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

    @classmethod
    def check_prefix_alias(cls, prefix: str) -> Commands:
        prefix = prefix.upper()
        for key, alias in cls.prefix_aliases.items():
            if prefix in alias:
                return key
        return Commands.NONE

    @staticmethod
    def check_sub_command(arguments: list[str]):
        if len(arguments) < 2: 
            return False, None, []
        sub_command = arguments[1].strip()
        if sub_command == "": 
            return False, None, []
        return True, arguments[1], arguments[2:]

    @classmethod
    def check_prefix(cls, command, checked_prefix, arguments) -> tuple:
        match (checked_prefix):
            case Commands.EXIT:
                return True, "EXITING..."
            case Commands.HELP:
                cls.command_help()
                return True, ""
            case Commands.CLEAR:
                if platform.system() == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")
                return True, "Cleared Terminal."
            case Commands.ACCOUNT:
                # Check sub command arguments
                parsable, sub_command, sub_command_arguments = cls.check_sub_command(arguments)
                if not parsable: return False, "Missing or empty subcommand for ACCOUNT command. Try using 'HELP' command"
                return True, "Account related commands"
            case Commands.TRANSACTION:
                parsable, sub_command, sub_command_arguments = cls.check_sub_command(arguments)
                if not parsable: return False, "Missing or empty subcommand for TRANSACTION command. Try using 'HELP' command"
                return True, "Transaction related commands"
        
        return False, f"Unknown command given: {command}. Try using 'HELP' command"

    @classmethod
    def parse(cls, command: str) -> tuple:
        # Check Empty
        if command.strip() == "": 
            return False, "Please enter a command, or typing help for list of commands."

        try:
            arguments: list[str] = shlex.split(command)
            prefix: str = arguments[0]

            checked_prefix: Commands = cls.check_prefix_alias(prefix)
            success, log = cls.check_prefix(command, checked_prefix, arguments)
            return success, log
        except ValueError as e:
            if str(e) == "No closing quotation":
                return False, f"Incomplete quotation mark. (Missing a closing mark.)"
            if str(e) == "No escaped character":
                return False, f"Invalid Escape sequence parsed."
            return False, f"A ValueError occurred while parsing: >_ {command}.\n{e}"
        except TypeError as e:
            return False, f"A TypeError occurred while parsing: >_ {command}.\n{e}"
        except Exception as e:
            return False, f"An unexpected error occurred while parsing: >_ {command}\n{e}"

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
