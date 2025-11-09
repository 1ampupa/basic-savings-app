import uuid
from modules.data_handler import DataHandler
from modules.transaction_types import TransactionTypes

class Transaction():
    
    def __init__(self, account, transaction_type: TransactionTypes, amount: float,
                 transferer, receiver):
        from modules.account import Account

        self.id : str = str(uuid.uuid4())[:8]
        self.account : Account = account
        self.transaction_type: TransactionTypes = transaction_type
        self.amount: float = amount
        self.transferer: Account = transferer
        self.receiver: Account = receiver

        # Create the transaction information
        
        DataHandler.write_transaction(self.account, self)

    def __str__(self) -> str:
        if self.transaction_type == TransactionTypes.DEPOSIT:
            return f"Transaction: DEPOSITED {self.amount} to {self.account.name}, now {self.account.balance}."
        elif self.transaction_type == TransactionTypes.WITHDRAW:
            return f"Transaction: WITHDREW {self.amount} from {self.account.name}, now {self.account.balance}."
        elif self.transaction_type == TransactionTypes.TRANSFER:
            return f"Transaction: TRANSFER {self.amount} from {self.transferer.name} to {self.receiver.name}, now {self.account.balance}."
        elif self.transaction_type == TransactionTypes.RECEIVE:
            return f"Transaction: RECEIVE {self.amount} from {self.transferer.name}, now {self.account.balance}."
        else:
            return f"Transaction: {self.transaction_type} {self.amount} -> {self.account.name}"
    
