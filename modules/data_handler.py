from pathlib import Path
import json

class DataHandler:
    folder_path: Path = Path("data")

    @classmethod
    def ensure_data_folder(cls) -> Path:
        cls.folder_path.mkdir(exist_ok=True)
        return cls.folder_path

    @classmethod
    def create_account_folder(cls, account_id: str) -> Path:
        folder = cls.folder_path / account_id
        folder.mkdir(exist_ok=True)
        return folder

    @staticmethod
    def write_json(path: Path, data: dict) -> None:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def create_account_profile(cls, account_folder: Path, account_id: str, name: str, balance: float) -> Path:
        path = account_folder / "profile.json"
        cls.write_json(path, {"id": account_id, "name": name, "balance": balance})
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
