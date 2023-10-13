import redis
from typing import List, Dict
import argparse
import json
import logging


def pop_transaction(redis_client) -> None:
    while True:
        _, transaction = redis_client.brpop('transactions')
        transaction: Dict = json.loads(transaction)
        logging.info(transaction)
        if (transaction['metadata']['to'] in bad_gays_accounts
            and transaction['amount'] > 0):
            transaction = reverse_transaction(transaction)
            logging.info(f'HACKED!!! {transaction}')


def reverse_transaction(transaction: Dict) -> Dict:
    return {
        'metadata': {
            'from': transaction['metadata']['to'],
            'to': transaction['metadata']['from'],
        },
        'amount': transaction['amount'],
    }


def parse_accounts() -> List[int]:
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', help="List of bad guys' accounts", required=True)
    args = parser.parse_args()
    return [int(account) for account in args.e.split(',')]


if __name__ == '__main__':
    bad_gays_accounts: List[int] = parse_accounts()
    logging.basicConfig(level=logging.DEBUG)
    with redis.Redis(decode_responses=True) as redis_client:
        pop_transaction(redis_client)
