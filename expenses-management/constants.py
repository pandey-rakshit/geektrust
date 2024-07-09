# constants.py


class Commands:
    MOVE_IN = "MOVE_IN"
    SPEND = "SPEND"
    DUES = "DUES"
    CLEAR_DUE = "CLEAR_DUE"
    MOVE_OUT = "MOVE_OUT"


class Status:
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"
    HOUSEFUL = "HOUSEFUL"
    MEMBER_NOT_FOUND = "MEMBER_NOT_FOUND"
    INCORRECT_PAYMENT = "INCORRECT_PAYMENT"
    INVALID_COMMAND = "Invalid command"
    FILE_PATH_NOT_ENTERED = "File path not entered"


class Config:
    MAX_MEMBERS = 3


class Messages:
    USAGE = "Usage: python main.py <file_path>"
