# constants.py


class Commands:
    ADD_COURSE_OFFERING = "ADD-COURSE-OFFERING"
    REGISTER = "REGISTER"
    ALLOT = "ALLOT"
    CANCEL = "CANCEL"
    


class Status:
    ACCEPTED = "ACCEPTED"
    COURSE_FULL_ERROR = "COURSE_FULL_ERROR"
    COURSE_CANCELED = "COURSE_CANCELED"
    CANCEL_REJECTED = "CANCEL_REJECTED"
    CANCEL_ACCEPTED = "CANCEL_ACCEPTED"
    INVALID_COMMAND = "Invalid command"
    FILE_PATH_NOT_ENTERED = "File path not entered"


class Config:
    pass


class Messages:
    INPUT_DATA_ERROR = "INPUT_DATA_ERROR"
