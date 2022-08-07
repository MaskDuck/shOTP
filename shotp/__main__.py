from __future__ import annotations
from typing import TYPE_CHECKING
import pyotp


from typer import Typer

if TYPE_CHECKING:
    from shotp.typehint import Account, Config
    from typing import Optional, Literal

from dotenv import load_dotenv
load_dotenv()



from os import getenv

try:
    import orjson as json
    orjson_installed: bool = True
except ImportError:
    import json
    orjson_installed: bool = False

app = Typer()

config_dir: str = getenv("SHOTP_CONFIG_FILE_DIRECTORY", default='./shotp_config.json')


try:
    with open(config_dir, mode="r") as f:
        config: Config = json.loads(f.read())
except FileNotFoundError: 
    f = open("./shotp_config.json", mode='x')
    open("./shotp_config.json", "w").write('{"accounts": []}')
    config: Config = {"accounts": []}
    print(f"No config file found, created a default config file.")

def _get_account(name: str) -> Optional[Account]:
    for x in config['accounts']:
        if x['name'] == name:
            return x
    return None

            

def _add_account(code: str, name: str) -> None:
    config['accounts'].append({
        "code": code,
        "name": name
    })

    with open(config_dir, "w") as f:
        f.write(json.dumps(config).decode("utf-8"))

@app.command()
def new(code: str, name: str) -> None:
    if _get_account(name) is None:
        _add_account(code=code, name=name)
    else:
        print("An account with the same name already exists.")


@app.command()
def code(name: str) -> None:
    account: Account = _get_account(name)
    if account is not None:
        generator: pyotp.TOTP = pyotp.TOTP(account['code'])
        print(generator.now())
    else:
        print("Seems like there is no account with that name exists.")

@app.command()
def accounts(name: str) -> None:
    for x in config['accounts']:
        print(x['name'])

@app.command()
def delete(name: str) -> None:
    account = _get_account(name)
    if account is not None: 
        

        confirm: Optional[Literal["y", "N"]] = input("Do you really want to delete account named {}? This action is not reversible! [y/N]:".format(account.name))
        if confirm.lower() == "n":
            print("Aborted.")
            return
        else:

            config['accounts'].remove(account)

            with open(config_dir, "w") as f:
                f.write(json.dumps(config).decode("utf-8"))
    else:
        print("No account with the name {} has been found.".format(name))
        
    
if __name__ == "__main__":
    app()

