import aiogram.exceptions
import re
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from controller import Controller
from enum import Enum, auto
from settings import (
    bot,
    dp,
    hero_name,
    user_info,
    user_progress,
    users_data,
    users_in_game,
    users_story_id
)


"""
The commands module is part of your project and
contains command handlers for the bot.
"""


class UserGameState(Enum):
    """
    An enumeration representing the player's states.

    States:
        IN_GAME: The player is in the game.
        NOT_IN_GAME: The player is not in the game.
    """
    IN_GAME = auto()
    NOT_IN_GAME = auto()


class PersonNameStates(StatesGroup):
    """
    A group of states associated with a person's name.

    States:
        WAITING_FOR_ANSWER: Waiting for the user's response.
    """
    WAITING_FOR_ANSWER = State()


async def start_bot() -> None:
    """Starting the bot"""
    await dp.start_polling(bot)


async def _get_user_info(message: types.Message):
    """
    Extract user information from a message.

    Args:
        message (types.Message): Message information.

    Returns:
        Tuple:
            telegram_id (int): User ID.
            username (str): User name.
            first_name (str): User's first name.
            if_bot (bool): True if the user is a bot.
    """
    user = message.from_user
    telegram_id = user.id
    first_name = user.first_name
    username = user.username
    if_bot = user.is_bot

    return telegram_id, username, first_name, if_bot


async def _delete_inline_keyboard(callback_query: types.CallbackQuery):
    """
    Remove the inline keyboard from the message in response to a
    callback_query.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object.

    Raises:
        aiogram.exceptions.AiogramError
    """
    try:
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=None
        )
    except aiogram.exceptions.AiogramError:
        pass
    

@dp.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    """
    Handler for the /start command to initiate the game.

    Args:
        message (types.Message): Message object containing information about the message.
        state (FSMContext): Bot state context.
    """
    telegram_id, username, first_name, is_bot = await _get_user_info(message)
    user_info.insert_field(telegram_id, username, first_name, is_bot)

    condition = users_in_game.get(telegram_id)
    if condition is not None or condition == UserGameState.IN_GAME:
        await message.answer(
            "/start, недоступно пока вы находитесь в игре"
        )
        return
    
    users_in_game[telegram_id] = UserGameState.NOT_IN_GAME

    progress_code = user_progress.get_plot_code(telegram_id)
    callback_data = "none progress" if progress_code == 1 else "continue"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="начать игру", 
                callback_data="start game",
                ),
            types.InlineKeyboardButton(
                text="продолжить",
                callback_data=callback_data
                ),
        ]
    ])
    await message.answer("Выберите действие:",reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == 'none progress')
async def process_new_game(callback_query: types.CallbackQuery):
    """
    Handler for pressing the 'none progress' button in callback_query.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the request.
    """
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="да", 
                callback_data="start game",
                ),
            types.InlineKeyboardButton(
                text="вернуться в главное меню",
                callback_data="menu"
            )
        ]
    ])

    await bot.send_message(
        callback_query.from_user.id,
        "Сохранение не найдено, хотите ли вы начать сначала ?",
        reply_markup=keyboard,
    )
    await _delete_inline_keyboard(callback_query)


@dp.callback_query(lambda c: c.data == 'menu')
async def start_command(callback_query: types.CallbackQuery):
    """
    Handler for pressing the 'menu' button in callback_query.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object
            containing information about the request.
    """
    await callback_query.bot.send_message(
        callback_query.from_user.id,
        "/start")
    await _delete_inline_keyboard(callback_query)


@dp.callback_query(lambda c: c.data == 'start game')
async def process_start_game(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Handles the request to start the game.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the request.
        state (FSMContext): Bot state context.
    """
    user_id = callback_query.from_user.id
    user_progress.insert_field(user_id, 1)
    await bot.send_message(
        user_id,
        "Введите Имя и Отчество главного героя:"
    )
    await _delete_inline_keyboard(callback_query)
    await state.set_state(state=PersonNameStates.WAITING_FOR_ANSWER)


@dp.message(PersonNameStates.WAITING_FOR_ANSWER)
async def process_user_answer(message: types.Message, state: FSMContext):
    """
    Handler for pressing the 'start game' button in callback_query.

    Args:
        message (types.Message): Message object containing information
            about the message.
        state (FSMContext): Bot state context.
    """
    user_input = message.text.strip()
    name_regex = r'^[A-Za-zА-Яа-я]{2,}\s+[A-Za-zА-Яа-я]{2,}$'
    
    if re.match(name_regex, user_input) and len(user_input.split()) <= 2:
        user_id = message.from_user.id
        formatted_name = ' '.join([part.capitalize() for part in user_input.split()])
        hero_name.insert_field(user_id, formatted_name)

        await message.answer(f"Имя и Отчество главного героя: {formatted_name}")
        await state.clear()
        await _key_continue(message)
    else:
        error_message = """
        Error.
        Пожалуйста, введите два слова (имя и фамилию),
        содержащие по крайней мере две буквы в каждом слове без цифр.
        """
        await message.answer(error_message)


async def _key_continue(message: types.Message):
    """
    Creates a message with an inline keyboard for continuing the action.

    Args:
        message (types.Message): Message object containing information about
            the message.
    """
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Продолжить", 
                callback_data="continue",
                ),
        ],
    ])

    await message.answer(
        "Нажмите чтобы продолжить:",
        reply_markup=keyboard,
    )


@dp.callback_query(lambda c: c.data == "continue")
async def process_continue(callback_query: types.CallbackQuery):
    """
    Handles pressing the "Continue" button.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
    """
    user_id = callback_query.from_user.id
    users_story_id[user_id] = user_progress.get_plot_code(user_id)
    users_data[user_id] = Controller(
        hero_name.get_hero_name(user_id)
        )
    users_in_game[user_id] = UserGameState.IN_GAME
    await story_line(callback_query)


@dp.callback_query(lambda c: c.data == "plot")
async def story_line(callback_query: types.CallbackQuery):
    """
    Handles pressing the inline button with callback_data == "plot".

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.

    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return
        
    try:
        history = users_data[user_id].go_line_script(users_story_id[user_id])
        if history is None:
            await _send_next_location_message(user_id)
        elif _is_option_fork(history):
            await _handle_option_fork(callback_query)
        else:
            await _send_history_message(user_id, history)
        await _delete_inline_keyboard(callback_query)
    except Exception as error:
        await _game_over(callback_query, error)
        return


def _is_option_fork(history):
    """
    Checks if the game story is a branching of options.

    Args:
        history (dict): Dictionary with the game story.

    Returns:
        bool: Result of the options branching check.
    """
    return history.get("option_a") is None and history.get("option_b") is None


async def _handle_option_fork(callback_query):
    """
    Handles the case when the game has a branching of options.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object.
    """
    await option_a(callback_query)


async def _send_next_location_message(user_id):
    """
    Sends a message about the next location in the game.

    Args:
        user_id (int): User's Telegram ID.
    """
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="перейти в следующую лоакцию",
                callback_data="land"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="локация",
                callback_data="land"
            ),
            types.InlineKeyboardButton(
                text="предметы",
                callback_data="items"
            ),
            types.InlineKeyboardButton(
                text="Выход из игры",
                callback_data="exit"
            )
        ]
    ])
    await _send_game_status_message(user_id)
    await bot.send_message(
        user_id, "Перейдите в следующую локацию", reply_markup=keyboard)


async def _send_history_message(user_id, history):
    """
    Sends a message with the game story and choices.

    Args:
        user_id (int): User's Telegram ID.
        history (dict): Dictionary with the text and possible story options.
            Contains keys: "text", "option_a", "option_b".
    """
    keyboard = []
    row = []

    if history.get("option_a") is not None:
        row.append(types.InlineKeyboardButton(
            text=history["option_a"], callback_data="option_a"))
    if history.get("option_b") is not None:
        row.append(types.InlineKeyboardButton(
            text=history["option_b"], callback_data="option_b"))
    
    keyboard.append(row)
    keyboard.extend([
        [
            types.InlineKeyboardButton(text="локация", callback_data="land"),
            types.InlineKeyboardButton(text="предметы", callback_data="items"),
            types.InlineKeyboardButton(text="Выход из игры",
                                      callback_data="exit")
        ]
    ])

    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard) 
    await _send_game_status_message(user_id)
    await bot.send_message(
        user_id, 
        history["text"], 
        reply_markup=inline_keyboard)


async def _send_game_status_message(user_id):
    """
    Sends a message with the current game status to the user.

    Args:
        user_id (int): User's Telegram ID.

    Raises:
        aiogram.exceptions.AiogramError
    """
    enemy_health = users_data[user_id].get_health_enemy()
    hp_hero = users_data[user_id].get_health_protogonist()
    exp = users_data[user_id].get_exp_protogonist()

    await bot.send_message(user_id, f"Роман\n\tЗдоровье: {enemy_health}")
    await bot.send_message(
        user_id, 
        f"{hero_name.get_hero_name(user_id)}\n\tЗдоровье: {hp_hero} \n\tОпыт: {exp}")

    
@dp.callback_query(lambda c: c.data == "option_a")
async def option_a(callback_query: types.CallbackQuery):
    """
    Handles pressing the "option_a" button.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return
    try:
        history = users_data[user_id].go_line_script(users_story_id[user_id])
    except Exception as error:
        await _game_over(callback_query, error)
        return
    users_story_id[user_id] = history["next_id_dial_a"]
    await story_line(callback_query)


@dp.callback_query(lambda c: c.data == "option_b")
async def option_b(callback_query: types.CallbackQuery):
    """
    Handles pressing the "option_b" button.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return
    try:
        history = users_data[user_id].go_line_script(users_story_id[user_id])
    except Exception as error:
        await _game_over(callback_query, error)
        return
    users_story_id[user_id] = history["next_id_dial_b"]
    await story_line(callback_query)


@dp.callback_query(lambda c: c.data == "land")
async def location(callback_query: types.CallbackQuery):
    """
    Handles transitioning to a new location.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return

    row = []
    keyboard = []
    history = users_data[user_id].go_line_script(users_story_id[user_id])
    
    if history is not None:
        row.append(types.InlineKeyboardButton(
            text="Недоступно. Прослушайте все диалоги",
            callback_data="plot"
        ))
    else:
        list_direction =  users_data[user_id].get_direction()

        for direction in list_direction:
            row.append(types.InlineKeyboardButton(
                text=direction,
                callback_data=direction
            ))
    
    keyboard.append(row)
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard) 
    await bot.send_message(
        user_id,
        f"Локация: {users_data[user_id].get_current_location()}"
    )
    await bot.send_message(
        user_id,
        f"{users_data[user_id].get_description_current_location()}",
        reply_markup=inline_keyboard,
    )
    await _delete_inline_keyboard(callback_query)


@dp.callback_query(lambda c: c.data == "direction")
async def process_choise_ditection(callback_query: types.CallbackQuery):
    """
    Handler for choosing a movement direction.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return
    direction = callback_query.data
    users_story_id[user_id] = users_data[user_id].go(direction)
    await story_line(callback_query)


@dp.callback_query(lambda c: c.data == "вперед")
async def process_choise_forward(callback_query: types.CallbackQuery):
    """
    Handler for choosing forward movement.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
    """
    await process_choise_ditection(callback_query)


@dp.callback_query(lambda c: c.data == "назад")
async def process_choise_back(callback_query: types.CallbackQuery):
    """Handler for choosing backward movement.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
    """
    await process_choise_ditection(callback_query)


@dp.callback_query(lambda c: c.data == "налево")
async def process_choise_left(callback_query: types.CallbackQuery):
    """
    Handler for choosing left movement.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
    """
    await process_choise_ditection(callback_query)


@dp.callback_query(lambda c: c.data == "направо")
async def process_choise_right(callback_query: types.CallbackQuery):
    """
    Handler for choosing right movement.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
    """
    await process_choise_ditection(callback_query)


@dp.callback_query(lambda c: c.data == "items")
async def process_items(callback_query: types.CallbackQuery):
    """
    Handler for display user items.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return
    
    row = []
    keyboard = []
    # предмет всегда в 1м количестве
    item = users_data[user_id].get_attributes()
    
    if item is None:
        row.append(types.InlineKeyboardButton(
            text="Предметы не найдены, перейти к сюжету",
            callback_data="plot"
        ))
    else:
        row.append(types.InlineKeyboardButton(
            text=f"использовать предмет",
            callback_data="use_item"
        ))
        row.append(types.InlineKeyboardButton(
            text="Вернуться к сюжету",
            callback_data="plot"
        ))
        
    keyboard.append(row)
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard) 
    await bot.send_message(
        callback_query.from_user.id,
        f"Предмет:{item}",
        reply_markup=inline_keyboard,
    )
    await _delete_inline_keyboard(callback_query)


@dp.callback_query(lambda c: c.data == "use_item")
async def process_use_item(callback_query: types.CallbackQuery):
    """
    Handler for using items.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return
    users_data[user_id].use_attributes()
    await story_line(callback_query)


async def _game_over(callback_query: types.CallbackQuery, error):
    """
    Notifies the user about the end of the game due to an error.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
        error (Exception): The error that led to the end of the game.
    """
    user_id = callback_query.from_user.id
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Выход из игры",
                callback_data="exit"
            )
        ]
    ]

    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.send_message(
        user_id,
        str(error),
        reply_markup=inline_keyboard,
    )
    await _delete_inline_keyboard(callback_query)


@dp.callback_query(lambda c: c.data == "exit")
async def exit(callback_query: types.CallbackQuery):
    """
    User exits the game.

    Args:
        callback_query (types.CallbackQuery): CallbackQuery object containing
            information about the button press.
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is not None:
        user_progress.insert_field(user_id, users_story_id[user_id])

        del users_data[user_id]
        del users_story_id[user_id]
        del users_in_game[user_id]

    await callback_query.bot.send_message(
        callback_query.from_user.id,
        "/start")
    await _delete_inline_keyboard(callback_query)
