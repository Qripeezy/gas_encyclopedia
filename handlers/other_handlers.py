from database.database import users, gas_list, param_list
from aiogram import F, Router
from aiogram.types import Message, ContentType
from services.properties import calc_property


router = Router()


# Хендлер для события ввода газа
@router.message(F.text and F.text.upper().in_(gas_list))
async def process_gas_input(message: Message):
    gas = message.text.upper()
    if not users[message.from_user.id]["calculating"]:
        users[message.from_user.id]["calculating"] = True
        await message.answer(gas_list.get(gas))
        users[message.from_user.id]["gas"] = gas
        await message.answer("Введите необходимый параметр в нужном формате")
    else:
        await message.answer("В режиме расчета можно только вычислять параметры и выполнять команды")


# Хендлер для события ввода искомого параметра
@router.message(F.text and F.text.split()[0] in param_list and F.text.find("=") == -1 and F.text.find("\n") == -1)
async def process_searched_param_input(message: Message):
    param_type: str = message.text.split()[0]
    param_name: str = message.text.split()[1]
    status: str = "result"
    users[message.from_user.id]["parameters"][param_name] = {
        "type": param_type,
        "value": None,
        "status": status
    }
    await message.answer("Введите 2 вспомогательных параметра в нужном формате")


# Хендлер для события ввода вспомогательных параметров
@router.message(lambda x: x.text and x.text.find("\n") != -1 and len(x.text.split("\n")) == 2 and
                x.text.split("\n")[0].split()[0] in param_list and
                x.text.split("\n")[1].split()[0] in param_list)
async def process_other_params_input(message: Message):
    for param in message.text.split("\n"):
        param_type: str = param.split()[0]
        param_name: str = param.split()[1]
        if param.find("=") == -1:
            if users[message.from_user.id]["parameters"].get(param_name) is not None:
                if users[message.from_user.id]["parameters"][param_name].get("value") is None:
                    await message.answer(f"Значение переменной {param_name} не задано\nВведите корректные переменные")
                    break
                else:
                    param_value = users[message.from_user.id]["parameters"][param_name].get("value")
            else:
                await message.answer(f"Переменная {param_name} не задана\nВведите корректные переменные")
                break
        else:
            param_value: float = float(param.split(" = ")[1])
        status = "param" + str(message.text.split("\n").index(param) + 1)
        users[message.from_user.id]["parameters"][param_name] = {
            "type": param_type,
            "value": param_value,
            "status": status
        }
    for var_name in list(users[message.from_user.id]["parameters"].keys()):
        if users[message.from_user.id]["parameters"][var_name]["status"] == "param1":
            first_param_value = users[message.from_user.id]["parameters"][var_name].get("value")
            first_param_type = users[message.from_user.id]["parameters"][var_name].get("type")
            users[message.from_user.id]["parameters"][var_name]["status"] = None
        if users[message.from_user.id]["parameters"][var_name]["status"] == "param2":
            second_param_value = users[message.from_user.id]["parameters"][var_name].get("value")
            second_param_type = users[message.from_user.id]["parameters"][var_name].get("type")
            users[message.from_user.id]["parameters"][var_name]["status"] = None
        if users[message.from_user.id]["parameters"][var_name]["status"] == "result":
            result_type = users[message.from_user.id]["parameters"][var_name].get("type")
            result_name = var_name
            users[message.from_user.id]["parameters"][var_name]["status"] = None
    result_value = calc_property(result_type, first_param_type, first_param_value, second_param_type,
                                 second_param_value, users[message.from_user.id].get("gas"))
    users[message.from_user.id]["parameters"][result_name]["value"] = result_value
    await message.answer(f"Значение вычислено!\n{result_name} = {result_value}")


# Хендлер для некорректного типа ввода
@router.message(F.content_type != ContentType.TEXT)
async def process_wrong_type(message: Message):
    await message.answer("Обработка неверного типа ввода (фото и тд)")


# Хендлер для прочих сообщений
@router.message()
async def process_other_messages(message: Message):
    await message.answer("Я не понимаю о чем речь")
