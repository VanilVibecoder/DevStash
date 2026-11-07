# «Блокнот с ответами»: функция один раз посчитает — дальше берём результат из памяти, не пересчитываем.
from functools import lru_cache

# «Навигатор по файлам»: умные пути — можно спросить .exists(), прочитать файл, склеить папку с файлом через /.
from pathlib import Path

# «Переводчик с языка конфигов»: даёшь TOML-файл → получаешь обычный словарь.
from tomllib import load

# «Подсказки для программиста» (не команды, а записки):
#   Type    — «сюда передают чертёж, а не готовую вещь» (класс, а не объект).
#   TypeVar — «переменная вместо типа»: что на входе, то и на выходе.
from typing import Type, TypeVar

# «Анкета с проверкой» + «секретная коробочка»:
#   BaseModel — описываешь поля и типы, Pydantic сам проверяет, что всё правильно.
#   SecretStr — пароль/токен прячется под **********, достать можно только осознанно через .get_secret_value().
from pydantic import BaseModel, SecretStr


# [1]

ConfigType = TypeVar("ConfigType",bound=BaseModel)


# [2]

class BotConfig(BaseModel):
    token: SecretStr


# [3]
# @lru_cache — "кэш": функция выполнится один раз, дальше результат берётся из памяти.
# Это удобно, т.к. функция без аргументов — значит результат всегда один и тот же.
@lru_cache
def parse_config_file() -> dict:
    # -> dict значит "функция вернёт словарь" (это подсказка, на работу не влияет)

    # __file__ — путь к ЭТОМУ файлу с кодом.
    # .parent — папка, где лежит файл.
    # .parent ещё раз — папка на уровень выше.
    # .joinpath("settings.toml") — приклеить имя файла.
    # Итог: полный путь к settings.toml, который лежит рядом с проектом.
    config_path = Path(__file__).parent.parent.joinpath("settings.toml")

    # Если файла по этому пути нет...
    if not config_path.exists():
        # ...падаем с понятной ошибкой, а не идём дальше вслепую.
        error = "Could not find settings file"
        raise ValueError(error)

    # with open(...) — открыть файл; with сам закроет его после блока,
    # даже если внутри случится ошибка.
    # "rb" = read + binary: только читать, в бинарном режиме (так требует tomllib).
    with open(config_path, "rb") as file:
        # load(file) — "переводчик" TOML → Python-словарь.
        # Кладём результат в config_data.
        config_data = load(file)

    # Отдаём словарь наружу. Благодаря @lru_cache этот return
    # реально сработает только ОДИН раз за всё время работы программы.
    return config_data


# [4]
# model — класс настроек (например BotConfig), root_key — имя раздела в конфиге (например "bot")
# -> ConfigType — вернём экземпляр того же класса, что передали в model
def get_config(model: Type[ConfigType], root_key: str) -> ConfigType:
    # читаем весь конфиг в словарь (второй раз — уже из кэша, файл не трогаем)
    config_dict = parse_config_file()

    # если раздела с таким именем нет — падаем с понятной ошибкой
    if root_key not in config_dict:
        error = f"Key {root_key} not found in config"
        raise KeyError(error)

    # 1) config_dict[root_key] — достаём из словаря нужный раздел
    # 2) model.model_validate(...) — превращаем этот словарь в объект класса model
    #    (Pydantic проверит, что все поля есть и правильного типа)
    # 3) return — отдаём готовый объект наружу
    return model.model_validate(config_dict[root_key]) # [5]