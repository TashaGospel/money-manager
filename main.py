import json, click, time, os
from datetime import date

datafile = "data.json"

defaults = {
    "account_remaining": 3600,
    "balance": 0,
    "last_time": date(2017, 3, 19)
}

end_date = date(2018, 5, 19)


class MoneyManager:
    def __init__(self, filename):
        data = {}

        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    data = json.load(f)
                except BaseException:
                    print("Can't read data, overwriting with defaults")

        self._data = {**defaults, **data}
        self._file_name = filename

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self._file_name, "w") as f:
            json.dump(self._data, f)

    def report(self):
        return {
            "account_remaining": self._data['account_remaining'],
            "balance": self._data['balance']
        }

    def update_balance(self):
        now_timestamp = time.time()
        now = date.fromtimestamp(now_timestamp)
        last_time = date.fromtimestamp(self._data['last_time'])
        print(last_time)
        days_since_last_time = (now - last_time).days
        self._data['balance'] += days_since_last_time * (self._data['account_remaining'] / (end_date - last_time).days)
        self._data['last_time'] = now_timestamp

    def update_account(self, new_account_remaining):
        self._data['balance'] -= self._data['account_remaining'] - new_account_remaining
        self._data['account_remaining'] = new_account_remaining


@click.group()
def cli():
    pass


@cli.command()
def report():
    with MoneyManager(datafile) as money_manager:
        money_manager.update_balance()
        print(money_manager.report())


@cli.command()
@click.argument('amount', default=0)
def update_account(amount):
    with MoneyManager(datafile) as money_manager:
        money_manager.update_account(amount)
        print(money_manager.report())