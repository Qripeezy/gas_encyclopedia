from dataclasses import dataclass
from environs import Env


# @dataclass
# class DatabaseConfig:
#     database: str         # Название базы данных
#     db_host: str          # URL-адрес базы данных
#     db_user: str          # Username пользователя базы данных
#     db_password: str      # Пароль к базе данных


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot
    # db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    # Создаем экземпляр класса Env
    env: Env = Env()
    # Добавляем в переменные окружения данные, прочитанные из файла .env
    env.read_env(path)
    # Создаем экземпляр класса Config и наполняем его данными из переменных окружения
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
        )
    )