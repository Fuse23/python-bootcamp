"""
Основной скрипт запуска бота.

Модули:
- sys: Содержит функции и переменные, связанные с интерпретатором Python.
- logging: Модуль для логирования сообщений.
- asyncio: Поддержка асинхронного программирования в Python.

Функции:
- start_bot(): Запускает основной бот.

"""

import sys
import logging
import asyncio

from commands import start_bot


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_bot())
