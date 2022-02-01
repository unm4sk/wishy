from rich.console import Console
from rich.theme import Theme
from tinydb import TinyDB, Query
from whishlist_db import WishListDB
from descriptions import *
from time import sleep


db = TinyDB('db.json')
theme = Theme({'success': 'bold green', 'warning': 'underline yellow',
               'error': 'underline red', 'critical': 'blink bold underline red on black'})
console = Console(theme=theme)
User = Query()


# user menu
while True:
    try:
        console.clear()
        if len(db) > 0:
            username_list = [item['username'] for item in db.all()]
            console.print(users)
            for num, i in enumerate(username_list):
                console.print(f'{num+1}. {i}')
            while True:
                try:
                    username = username_list[int(input('>>> ').strip())-1]
                    break
                except:  # if user selected an unknown name
                    new_user_validation = input('Create a new user? [y/n] ').lower().strip()
                    if new_user_validation == 'y':
                        username = str(input('Enter your username: ').strip())
                        while True:
                            try:
                                balance = int(input('Enter your current balance: '))
                                if balance < 0:
                                    console.print('Balance can\'t be negative!', style='error')
                                    continue
                                user = WishListDB(username, balance)
                                break_validation = True
                                break
                            except KeyboardInterrupt:
                                console.clear()
                                exit(0)
                                break
                            except:
                                console.print('Balance must contain only numbers!', style='error')
                                continue
                    else:
                        continue
                    if break_validation:
                        break
            user = WishListDB(username, db.get(User.username == f'{username}')['balance'])

        else:
            username = str(input('Enter your username: ').strip())
            balance = int(input('Enter your current balance: '))
            user = WishListDB(username, balance)
        # user.build_table()
        break
    except ValueError:
        console.print('An error has occurred!', style='critical')
        continue
    except KeyboardInterrupt:
        console.clear()
        exit(0)
        break


if __name__ == '__main__':
    # inherit()
    # console.clear()
    user.build_table()
    console.print(menu)
    while True:
        try:
            command = (input('\n>>> ').lower().strip()).split()
            choice = command[0]
            match choice:
                case 'addit':
                    try:
                        # command = (input('\n>>> ').lower().strip()).split()
                        item, price, nec = str(command[1]), int(command[2]), int(command[3])  # console-like input
                        if price < 0 or not (1 <= nec <= 3):
                            raise ValueError
                        user.add_item(item, price, nec)
                        user.build_table()
                    except:
                        while True:
                            try:
                                # if it didn't work...
                                item = str(input('Enter the name of an item: ').lower().strip())
                                while True:
                                    price = int(input('Its price: ').lower().strip())
                                    if price < 0:
                                        console.print('Price can\'t be negative!', style='error')
                                        continue
                                    else:
                                        break
                                while True:
                                    nec = int(input('Necessity: ').lower().strip())
                                    if 1 <= nec <= 3:
                                        break
                                    else:
                                        console.print('Necessity should be from 1 to 3!', style='error')
                                        continue
                                user.add_item(item, price, nec)
                                user.build_table()
                                break
                            except KeyboardInterrupt:
                                console.clear()
                                exit(0)
                                break
                            except:
                                continue

                case 'buy':
                    try:
                        if user.balance - user.product_dict[command[1].capitalize()][0] < 0:
                            console.print('Your balance now is less than zero!', style='warning')
                            sleep(3)
                        user.buy_item(command[1])
                        user.build_table()
                    except:
                        while True:
                            try:
                                item = str(input('Enter a name of item you bought: ').lower().strip())
                                if user.balance - user.product_dict[item.capitalize()][0] < 0:
                                    console.print('Your balance now is less than zero!', style='warning')
                                    sleep(3)
                                user.buy_item(item)
                                user.build_table()
                                break
                            except KeyboardInterrupt:
                                console.clear()
                                exit(0)
                                break
                            except:
                                continue
                case 'rmit':
                    try:
                        user.rm_item(command[1])
                        user.build_table()
                    except:
                        while True:
                            try:
                                item = str(input('Enter an item you want to delete: ').capitalize().strip())
                                user.rm_item(item)
                                user.build_table()
                                break
                            except KeyboardInterrupt:
                                console.clear()
                                exit(0)
                                break
                            except:
                                continue
                case 'addval':
                    try:
                        if int(command[1]) < 0:
                            raise ValueError
                        user.add_value(int(command[1]))
                        user.build_table()
                    except:
                        while True:
                            try:
                                value = int(input('Enter value: ').strip())
                                if value < 0:
                                    console.print('Value can\'t be negative!', style='error')
                                    continue
                                user.add_value(value)
                                user.build_table()
                                break
                            except KeyboardInterrupt:
                                console.clear()
                                exit(0)
                                break
                            except:
                                continue
                case 'rmval':
                    try:
                        if int(command[1]) < 0:
                            raise ValueError
                        if user.balance - int(command[1]) < 0:
                            console.print('Your balance now is less than zero!', style='warning')
                            sleep(3)
                        user.rm_value(int(command[1]))
                        user.build_table()
                    except:
                        while True:
                            try:
                                value = int(input('Enter value: ').strip())
                                if value < 0:
                                    console.print('Value can\'t be negative!', style='error')
                                    continue
                                if user.balance - value < 0:
                                    console.print('Your balance now is less than zero!', style='warning')
                                    sleep(3)
                                user.rm_value(value)
                                user.build_table()
                                break
                            except KeyboardInterrupt:
                                console.clear()
                                exit(0)
                                break
                            except:
                                continue
                case 'rmuser':
                    break_validation = False
                    while True:
                        try:
                            console.print(danger_zone, style='critical')
                            user_response = str(input('REMOVE CURRENT USER? [YES/NO] ').strip())
                            if user_response == 'YES':
                                user.rm_db_user()
                                console.print(f'User {username} was removed!', style='success')
                                break_validation = True
                                break
                            else:
                                break_validation = False
                                break
                        except KeyboardInterrupt:
                            console.clear()
                            exit(0)
                        except:
                            break
                    if break_validation:
                        sleep(5)
                        console.clear()
                        exit(0)
                        break
                        #     break
                        # except Error as err:
                        #     print(err)
                        #     break
                case 'rmall':
                    break_validation = False
                    while True:
                        try:
                            console.print(danger_zone, style='critical')
                            answer = \
                                str(console.input('ARE YOU SURE YOU WANT TO DELETE THE DATABASE? [YES/NO] ').strip())
                            if answer == 'YES':
                                user.rm_db_all()
                                # console.clear()
                                break_validation = True
                                break
                            else:
                                break_validation = False
                                break
                        except KeyboardInterrupt:
                            console.clear()
                            exit(0)
                            break
                        except:
                            break
                    if break_validation:
                        console.print('The database was deleted successfully!', style='success')
                        sleep(5)
                        console.clear()
                        exit(0)
                        break
                case 'help':
                    console.print(menu)
                case 'exit':
                    console.clear()
                    exit(0)
                case _:
                    continue
        except KeyboardInterrupt:
            console.clear()
            exit(0)
            break
        except IndexError:
            continue

        # finally  log here
                # user.update_table()


# print(user.balance)
