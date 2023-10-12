import redis
import random
from typing import List, Any, Dict, Tuple
import json
from time import sleep
import logging


ACCOUNTS: List[int | Any] = [
    1111111111,
    2222222222,
    3333333333,
    123,          # not valid
    4444444444,
    5555555555,
    456787763,    # not valid
    6666666666,
    0,            # not valid
    7777777777,
    8888888888,
    9999999999,
    '1234567890', # not valid
    [0000000000], # not valid
]


def push_transactions(redis_client) -> None:
    while True:
        transaction: Dict = get_transaction()
        if not is_valid_transaction(transaction):
            logging.error(transaction)
            continue
        redis_client.lpush('transactions', json.dumps(transaction))
        logging.info(transaction)
        sleep(1)


def is_valid_transaction(transaction: Dict) -> bool:
    if (transaction['metadata']['from'] == transaction['metadata']['to']
        or len(str(transaction['metadata']['from'])) != 10
        or len(str(transaction['metadata']['to'])) != 10
        or transaction['amount'] == 0):
        return False
    return True


def get_random_data() -> Tuple[int]:
    return (
        random.choice(ACCOUNTS),
        random.choice(ACCOUNTS),
        random.randint(-10000, 10000),
    )


def get_transaction() -> Dict:
    sender, receiver, value = get_random_data()
    return {
        "metadata": {
            "from": sender,
            "to": receiver,
        },
        "amount": value,
    }


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with redis.Redis() as redis_client:
        push_transactions(redis_client)
