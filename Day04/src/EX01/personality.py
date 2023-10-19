import random
from typing import Dict, List


def turrets_generator():
    def generate_personality() -> Dict[str, int]:
        values: List[int] = []
        curr_sum: int = 0
        for _ in range(4):
            values.append(random.randint(0, 100 - curr_sum))
            curr_sum += values[-1]
        values.append(100 - curr_sum)
        return {
            'neuroticism': values[0],
            'openness': values[1],
            'conscientiousness': values[2],
            'extraversion': values[3],
            'agreeableness': values[4],
        }


    def shoot() -> None:
        print('Shooting')


    def serach() -> None:
        print('Searching')


    def talk() -> None:
        print('Talking')


    while True:
        turret = type('Turret', (object, ), {
            'shoot': shoot,
            'search': serach,
            'talk': talk,
        } | generate_personality())
        yield turret


def tests() -> None:
    def count_turret_fields(turret) -> int:
        return (
            turret.neuroticism
            + turret.openness
            + turret.conscientiousness
            + turret.extraversion
            + turret.agreeableness
        )


    def print_turrtel_fields(turret) -> None:
        print(
            f'neuroticism: {turret.neuroticism}',
            f'openness: {turret.openness}',
            f'conscientiousness: {turret.conscientiousness}',
            f'extraversion: {turret.extraversion}',
            f'agreeableness: {turret.agreeableness}',
        )


    def test_1() -> None:
        print('TEST 1\n')
        turrets = turrets_generator()
        turret = next(turrets)
        for _ in range(3):
            print(turret)
            turret.shoot()
            turret.search()
            turret.talk()
            print_turrtel_fields(turret)
            print(f'Sum turret fields: {count_turret_fields(turret)}')
            turret = next(turrets)


    test_1()


if __name__ == '__main__':
    tests()
