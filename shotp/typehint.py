from typing import TypedDict, final, type_check_only, List

@type_check_only
@final
class Account(TypedDict):
    name: str
    code: str

@type_check_only
@final
class Config(TypedDict):
    accounts: List[Account]