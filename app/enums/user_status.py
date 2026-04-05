from enum import Enum


class UserStatus(Enum):
    active = 'active'
    inactive = 'inactive'
    suspended = 'suspended'