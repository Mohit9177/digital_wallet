from datetime import datetime
from functools import cmp_to_key
from constants import MINIMUM_BAL, TRANSACTION_TYPES, OFFER1_REWARD, OFFER2_REWARDS
import logging

logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s')


class User(object):
    def __init__(self, name):
        self.name = name


class Transaction:
    def __init__(self, transaction_type, user, transaction_amount):
        self.transaction_type = transaction_type
        self.user = user
        self.created_on = datetime.now()
        self.transaction_amount = transaction_amount


class Account:
    def __init__(self, user, name, amount):
        self.user = user
        self.amount = amount
        self.created_on = datetime.now()
        self.transactions = []
        self.transactions_count = 0
        self.fixed_deposit = False
        self.fixed_deposit_amount = 0
        self.fixed_deposit_start_trans_count = 0

    @staticmethod
    def comparator(a, b):
        if a.transactions_count == b.transactions_count:
            if a.amount == b.amount:
                if a.created_on < b.created_on:
                    return 1
                else:
                    return -1
            elif a.amount > b.amount:
                return 1
            else:
                return -1
        elif a.transactions_count > b.transactions_count:
            return 1
        else:
            return -1


class Wallet:
    def __init__(self):
        self.accounts = []

    def create_wallet(self, name, amount):
        user = User(name)
        account = Account(user, name, amount)
        self.accounts.append(account)

    @staticmethod
    def check_fixed_deposit(account, amount):
        if account.fixed_deposit:
            if account.amount - amount < account.fixed_deposit_amount:
                account.fixed_deposit = False
                account.fixed_deposit_amount = 0
                account.fixed_deposit_start_trans_count = 0
            else:
                account.fixed_deposit_start_trans_count += 1
                if account.fixed_deposit_start_trans_count == 5:
                    account.amount += 10

    def transfer_money(self, sender, receiver, amount):
        sender_acc, receiver_acc = None, None
        for account in self.accounts:
            if account.name == sender:
                sender_acc = account
            elif account.name == receiver:
                receiver_acc = account
        if not sender_acc or not receiver_acc:
            logging.error("Either Sender or Receiver Account Not found!")
        elif sender_acc.amount - amount >= MINIMUM_BAL:
            self.check_fixed_deposit(sender_acc, amount)
            self.check_fixed_deposit(receiver_acc, amount)
            transaction = Transaction(TRANSACTION_TYPES[0], sender_acc.name, amount)
            receiver_acc.transactions.append(transaction)
            transaction = Transaction(TRANSACTION_TYPES[1], receiver_acc.name, amount)
            sender_acc.transactions.append(transaction)
            sender_acc.amount -= amount
            receiver_acc.amount += amount
            sender_acc.transactions_count += 1
            receiver_acc.transactions_count += 1
        else:
            logging.error("Account Balance is not sufficient for transaction!")

    def statement(self, name):
        user_account = None
        for account in self.accounts:
            if account.name == name:
                user_account = account

                break

        for transaction in user_account.transactions:
            print("{} {} {} {}".format(transaction.user, transaction.transaction_type, transaction.transaction_amount, user_account.fixed_deposit_amount))

    def overview(self):
        for account in self.accounts:
            print("{} {} {}".format(account.name, account.amount, account.fixed_deposit_amount))

    def check_for_offer1(self, sender, receiver):
        sender_acc, receiver_acc = None, None
        for account in self.accounts:
            if account.name == sender:
                sender_acc = account
            elif account.name == receiver:
                receiver_acc = account
        if not sender_acc or not receiver_acc:
            logging.error("Either Sender or Receiver Account Not found!")
        elif sender_acc.amount == receiver_acc.amount:
            return True
        return False

    def offer1(self, sender, receiver, amount=OFFER1_REWARD):
        sender_acc, receiver_acc = None, None
        for account in self.accounts:
            if account.name == sender:
                sender_acc = account
            elif account.name == receiver:
                receiver_acc = account
        if not sender_acc or not receiver_acc:
            logging.error("Either Sender or Receiver Account Not found!")
        else:
            transaction = Transaction(TRANSACTION_TYPES[0], TRANSACTION_TYPES[2], amount)
            receiver_acc.transactions.append(transaction)
            transaction = Transaction(TRANSACTION_TYPES[0], TRANSACTION_TYPES[2], amount)
            sender_acc.transactions.append(transaction)
            sender_acc.amount += amount
            receiver_acc.amount += amount

    def offer2(self, reward_users=3):
        accounts = sorted(self.accounts, key=cmp_to_key(Account.comparator), reverse=True)
        for index, ele in enumerate(accounts[: reward_users]):
            transaction = Transaction(TRANSACTION_TYPES[3], ele.name, OFFER2_REWARDS[index])
            ele.transactions.append(transaction)
            ele.amount += OFFER2_REWARDS[index]

    def fixed_deposit(self, name, amount):
        customer_account = None
        for account in self.accounts:
            if account.name == name:
                customer_account = account
                break
        if amount <= customer_account.amount:
            customer_account.fixed_deposit = True
            customer_account.fixed_deposit_amount = amount
            customer_account.fixed_deposit_start_trans_count = customer_account.transactions_count
        else:
            logging.error("Customer account balance is less than fixed_deposit amount")
