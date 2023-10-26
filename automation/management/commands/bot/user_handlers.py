from aiogram import Router, F, Bot
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State

import logging
import os
# from datetime import datetime
from datetime import datetime
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from environs import Env

# from conf.settings import BASE_DIR
# from shopbot.models import Client, Advertisement, Staff, Bouquet, Order
# from automation.management.commands.bot.user_keyboards import get_catalog_keyboard
from automation.management.commands.bot.user_menu import *
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from automation.models import *

from automation.management.commands.bot.user_menu import (
    get_times_shedule,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d - %(levelname)-8s - %(asctime)s - %(funcName)s - %(name)s - %(message)s'
)

logger = logging.getLogger(__name__)
env: Env = Env()
env.read_env()
bot: Bot = Bot(token=env('TG_BOT_API'), parse_mode='HTML')
router = Router()

class OState(StatesGroup):
    user_name = State()

@router.message(Command(commands=["start"]))
async def start_command_handler(message: Message):
    """
        Обработчик кнопки старт, если пользователя нет в БД - добавляю
    """
    user_id = await sync_to_async(DevmanUser.objects.filter(telegram_id=int(message.from_user.id)).first)()
    if not user_id:
        user_id = DevmanUser(telegram_id=int(message.from_user.id), first_name=message.from_user.first_name, created_at=datetime.datetime.now())
        await sync_to_async(user_id.save)()
        await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}\nВас приветствует учебный бот DEVMAN', reply_markup=main_menu)
    else:
        if await sync_to_async(ProjectManager.objects.filter(telegram_id=int(message.from_user.id)).first)():
        # это ПМ
            await bot.send_message(message.from_user.id,
                                   f'Привет {message.from_user.first_name}',
                                   reply_markup=main_menu_pm)

        else: # это обычный юзер, но зашел повторно
            await bot.send_message(message.from_user.id,
                                   f'Привет {message.from_user.first_name}\nРад снова видеть тебя!!!',
                                   reply_markup=main_menu)


@router.message(F.text == "Оповестить участников")
async def show_main_menu(message: Message):
    async for user in DevmanUser.objects.all().order_by('telegram_id'):
        await bot.send_message(str(user.telegram_id), f'Проверка рассылки и т.д...')

@router.message(F.text == "О Devman...")
async def create_order(message: Message):
    await message.answer('https://dvmn.org/')


@router.message(F.text == "Записаться на время")
async def choise_time_shedule(message: Message):
     #ODO тут необходимо предусмотреть проверку на то что пользователь уже ученик, пока этого нет
     # просто записываем его выбор и заносим его в модель Ученик
     # взять из БД время
     await bot.send_message(message.from_user.id, 'Укажите удобное время для занятий (МСК)', reply_markup=await get_times_shedule())


@router.callback_query(F.data.startswith('time_'))
async def get_time_handler(callback: CallbackQuery):
    logger.info(f'time handler - {callback.data}')
    # создание студентов...
    # T.ODO проверить если уже юзер в студента, иначе новый
    # posts = await sync_to_async(name.devman_user.all)()

    time_shudule_id = callback.data.split('_')[-1]
    user_name = await sync_to_async(DevmanUser.objects.filter(telegram_id=callback.from_user.id).first)()
    start_time = await sync_to_async(StudyingTime.objects.filter(pk=time_shudule_id).first)()

    info = f'Студент создан {datetime.datetime.now()}.\nУказал удобное время {start_time}'
    # type = 'newbie' т.к. это уровень задаст ПМ в админке
    student = Student(name=user_name, type='newbie', start=start_time, info=info)
    await sync_to_async(student.save)()
    await bot.send_message(callback.from_user.id, info)

