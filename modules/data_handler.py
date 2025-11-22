from modules.ascii_decorator import AsciiDecorator as Text
from pathlib import Path
import json, csv

class DataHandler:
    data_folder_path: Path = Path("data")
    accounts_json_file: Path = data_folder_path / "accounts.json"
    transaction_csv_header: list = ["id", "account_name", "account_id", "type", "amount", 
                                    "account_new_balance", "date", "time", "transferer", "receiver"]

    # Helper function to check index exist in list
    @staticmethod
    def exists_in_list(target_list: list, index: int) -> bool:
        return index < len(target_list)

    # Helper function for writing a JSON file
    @staticmethod
    def write_json(path: Path, data: dict|list) -> None:
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

    # Helper function for appending CSV file
    @classmethod
    def append_csv(cls, folder_path: Path, data: dict) -> None:
        folder_path = cls.ensure_transaction_history_file(folder_path)
        with open(folder_path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=cls.transaction_csv_header)
            writer.writerow(data)

    # Helper function for reading a JSON file
    @classmethod
    def read_file(cls, path, file_type: str):
        with open(path, "r", newline='', encoding="utf-8") as file:
            if file_type.upper() == "JSON":
                json_data: dict = json.load(file)
                return json_data
            elif file_type.upper() == "CSV":
                reader = csv.DictReader(file)
                csv_data: list = []
                for row in reader:
                    row_data = {}
                    for header in cls.transaction_csv_header:
                        row_data[header] = row[header]
                    csv_data.append(row_data)
                return csv_data
            return {}

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

    # Create a transaction history file inside an account folder
    @classmethod
    def ensure_transaction_history_file(cls, account_folder: Path) -> Path:
        path = Path(account_folder) / "transaction_history.csv"
        if not Path(path).exists() or Path(path).stat().st_size == 0:
            with open(path, "w", newline="") as file:
                writer = csv.writer(file)
                # Write Header
                writer.writerow(cls.transaction_csv_header)
        return path

    # Update Accounts list file
    @classmethod
    def update_accounts_list(cls, data: dict) -> None:
        path: Path = cls.accounts_json_file
        cls.write_json(path, data)

    # Get Accounts list from file
    @classmethod
    def get_accounts_list(cls):
        path: Path = cls.accounts_json_file
        data = cls.read_file(path, "JSON")
        return data

    # Create an account folder
    @classmethod
    def ensure_account_folder(cls, account_id: str) -> Path:
        folder = cls.data_folder_path / account_id
        folder.mkdir(exist_ok=True)
        return folder

    # Account profile writer
    @classmethod
    def write_account_profile(cls, account_id: str, name: str, balance: float, 
                               folder_path: Path, profile_path, 
                               transaction_history_file: Path, 
                               ) -> Path:
        cls.write_json(Path(profile_path), {
            "id": account_id, 
            "name": name, 
            "balance": balance,
            "folder_path": str(folder_path),
            "profile_path": str(profile_path),
            "transaction_history_file": str(transaction_history_file)
            })
        return Path(profile_path)

    # Create an account profile JSON file
    @classmethod
    def ensure_account_profile(cls, account_id: str, account_name: str, balance: float, 
                               folder_path: Path, profile_path: Path,
                               transaction_history_file: Path, ) -> Path:
        path: Path = cls.write_account_profile(
            account_id,
            account_name,
            balance,
            folder_path,
            profile_path,
            transaction_history_file
            )
        return path

    # Update an account profile JSON file
    @classmethod
    def update_account_profile(cls, account) -> None:
        DataHandler.write_account_profile(
            account.id,
            account.name,
            account.balance,
            account.folder_path,
            account.profile_path,
            account.transaction_history_file
        )

    # Write transaction log into the transaction folder inside the account folder.
    @staticmethod
    def write_transaction(account, transaction) -> None:
        try:
            data = {                                            # Original variables data type
                "id": str(transaction.id),                      # str
                "account_name": str(account.name),              # Account
                "account_id": str(account.id),                  # str
                "type": str(transaction.transaction_type),      # enum TRANSACTION_TYPE
                "amount": str(transaction.amount),              # float
                "account_new_balance": str(account.balance),    # float
                "date": str(transaction.date),                  # str
                "time": str(transaction.time),                  # str
                "transferer": str(transaction.transferer.name), # str
                "receiver": str(transaction.receiver.name)      # str
            }
            DataHandler.append_csv(account.folder_path, data)
        except Exception as e:
            from modules.parser import Parser
            if Parser.debug_mode:
                print(Parser.traceback_exception(e))
            else:
                print(f"{Text.RED}Something went wrong while writing a transaction.{Text.RESET}")
