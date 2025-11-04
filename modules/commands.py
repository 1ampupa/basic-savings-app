from enum import Enum, auto

class Commands(Enum):
    # Command prefixes
    NONE = 0
    EXIT = auto()
    HELP = auto()
    CLEAR = auto()
    ACCOUNT = auto()
    TRANSACTION = auto()

    # Accounts Sub command
    ACC_LOGIN = auto()
    ACC_CREATE = auto()
    ACC_BALANCE = auto()
    ACC_EDIT = auto()
    ACC_DELETE = auto()

    # Transaction Sub command
    T_DEPOSIT = auto()
    T_WITHDRAW = auto()
    T_TRANSFER = auto()

