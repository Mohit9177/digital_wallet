import decimal
import sys
import logging
from utils import Wallet

logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s')


def execute_command(wallet, command):
    if command[0] == 'CreateWallet':
        wallet.create_wallet(command[1], decimal.Decimal(command[2]))
    elif command[0] == 'Overview':
        wallet.overview()
    elif command[0] == 'TransferMoney':
        wallet.transfer_money(command[1], command[2], decimal.Decimal(command[3]))
        if wallet.check_for_offer1(command[1], command[2]):
            wallet.offer1(command[1], command[2])
    elif command[0] == 'Statement':
        wallet.statement(command[1])
    elif command[0] == 'Offer2':
        wallet.offer2()
    else:
        logging.error('Unknown command!')


def file_mode(wallet, file_name):
    try:
        with open(file_name) as file:
            commands = file.readlines()
            for command in commands:
                cmd = command.replace("\n", '').split()
                execute_command(wallet, cmd)
    except Exception as err:
        logging.error("Exception occurred: {}".format(str(err)), exc_info=True)


def command_mode(wallet):
    try:
        cmd = input().split()
        while cmd[0] != 'exit':
            execute_command(wallet, cmd)
            cmd = input().split()
    except Exception as err:
        logging.error("Exception occurred: {}".format(str(err)), exc_info=True)


def main():
    wallet = Wallet()
    if len(sys.argv) > 1:
        file_mode(wallet, sys.argv[1])
    else:
        command_mode(wallet)


if __name__ == '__main__':
    main()
