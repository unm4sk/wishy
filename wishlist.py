class WishList:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.product_dict = {}  # value as a key, price and nec as a value [price, nec]

    def add(self, product, price, nec):
        self.product_dict.update({product.capitalize(): [price, nec]})
        if self.balance >= price:
            print(f'\nYou can afford {product.capitalize()}!')
            if self.balance - price > 0:
                print(f'If you buy it, you will still have {self.balance - price}')
            else:
                print('If you buy it, you won\'t have any money left!')
            print('Take time to consider whether you need this item or not!')
        else:
            print(f'\nYou cannot afford {product.capitalize()}')
            print(f'You gotta save at least {price - self.balance}!')
            print('Good luck!')

    def bought(self, rm_product):
        self.balance -= self.product_dict.get(rm_product.capitalize())[0]
        self.product_dict.pop(rm_product.capitalize())
        print(f'\nThe item <{rm_product.capitalize()}> was removed!')

    def items(self):
        print('\nYour wish list:')
        print('\tItem\t\tNecessity')
        for item in sorted(self.product_dict.keys(), key=lambda it: self.product_dict[it][1]):
            print('•'+item+'\t\t\t'+str(self.product_dict[item][1]))
        '''
        see all items in a wish list
        :return:
        '''