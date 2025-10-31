import json

from pathlib import Path    
from typing import Optional

from modules.transaction import Transaction
from modules.data_handler import DataHandler
from modules.transaction_types import TransactionTypes

class Account():

    # Account Variables
    accounts : list[Account] = []
    _account_id_counter : int = 1

    # Path Variables
    _data_folder_path: Path = DataHandler.ensure_data_folder()

    # Initialise an account.
    def __init__(self, id : str, name: str, balance: float, folder_path: Path, profile_path: Path, transactions_folder_path: Path) -> None:
        
        # Assign values
        self.id = id
        self.name = name
        self.balance = balance
        self.folder_path = folder_path
        self.profile_path = profile_path
        self.transaction_folder_path = transactions_folder_path

        # Append account to the accounts list
        Account.accounts.append(self)

    @classmethod # Alternative Constructor
    def create_account(cls, name: Optional[str], balance: float = 0) -> Account:
        
        # Assign account profile
        id: str = f"account{Account._account_id_counter}"
        name = name or f"Account {Account._account_id_counter}"
        balance = balance or 0

        # Create an account folder and profile JSON file
        folder_path = DataHandler.create_account_folder(id)
        profile_path = DataHandler.create_account_profile(folder_path, id, name, balance)
        
        # Create a transactions folder
        transactions_folder_path = DataHandler.create_transactions_folder(folder_path)

        # Increase the counter
        Account._account_id_counter += 1
        
        return cls(id, name, balance, folder_path, profile_path, transactions_folder_path)
    
    # Transaction Handling
    def deposit(self, amount: float) ->  tuple:
        
        # Condition Checking
        if amount <= 0:
            return False, "Cannot deposit amount below or equal 0."

        self.balance += amount

        # Create Transaction log
        log = Transaction(self, TransactionTypes.DEPOSIT, amount)

        # Update Profile Json file
        DataHandler.update_account_profile(self)
        
        return True, str(log)

    def withdraw(self, amount: float) -> tuple:
       
        # Condition Checking
        if amount <= 0:
            return False, "Cannot withdraw amount below or equal 0."
        if self.balance < amount:
            return False, f"Insufficient fund in {self.name} ({self.balance})"
        
        self.balance -= amount

        # Create Transaction log
        log = Transaction(self, TransactionTypes.WITHDRAW, amount)

        # Update Profile Json file
        DataHandler.update_account_profile(self)

        return True, str(log)

    def __str__(self) -> str:
        return f"{self.name} has balance of {self.balance}."
    
    def __repr__(self) -> str:
        return f"{self.name} ({self.id})\nBALANCE: {self.balance}.\nFolder: {self.folder_path}\nProfile JSON file: {self.profile_path}\nTransaction folder: {self.transaction_folder_path}"
