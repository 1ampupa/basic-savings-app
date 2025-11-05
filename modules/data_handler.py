from pathlib import Path
import json

class DataHandler:
    data_folder_path: Path = Path("data")
    accounts_json_file: Path = data_folder_path / "accounts.json"

    # Helper function for writing JSON file
    @staticmethod
    def write_json(path: Path, data: dict|list) -> None:
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

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

    @classmethod
    def create_account_folder(cls, account_id: str) -> Path:
        folder = cls.data_folder_path / account_id
        folder.mkdir(exist_ok=True)
        return folder

    @classmethod
    def create_account_profile(cls, account_folder: Path, account_id: str, 
                               name: str, balance: float, folder_path: Path,
                               transaction_folder_path: Path) -> Path:
        path = account_folder / "profile.json"
        cls.write_json(path, {
            "id": account_id, 
            "name": name, 
            "balance": balance,
            "folder-path": str(folder_path),
            "profile-path": str(path),
            "transactions-folder-path": str(transaction_folder_path)
            })
        return path

    @staticmethod
    def update_account_profile(account) -> None:
        path = account.profile_path
        data = {"id": account.id, "name": account.name, "balance": account.balance}
        DataHandler.write_json(path, data)

    @staticmethod
    def create_transactions_folder(account_folder: Path) -> Path:
        folder = account_folder / "transactions"
        folder.mkdir(exist_ok=True)
        return folder

    @staticmethod
    def write_transaction(account, transaction) -> None:
        path = account.transaction_folder_path / f"{transaction.id}.json"
        data = {
            "id": transaction.id,
            "account": account.name,
            "account-id": account.id,
            "type": str(transaction.transaction_type),
            "amount": transaction.amount,
            "new-balance": account.balance
        }
        DataHandler.write_json(path, data)
