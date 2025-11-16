from modules.ascii_decorator import AsciiDecorator as Text
from pathlib import Path
import json, csv

class DataHandler:
    data_folder_path: Path = Path("data")
    accounts_json_file: Path = data_folder_path / "accounts.json"
    transaction_csv_header: list = ["id", "account_name", "account_id", "type", "amount", 
                                    "account_new_balance", "transferer", "receiver"]

    # Helper function to check index exist in list
    @staticmethod
    def exists_in_list(target_list: list, index: int) -> bool:
        return index < len(target_list)

    # Helper function for writing JSON file
    @staticmethod
    def write_json(path: Path, data: dict|list) -> None:
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

    # Helper function for appending CSV file
    @classmethod
    def append_csv(cls, path: Path, data: dict) -> None:
        with open(path, "a", newline="") as file:
            if not Path(path).exists() or Path(path).stat().st_size == 0:
                from modules.account import Account
                if Account.current_account:
                    cls.create_transaction_history_file(Account.current_account.folder_path)
            writer = csv.DictWriter(file, fieldnames=cls.transaction_csv_header)
            writer.writerow(data)

    # Helper function for reading JSON file
    @staticmethod
    def read_json(path):
        with open(path, "r") as file:
            data = json.load(file)
            return data

    # Create Data Folder
    @classmethod
    def ensure_data_folder(cls) -> Path:
        cls.data_folder_path.mkdir(exist_ok=True)
        return cls.data_folder_path

    # Create Accounts list file
    @classmethod
    def ensure_accounts_list(cls) -> Path:
        if not cls.accounts_json_file.exists():
            cls.write_json(cls.accounts_json_file, {
                "accounts": {},
                "account_id_counter": 1
            })
        return cls.accounts_json_file

    # Update Accounts list file
    @classmethod
    def update_accounts_list(cls, data: dict) -> None:
        path: Path = cls.accounts_json_file
        cls.write_json(path, data)

    # Get Accounts list from file
    @classmethod
    def get_accounts_list(cls):
        path: Path = cls.accounts_json_file
        data = cls.read_json(path)
        return data

    # Create an account folder
    @classmethod
    def create_account_folder(cls, account_id: str) -> Path:
        folder = cls.data_folder_path / account_id
        folder.mkdir(exist_ok=True)
        return folder

    # Create an account profile JSON file
    @classmethod
    def create_account_profile(cls, account_folder: Path, account_id: str, 
                               name: str, balance: float, folder_path: Path,
                               transaction_history_file: Path) -> Path:
        path = account_folder / "profile.json"
        cls.write_json(path, {
            "id": account_id, 
            "name": name, 
            "balance": balance,
            "folder_path": str(folder_path),
            "profile_path": str(path),
            "transaction_history_file": str(transaction_history_file)
            })
        return path

    # Update an account profile JSON file
    @staticmethod
    def update_account_profile(account) -> None:
        path = account.profile_path
        DataHandler.write_json(path, {
            "id": account.id,
            "name": account.name,
            "balance": account.balance,
            "folder_path": str(account.folder_path),
            "profile_path": str(account.profile_path),
            "transaction_history_file": str(account.transaction_history_file)
        })

    # Create a transaction history file inside an account folder
    @classmethod
    def create_transaction_history_file(cls, account_folder: Path) -> Path:
        path = account_folder / "transaction_history.csv"
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            # Write Header
            writer.writerow(cls.transaction_csv_header)
        return path

    # Write transaction log into the transaction folder inside the account folder.
    @staticmethod
    def write_transaction(account, transaction) -> None:
        try:
            path: Path = account.transaction_history_file
            data = {                                            # Original variables data type
                "id": str(transaction.id),                      # str
                "account_name": str(account.name),                   # Account
                "account_id": str(account.id),                  # str
                "type": str(transaction.transaction_type),      # enum TRANSACTION_TYPE
                "amount": str(transaction.amount),              # float
                "account_new_balance": str(account.balance),            # float
                "transferer": str(transaction.transferer.name), # str
                "receiver": str(transaction.receiver.name)      # str
            }
            DataHandler.append_csv(path, data)
        except Exception as e:
            from modules.parser import Parser
            if Parser.debug_mode:
                print(Parser.traceback_exception(e))
            else:
                print(f"{Text.RED}Something went wrong while writing a transaction.{Text.RESET}")
