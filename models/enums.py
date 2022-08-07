from enum import Enum


class UserRole(Enum):
    simple_user = "User"
    manager = "Manager"


class ThreadState(Enum):
    open = "Open"
    closed = "Closed"