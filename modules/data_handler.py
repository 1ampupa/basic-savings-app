from pathlib import Path
import json

#TODO Create a data folder

class DataHandler():

    folder_path : Path

    @staticmethod
    def create_data_folder() -> Path:
        DataHandler.folder_path = Path("data")
        DataHandler.folder_path.mkdir(exist_ok=True)
        return DataHandler.folder_path
    
    @staticmethod
    def create_account_folder(account_id: str) -> Path:
        account_folder : Path = Path(f"{DataHandler.folder_path}/{account_id}")
        account_folder.mkdir(exist_ok=True)
        return account_folder

    @staticmethod
    def create_account_profile_JSON(account_folder: Path, account_id: str, 
                                    account_name: str, account_balance: float) -> Path:
        account_path: Path = account_folder / "profile.json"
        account_data: dict = {
            "id": account_id,
            "name": account_name,
            "balance": account_balance
        }
        with open(account_path, "w") as file:
            json.dump(account_data.copy(), file,indent=4)
        return account_path
    
    @staticmethod
    def create_account_transactions_folder(account_folder: Path) -> Path:
        account_transactions_folder: Path = Path(f"{account_folder}/transactions")
        account_transactions_folder.mkdir(exist_ok=True)
        return account_transactions_folder
