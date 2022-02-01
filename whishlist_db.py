from tinydb import TinyDB, Query
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich.text import Text

console = Console()
db = TinyDB('db.json')
User = Query()


class WishListDB:
    def __init__(self, name: str, balance: int):
        console.clear()
        if db.contains(User.username == name):
            self.name = db.get(User.username == f'{name}')['username']
            self.balance = db.get(User.username == f'{name}')['balance']
            self.product_dict = db.get(User.username == f'{name}')['product_dict']
        else:
            self.name = name
            self.balance = balance
            self.product_dict = {}  # value as a key, price and nec as a value [price, nec]
            self.res = {"username": self.name, "balance": self.balance, "product_dict": self.product_dict}
            db.insert(self.res)

    def build_table(self) -> Table:
        console.clear()
        table = Table(show_header=True, show_footer=True)
        total_value = sum([item[0] for item in self.product_dict.values()])
        table.title = f'{self.name}\'s Wish List🌟'
        table.add_column(header='Item', justify='left', style='cyan', footer=f'{len(self.product_dict)}',
                         no_wrap=True)
        table.add_column(header='Necessity (1~3)', justify='center', style='magenta')
        table.add_column(header='Value', justify='right', footer=f'Total: {total_value}', style='green')
        table.add_column(header='Can afford?', justify='center', footer=f'Total balance: {self.balance}')
        # sorted_keys = sorted(self.product_dict.values(), key=lambda it: (it[1], it[0]))  # sort by value & nec
        # sorted_keys = sorted(self.product_dict.keys(), key=lambda it: )
        sorted_keys = [key for key, value in sorted(self.product_dict.items(), key=lambda it: (it[1][1], it[1][0]))]
        with Live(table) as live:
            live.update(Align.center(table))
            for i in sorted_keys:
                table.add_row(str(i),  # name
                              str(self.product_dict[i][1]),  # necessity
                              str(self.product_dict[i][0]),  # value
                              Text('+' if self.balance >= self.product_dict[i][0]
                                   else f'-\n({self.product_dict[i][0]-self.balance} needed)',
                                   style='green' if self.balance >= self.product_dict[i][0] else 'red'
                                   )
                              )
                # sleep(0.1)
                live.update(Align.center(table))
            # live.update(Align.center(table))
        # table.show_footer = False
        return table

    def add_item(self, product: str, price: int, nec: int):
        if price > 0:
            self.product_dict.update({product.capitalize(): [price, nec]})
        else:
            raise ValueError('Price can\'t be less than zero')
        db.update({'product_dict': self.product_dict}, User.username == f'{self.name}')

    def rm_item(self, rm_product: str):
        # self.balance -= self.product_dict.get(rm_product.capitalize())[0]
        self.product_dict.pop(rm_product.capitalize())
        db.update({'product_dict': self.product_dict}, User.username == f'{self.name}')

    def buy_item(self, product: str):
        self.balance -= self.product_dict.get(product.capitalize())[0]
        self.product_dict.pop(product.capitalize())
        db.update({'product_dict': self.product_dict}, User.username == f'{self.name}')

    def add_value(self, amount: int):
        self.balance += amount
        db.update({'balance': self.balance}, User.username == f'{self.name}')

    def rm_value(self, amount: int):
        self.balance -= amount
        db.update({'balance': self.balance}, User.username == f'{self.name}')

    def rm_db_user(self):
        db.remove(User.username == f'{self.name}')

    def rm_db_all(self):
        db.truncate()
