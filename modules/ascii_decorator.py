from enum import Enum

class AsciiDecorator(Enum):
    RESET = "\033[0m"

    # Colours
    BLACK   = "\033[90m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

    # Styling
    BOLD      = "\033[1m"
    ITALIC    = "\033[3m"
    UNDERLINE = "\033[4m"

    # Background Colours
    BG_BLACK   = "\033[40m"
    BG_RED     = "\033[41m"
    BG_GREEN   = "\033[42m"
    BG_YELLOW  = "\033[43m"
    BG_BLUE    = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN    = "\033[46m"
    BG_WHITE   = "\033[47m"

    def __str__(self) -> str:
        return self.value
