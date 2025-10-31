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
        Commands.ACC_LOGIN: [],
        Commands.ACC_CREATE: [],
        Commands.ACC_GET: [],
        Commands.ACC_EDIT: [],
        Commands.ACC_DELETE: [],

        # TRANSACTION
        Commands.T_DEPOSIT: [],
        Commands.T_WITHDRAW: [],
        Commands.T_TRANSFER: []
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
    def parse(cls, command: str) -> tuple:
        # Check Empty
        if command.strip() == "": 
            return False, "Please enter a command, or typing help for list of commands."

        try:
            arguments: list[str] = shlex.split(command)
            prefix: str = arguments[0]

            checked_prefix: Commands = cls.check_prefix_alias(prefix)

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
                    print(sub_command, sub_command_arguments)
                    return True, "Account related commands"
                case Commands.TRANSACTION:
                    parsable, sub_command, sub_command_arguments = cls.check_sub_command(arguments)
                    if not parsable: return False, "Missing or empty subcommand for TRANSACTION command. Try using 'HELP' command"
                    print(sub_command, sub_command_arguments)
                    return True, "Transaction related commands"
        except ValueError as e:
            if str(e) == "No closing quotation":
                return False, f"Incomplete quotation mark. (Missing a closing mark.)"
            return False, f"A ValueError occurred while parsing: >_ {command}.\n{e}"
        except TypeError as e:
            return False, f"A TypeError occurred while parsing: >_ {command}.\n{e}"
        except Exception as e:
            return False, f"An unexpected error occurred while parsing: >_ {command}\n{e}"
        
        return False, f"Unknown command given: {command}. Try using 'HELP' command"

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
