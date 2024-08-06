from database.database import users
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message


router = Router()


# Хендлер для команды /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer("Приветствие пользователя\nКраткое инфо о функционале бота\n"
                         "Список команд\nПредложение ввести газ")
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            "calculating": False,
            "gas": None,
            "parameters": {}
        }


# Хендлер для команды /help
@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer("Подробная помощь по функционалу бота, формат ввода и тд")


# Хендлер для команды /param
@router.message(Command(commands="param"))
async def process_param_command(message: Message):
    response: str = f"gas = {users[message.from_user.id].get('gas')}\n"
    for param in list(users[message.from_user.id].get("parameters").keys()):
        response = response + f"{param} = {users[message.from_user.id]['parameters'][param]['value']}\n"
    await message.answer(f"Текущий список переменных:\n{response}")


# Хендлер для команды /cancel
@router.message(Command(commands="cancel"))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]["calculating"]:
        users[message.from_user.id]["gas"] = None
        users[message.from_user.id]["calculating"] = False
        users[message.from_user.id]["parameters"] = {}
        await message.answer("Вы вышли из вычислений. Может, посчитаем что-нибудь?")
    else:
        await message.answer("Вычисления и так не производятся. Может, посчитаем что-нибудь?")
