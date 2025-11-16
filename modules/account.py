from pathlib import Path    
from typing import Optional

from modules.transaction import Transaction
from modules.data_handler import DataHandler
from modules.transaction_types import TransactionTypes
from modules.ascii_decorator import AsciiDecorator as Text

class Account():

    # Path Variables
    _data_folder_path: Path = DataHandler.ensure_data_folder()
    _accounts_file_path: Path = DataHandler.ensure_accounts_list()

    # Account Variables
    accounts : list[Account] = []
    current_account: Account | None = None
    _accounts_path : dict = {}
    _account_id_counter : int = 1

    # Initialise an account.
    def __init__(self, id : str, name: str, balance: float, folder_path: Path, profile_path: Path, transaction_history_file: Path) -> None:
        
        # Assign values
        self.id: str = id
        self.name: str = name
        self.balance: float = balance
        self.folder_path: Path = folder_path
        self.profile_path: Path = profile_path
        self.transaction_history_file: Path = transaction_history_file

        # Increase the counter
        Account._account_id_counter += 1

        # Append account to the accounts list
        Account.accounts.append(self)
        Account._accounts_path[self.id] = str(self.profile_path)

        # Update the accounts.json
        accounts_json_data = {
            "accounts": {k: str(v) for k, v in Account._accounts_path.items()},
            "account_id_counter": Account._account_id_counter
        }
        DataHandler.update_accounts_list(accounts_json_data)

    @classmethod # Alternative Constructor
    def create_account(cls, name: Optional[str], balance: float = 0) -> Account:
        
        # Assign account profile
        id: str = f"account{Account._account_id_counter}"
        name = name or f"Account {Account._account_id_counter}"
        balance = balance or 0

        # Create an account folder
        folder_path = DataHandler.ensure_account_folder(id)
        
        # Create a transaction history file
        transaction_history_file = DataHandler.ensure_transaction_history_file(folder_path)
        
        # Create a profile.json file
        profile_path = DataHandler.ensure_account_profile(id, name, balance, folder_path, Path(folder_path / "profile.json"), transaction_history_file)

        return cls(id, name, balance, folder_path, profile_path, transaction_history_file)
    
    @classmethod
    def load_accounts(cls) -> Account | None:
        cls.accounts.clear()
        accounts: dict = DataHandler.get_accounts_list()

        if not accounts.get("accounts"): 
            return None

        for _, profile_path in accounts["accounts"].items():
            account_data = DataHandler.read_json(profile_path)
            try:
                cls(
                account_data["id"],
                account_data["name"],
                account_data["balance"],
                account_data["folder_path"],
                account_data["profile_path"],
                account_data["transaction_history_file"]
            )
            except Exception as e:
                from modules.parser import Parser
                if Parser.debug_mode:
                    print(Parser.traceback_exception(e))
                else:
                    print(f"{Text.BG_RED}{Text.WHITE}Something went wrong while loading an account, please make sure that the account directory isn't corrupted.{Text.RESET}")
                break
        return None

    @classmethod
    def find_account(cls, account_name_or_id: str) -> Account | None:
        for account in Account.accounts:
            if account_name_or_id == account.name or account_name_or_id == account.id:
                return account
        return None

    # Transaction Handling
    def deposit(self, amount: float, loggable: bool) ->  tuple:
        
        # Condition Checking
        if amount <= 0:
            return False, f"{Text.YELLOW}Cannot deposit amount below or equal 0.{Text.RESET}"

        self.balance += amount

        # Create Transaction log
        if loggable:
            log = Transaction(self, TransactionTypes.DEPOSIT, amount, self, self)
        else:
            log = f"Deposited {amount} to {self}, now {self.balance}."

        # Update Profile Json file
        DataHandler.update_account_profile(self)
        
        return True, str(log)

    def withdraw(self, amount: float, loggable: bool) -> tuple:
       
        # Condition Checking
        if amount <= 0:
            return False, f"{Text.YELLOW}Cannot withdraw amount below or equal 0.{Text.RESET}"
        if self.balance < amount:
            return False, f"{Text.YELLOW}Insufficient fund in your account (Only: {self.balance}){Text.RESET}"
        
        self.balance -= amount

        # Create Transaction log
        if loggable:
            log = Transaction(self, TransactionTypes.WITHDRAW, amount, self, self)
        else:
            log = f"Withdrew {amount} to {self}, now {self.balance}."

        # Update Profile Json file
        DataHandler.update_account_profile(self)
    
        return True, str(log)

    def transfer(self, target_account: Account, amount: float) -> tuple:
        # Condition Checking
        if not target_account:
            return False, f"{Text.YELLOW}Target account not found in the system.{Text.RESET}"
        if amount <= 0:
            return False, f"{Text.YELLOW}Cannot transfer amount below or equal 0.{Text.RESET}"
        if self.balance < amount:
            return False, f"{Text.YELLOW}Insufficient fund in your account (Only: {self.balance}){Text.RESET}"
        
        self.withdraw(amount, False)
        target_account.deposit(amount, False)

        # Create Transaction log
        log_transfer = Transaction(self, TransactionTypes.TRANSFER, amount, self, target_account)
        log_receive = Transaction(target_account, TransactionTypes.RECEIVE, amount, self, target_account)

        # Update Profile Json file
        DataHandler.update_account_profile(self)
        DataHandler.update_account_profile(target_account)
        
        return True, str(log_transfer)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    def __repr__(self) -> str:
        return f"{self.name} ({self.id})\nBALANCE: {self.balance}.\nFolder: {self.folder_path}\nProfile JSON file: {self.profile_path}\nTransaction folder: {self.transaction_history_file}"
    