from typing import Iterator, Callable
import random
import time


def emit_gel(step: int) -> Iterator[int]:
    pressure: int = 50
    while True:
        pressure += random.randint(min(0, step), max(0, step))
        if pressure > 100:
            pressure = 100
        step = yield pressure


def valve(generator: Callable[[int], Iterator[int]],
          step_size: int,
          show_result: bool,
          time_sleep: bool) -> None:
    pressures: Iterator[int] = emit_gel(step_size)
    pressure: int = next(pressures)
    while 10 <= pressure <= 90:
        if show_result:
            print(f'Current pressure: {pressure}')
            print(f'Current step: {step_size}')
        if time_sleep:
            time.sleep(0.5)
        if pressure < 20:
            step_size = abs(step_size)
        elif pressure > 80:
            step_size = -abs(step_size)
        pressure = pressures.send(step_size)
    else:
        pressures.close()
        print(f'Pressure is above the norm: {pressure}')
        print(f'Current step: {step_size}')


def tests() -> None:
    print('\nTEST1\n')
    valve(emit_gel, 50, True, True)
    print('\nTEST2\n')
    valve(emit_gel, 22, True, False)


if __name__ == '__main__':
    tests()
