from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import KeyboardBuilder
from asgiref.sync import sync_to_async
from automation.models import StudyingTime

async def get_times_shedule():
    time_periods = await sync_to_async(StudyingTime.objects.all().order_by)('start_time')
    builder = KeyboardBuilder(button_type=InlineKeyboardButton)
    time_periods_buttons = []
    async for time_choise in time_periods:
        time_button = InlineKeyboardButton(text=str(time_choise.start_time), callback_data=f'time_{time_choise.pk}')
        time_periods_buttons.append(time_button)
    # else:
    #     time_periods_buttons.append(InlineKeyboardButton(text=str(' Необходимо согласовать с ПМ\nhttps://dvmn.org/'), callback_data=f'time_Error'))
    builder.row(*time_periods_buttons, width=3)
    return InlineKeyboardMarkup(inline_keyboard=builder.export())

def get_type_of_commands():
    builder = KeyboardBuilder(button_type=InlineKeyboardButton)
    student_level = ['newbie','newbie_plus','junior'] #потом это тоже можно сделать как отдельная таблица и из нее брать данные
    buttons = []
    for level in student_level:
        level_button = InlineKeyboardButton(text=str(level), callback_data=f'level-{str(level)}')
        buttons.append(level_button)
    builder.row(*buttons, width=3)
    return InlineKeyboardMarkup(inline_keyboard=builder.export())


kb_choise_main_menu = [
    [types.KeyboardButton(text="Посмотреть информацию")],
    [types.KeyboardButton(text="Записаться на время")],
    [types.KeyboardButton(text="Отказаться от созвона")],
    [types.KeyboardButton(text="О Devman...")]
]
main_menu = types.ReplyKeyboardMarkup(
    keyboard=kb_choise_main_menu,
    resize_keyboard=True,)

kb_choise_main_menu_pm = [
    [types.KeyboardButton(text="Расформировать команды")],
    [types.KeyboardButton(text="Сформировать команды")],
    [types.KeyboardButton(text="Дополнить команды")],
    [types.KeyboardButton(text="Оповестить участников")],
]
main_menu_pm = types.ReplyKeyboardMarkup(
    keyboard=kb_choise_main_menu_pm,
    resize_keyboard=True,)
