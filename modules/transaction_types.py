from enum import Enum, auto

class TransactionTypes(Enum):
    DEPOSIT = auto()
    WITHDRAW = auto()
    TRANSFER = auto()
    RECEIVE = auto()
    