import json
from pathlib import Path
from typing import Optional

from modules.data_handler import DataHandler

class Account():

    # Account Variables
    accounts : list[Account] = []
    _account_id_counter : int = 1

    # Path Variables
    _data_folder_path: Path = DataHandler.create_data_folder()

    # Initialise an account.
    def __init__(self, id : str, name: str, balance: float, folder_path: Path, profile_path: Path, transactions_folder_path: Path) -> None:
        # Assign values
        self.id = id
        self.name = name
        self.balance = balance
        self.folder_path = folder_path
        self.profile_path = profile_path
        self.transaction_folder_path = transactions_folder_path

        Account.accounts.append(self)

    @classmethod # Alternative Constructor
    def create_account(cls, name: Optional[str], balance: Optional[float]) -> Account:
        
        # Assign account profile
        id: str = f"account{Account._account_id_counter}"
        name = name or f"Account {Account._account_id_counter}"
        balance = balance or 0

        # Create an account folder and profile JSON file
        folder_path = DataHandler.create_account_folder(id)
        profile_path = DataHandler.create_account_profile_JSON(folder_path,id, name, balance)
        
        # Create a transactions folder
        transactions_folder_path = DataHandler.create_account_transactions_folder(folder_path)

        return cls(id, name, balance, folder_path, profile_path, transactions_folder_path)
    
    # Balance Handling
    def deposit(self, amount: float) -> None:
        self.balance += amount
        print(f"Deposited {amount} to {self.name}, now {self.balance}.")

    def withdraw(self, amount: float) -> bool:
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdrew {amount} from {self.name}, now {self.balance}.")
            return True
        else:
            print(f"{self.name} has insufficient funds. ({self.balance})") 
            return False

    def __str__(self) -> str:
        return f"{self.name} has balance of {self.balance}."
    
    def __repr__(self) -> str:
        return f"{self.name} ({self.id})\nBALANCE: {self.balance}.\nFolder: {self.folder_path}\nProfile JSON file: {self.profile_path}\nTransaction folder: {self.transaction_folder_path}"
