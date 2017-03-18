import json, sys, click, time
from datetime import datetime

class MoneyManager:
    def __init__(self, filename):
        defaults = {
            "account_remaining": 3600,
            "balance": 0,
            "last_time": time.time()
        }
        data = {}

        # HACK: nested with - try - except
        try:
            with open(filename, "r") as f:
                try:
                    data = json.load(f)
                except BaseException:
                    print("Can't read data, overwriting with defaults")
        except FileNotFoundError as ex:
            print(ex)

        self.data = {**defaults, **data}
        self.filename = filename
        self.enddate = datetime(2018, 5, 19)

    def getdata(self):
        return self.data

    def writedata(self, data):
        with open(self.filename, "w") as f:
            json.dump(self.data, f)


@click.group()
def cli():
    pass


@cli.command()
def show():
    moneymanager = MoneyManager("data.json")
    data = moneymanager.getdata()
    now = datetime.fromtimestamp(time.time())
    last_time = datetime.fromtimestamp(data['last_time'])
    days_since_last_time = (now - last_time).days

    data['balance'] += days_since_last_time * (data['account_remaining'] / (moneymanager.enddate - last_time).days)
    data['last_time'] = now.timestamp()

    print(data)
    moneymanager.writedata(data)


@cli.command()
@click.argument('amount', default=0)
def update_account(amount):
    moneymanager = MoneyManager("data.json")
    data = moneymanager.getdata()

    data['balance'] -= data['account_remaining'] - amount
    data['account_remaining'] = amount

    print(data)
    moneymanager.writedata(data)