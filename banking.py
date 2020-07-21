# Write your code here
import math
import random
import sys
import sqlite3

# id = 0 Поставил авто-увеличение, надо будет чекнуть, что хочет тест

cards_db = {}
conn = sqlite3.connect('card.s3db')
c = conn.cursor()

# Create table
# c.execute('''DROP TABLE IF EXISTS card''')
c.execute('''CREATE TABLE IF NOT EXISTS card (
            id          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULl,
            `number`    TEXT,
            pin         TEXT,
            balance     INTEGER DEFAULT 0
            )''')
conn.commit()


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
# conn.close()

def ft_menu_outer():
    print("""
1. Create an account
2. Log into account
0. Exit
""")
#    c.execute("SELECT * FROM card")  # FOR DEBUG
#    print(c.fetchall())  # FOR DEBUG


def ft_check_input(user_input):
    if user_input == 1:
        card = ft_card_gen()
        pin = ft_pin_gen()
        ft_save_card(card, pin)
    elif user_input == 2:
        ft_auth()
    elif user_input == 0:
        ft_exit()
    return 1


def ft_save_card(card, pin):
    cards_db[card] = pin
    params = (card, pin)
    c.execute("INSERT INTO card(`number`, `pin`) VALUES (?, ?)", params)
    conn.commit()


def ft_roundup(x):
    return int(math.ceil(x / 10.0)) * 10


def ft_luhn(card_number):
    tmp = list(card_number)
    x = 0
    while x < 15:
        tmp[x] = int(tmp[x]) * 2
        if tmp[x] > 9:
            tmp[x] = int(tmp[x]) - 9
        x += 2
    new_card_number = "".join(str(e) for e in tmp)
    check_sum = 0
    for x in new_card_number:
        check_sum += int(x)
    if check_sum % 10 == 0:
        return card_number + '0'
    else:
        last_digit = ft_roundup(check_sum) - check_sum
        return card_number + str(last_digit)


def ft_card_gen():
    global id
    new_account = '400000' + f'{random.randrange(1, 10 ** 9):09}'  # change 10 to 9
    new_card_number = ft_luhn(new_account)
    print("""Your card has been created
Your card number:""")
    print(new_card_number)
    return new_card_number


def ft_pin_gen():
    new_pin = f'{random.randrange(0, 9999):04}'
    print("""Your card PIN:""")
    print(new_pin)
    return new_pin


def ft_auth():
    print("Enter your card number:")
    card_number = input()
    print("Enter your PIN:")
    pin = input()
    val = (card_number, pin)
    c.execute("SELECT * FROM card WHERE `number` = ? AND pin = ?", val)
    auth = c.fetchone()
    #    print(auth)
    if not auth:
        print("\nWrong card number or PIN!")
    else:
        print("\nYou have successfully logged in!")
        ft_inside(card_number)


def ft_inner_menu():
    print("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
""")


def ft_inside(card_number):
    while True:
        ft_inner_menu()
        user_input_inside = int(input())
        if not ft_check_input_inside(user_input_inside, card_number):
            break
        else:
            continue


def ft_check_balance(card_number):
    val = (card_number,)
    c.execute("SELECT balance FROM card WHERE `number` = ?", val)
    balance = c.fetchone()
    print("\nBalance: ", balance[0])


def ft_add_income(card_number):
    try:
        income = int(input("Enter income:\n"))
    except ValueError:
        print("Input is a integer number.")
    val = (income, card_number)
    c.execute("UPDATE card SET balance = balance + ? WHERE `number` = ?", val)
    conn.commit()
    print("Income was added!")


def ft_check_luhn(transfer_card):
    tmp = list(transfer_card)
    x = 0
    while x < 15:
        tmp[x] = int(tmp[x]) * 2
        if tmp[x] > 9:
            tmp[x] = int(tmp[x]) - 9
        x += 2
    transfer_check = "".join(str(e) for e in tmp)
    check_sum = 0
    for x in transfer_check:
        check_sum += int(x)
    if check_sum % 10 == 0:
        return 1
    return 0


def ft_check_transfer_card(card_number, transfer_card):
    if card_number == transfer_card:
        print("\nYou can't transfer money to the same account!")
        return 0
    if not ft_check_luhn(transfer_card):
        print("\nProbably you made mistake in the card number. Please try again!")
        return 0
    val = (transfer_card,)
    c.execute("SELECT * FROM card WHERE `number` = ?", val)
    card_in_db = c.fetchone()
    if not card_in_db:
        print("\nSuch a card does not exist.")
        return 0  # 4000003243107121 Real but deleted to check
    return 1


def ft_transfer(card_number):
    print("""Transfer
Enter card number:""")
    transfer_card = input()
    if not ft_check_transfer_card(card_number, transfer_card):
        return 0
    try:
        transfer_money = int(input("Enter how much money you want to transfer:\n"))
    except ValueError:
        print("Input is a integer number.")
    val = (card_number,)
    c.execute("SELECT balance FROM card WHERE `number` = ?", val)
    user_balance = c.fetchone()
    if user_balance[0] - transfer_money < 0:
        print("\nNot enough money!")
        return 0
    money_take = (transfer_money, card_number)
    c.execute("UPDATE card SET balance = balance - ? WHERE `number` = ?", money_take)
    money_give = (transfer_money, transfer_card)
    c.execute("UPDATE card SET balance = balance + ? WHERE `number` = ?", money_give)
    conn.commit()
    print("Success!")


def ft_close_account(card_number):
    val = (card_number,)
    c.execute("DELETE FROM card WHERE `number` = ?", val)
    print("The account has been closed!")
    conn.commit()


def ft_check_input_inside(user_input_inside, card_number):
    if user_input_inside == 1:
        ft_check_balance(card_number)
    elif user_input_inside == 2:
        ft_add_income(card_number)
    elif user_input_inside == 3:
        ft_transfer(card_number)
    elif user_input_inside == 4:
        ft_close_account(card_number)
        return False
    elif user_input_inside == 5:
        print("You have successfully logged out!")
        return False
    elif user_input_inside == 0:
        ft_exit()
    return 1


def ft_exit():
    print("Bye!")
    conn.close()
    sys.exit()


def ft_outside():
    while True:
        ft_menu_outer()
        user_input = int(input())
        if not ft_check_input(user_input):
            break
        else:
            continue


ft_outside()
