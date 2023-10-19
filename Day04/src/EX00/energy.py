from typing import List, Any
from itertools import zip_longest, starmap


def generate_str(*args) -> str:
    x, y = args
    if not y:
        return 'weld '+x[0]+' to '+x[1]+' without plug'
    return 'plug '+x[0]+' into '+x[1]+' using '+y


def fix_wiring(cabels: List[str | Any],
               sockets: List[str | Any],
               plugs: List[str | Any]):
    # return starmap(generate_str, filter(lambda x: not x[0] is None, zip_longest(zip(filter(lambda x: isinstance(x, str), cabels),filter(lambda x: isinstance(x, str), sockets),),filter(lambda x: isinstance(x, str), plugs))))
    return starmap(
        generate_str,
        filter(
            lambda x: not x[0] is None,
            zip_longest(
                zip(
                    filter(lambda x: isinstance(x, str), cabels),
                    filter(lambda x: isinstance(x, str), sockets),
                ),
                filter(lambda x: isinstance(x, str), plugs)
            )
        )
    )


def tests() -> None:
    assert list(fix_wiring(
        plugs=['plug1', 'plug2', 'plug3'],
        sockets=['socket1', 'socket2', 'socket3', 'socket4'],
        cabels=['cable1', 'cable2', 'cable3', 'cable4'],
    )) == [
        'plug cable1 into socket1 using plug1',
        'plug cable2 into socket2 using plug2',
        'plug cable3 into socket3 using plug3',
        'weld cable4 to socket4 without plug',
    ]
    assert list(fix_wiring(
        plugs=['plugZ', None, 'plugY', 'plugX'],
        sockets=[1, 'socket1', 'socket2', 'socket3', 'socket4'],
        cabels=['cable2', 'cable1', False],
    )) == [
        'plug cable2 into socket1 using plugZ',
        'plug cable1 into socket2 using plugY',
    ]
    assert list(fix_wiring(
        plugs=['plugZ', None],
        sockets=[1, 'socket1'],
        cabels=['cable2', 'cable1', False],
    )) == [
        'plug cable2 into socket1 using plugZ',
    ]
    print('Tests passed!!!')


if __name__ == '__main__':
    plugs = ['plug1', 'plug2', 'plug3']
    sockets = ['socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable1', 'cable2', 'cable3', 'cable4']
    for c in fix_wiring(cables, sockets, plugs):
        print(c)
    print()
    plugs = ['plugZ', None, 'plugY', 'plugX']
    sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable2', 'cable1', False]
    for c in fix_wiring(cables, sockets, plugs):
        print(c)
    # tests()

