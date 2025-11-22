import uuid
from datetime import datetime
from modules.data_handler import DataHandler
from modules.transaction_types import TransactionTypes
from modules.ascii_decorator import AsciiDecorator as Text

class Transaction():
    
    def __init__(self, account, transaction_type: TransactionTypes, amount: float,
                 transferer, receiver):
        from modules.account import Account

        self.id : str = str(uuid.uuid4())[:8]
        self.account : Account = account
        self.transaction_type: TransactionTypes = transaction_type
        self.amount: float = amount
        now = datetime.now()
        self.date: str = now.strftime("%d/%m/%Y")
        self.time: str = now.strftime("%H:%M:%S")
        self.transferer: Account = transferer
        self.receiver: Account = receiver

        # Create the transaction information
        DataHandler.write_transaction(self.account, self)

    def __str__(self) -> str:
        match self.transaction_type:
            case TransactionTypes.DEPOSIT:
                return f"{Text.GREEN}DEPOSITED {self.amount} to {self.account.name}, now {self.account.balance}.{Text.RESET}"
            case TransactionTypes.WITHDRAW:
                return f"{Text.GREEN}WITHDREW {self.amount} from {self.account.name}, now {self.account.balance}.{Text.RESET}"
            case TransactionTypes.TRANSFER:
                return f"{Text.GREEN}TRANSFERRED {self.amount} from {self.transferer.name} to {self.receiver.name}, now {self.account.balance}.{Text.RESET}"
            case TransactionTypes.RECEIVE:
                return f"{Text.GREEN}RECEIVED {self.amount} from {self.transferer.name}, now {self.account.balance}.{Text.RESET}"
            case _:
                return f"{Text.GREEN}A transaction log has created for {self.account.name}.{Text.RESET}"
            