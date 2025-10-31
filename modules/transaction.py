import uuid
from modules.data_handler import DataHandler
from modules.transaction_types import TransactionTypes

class Transaction():
    
    def __init__(self, account, transaction_type: TransactionTypes, amount: float):
        from modules.account import Account

        self.id : str = str(uuid.uuid4())
        self.account : Account = account
        self.transaction_type = transaction_type
        self.amount = amount

        # Create the transaction information
        
        DataHandler.write_transaction(self.account, self)

    def __str__(self) -> str:
        if self.transaction_type == TransactionTypes.DEPOSIT:
            return f"Transaction: DEPOSITED {self.amount} to {self.account.name}, now {self.account.balance}."
        elif self.transaction_type == TransactionTypes.WITHDRAW:
            return f"Transaction: WITHDREW {self.amount} from {self.account.name}, now {self.account.balance}."
        else:
            return f"Transaction: {self.transaction_type} {self.amount} -> {self.account.name}"
    
