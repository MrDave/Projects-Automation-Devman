from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State

import logging
import os
from collections import defaultdict
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
from project.settings import LIMIT_USER_IN_TEAM

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
        user_id = DevmanUser(telegram_id=int(message.from_user.id), first_name=message.from_user.first_name)
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
        try:
            await bot.send_message(str(user.telegram_id), f'Проверка рассылки и т.д...')
        except TelegramBadRequest:
            await bot.send_message(message.from_user.id, f'Пользователь телеграмм {str(user.telegram_id)} не существует')


@router.message(F.text == "О Devman...")
async def create_order(message: Message):
    await message.answer('https://dvmn.org/')

@router.message(F.text == "Показать команды")
async def create_order(message: Message):
    await message.answer('https://dvmn.org/')

@router.message(F.text == "Сформировать команды")
async def create_team(message: Message):
    await bot.send_message(message.from_user.id, 'Укажите тип формируемых команд',
                           reply_markup=get_type_of_commands())


@router.callback_query(F.data.startswith('level-'))
async def get_level_handler(callback: CallbackQuery):
    # алгоритм :
    # удалить все команды, если какие-либо были ранее
    # по всем студентам сформировать id : время записи
    # организовать цикл по временным слотам
    # ... и формировать новые группы
    logger.info(f'time handler - {callback.data}')
    # создание студентов...
    # T.ODO проверить если уже юзер в студента, иначе новый

    student_level = callback.data.split('-')[-1]

    students = []
    await sync_to_async(StudyGroup.objects.all().delete)()
    async for student in Student.objects.all().order_by('preferred_time'):
        students.append(student)

    # for _ in students:
    #     print(_)
    # posts_with_comments = Post.objects.filter(id__in=most_popular_posts_ids).annotate(comments_count=Count('comments'))
    students = await sync_to_async(Student.objects.all)()
    student_id_time_id_qs = await sync_to_async(students.values_list)('id', 'preferred_time') #ключ-это id cтудента, значение - id времени слота
    student_id_time_id = await sync_to_async(dict)(student_id_time_id_qs)
    # sstudent = student_id_time_id.items()
    # student_id_time_id = await sync_to_async(dict)(student_id_time_id_qs.items)()
    # student_id_time_id = await sync_to_async(dict(student_id_time_id_qs).items)()
    # d = defaultdict(list)
    # for k, v in sstudent:
    #     d[k].append(v)

    # search_student_list = sorted(d.items())


    # цикл по слотам, исключая слот-время, которое "задаст ПМ сам", т.е. только по реальным указанным
    # await studying_time_slot = StudyingTime.objects.all().order_by('start_time')
    async for time_slot in StudyingTime.objects.all().order_by('start_time')[1:]:
        # цикл по студентам из словаря
        total_members = 0
        team = None
        students_with_the_same_time = [key for key in student_id_time_id if student_id_time_id[key] == time_slot.id]
        for student_id in students_with_the_same_time:
            if total_members==0:
                team = StudyGroup(name=f"Команда уровня {student_level} созвон с {time_slot} ", call_time=time_slot)
                await sync_to_async(team.save)()
                await sync_to_async(Student.objects.filter(id=student_id).update)(current_group=team)
                total_members += 1
            else:
                await sync_to_async(Student.objects.filter(id=student_id).update)(current_group=team)
                total_members += 1
                if total_members > LIMIT_USER_IN_TEAM:
                    total_members = 0

    # есть команды или нет ни одной, но тогда случай, когда Время по Выбору ПМ
    if await sync_to_async(StudyGroup.objects.all)():
        # цикл по командам, проверять места и добавлять или создавать новые
        # считать сколько чел без времени
        pass

    else:
        pass

        #думать !!!!

        #просто создать и всем её указать, нужно дорабатывать логику...
        # team_non_time = sync_to_async(StudyGroup(name=f"Команда уровня {student_level} время созвона не указано", call_time=sync_to_async(StudyingTime.objects.all().order_by('start_time').first)()))()
        # await sync_to_async(team_non_time.save)()
        # await sync_to_async(Student.objects.filter(preferred_time=StudyingTime.objects.all().order_by('start_time').first()).update)(current_group=team_non_time)


    await bot.send_message(callback.from_user.id, 'iэnfo')


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
    if time_shudule_id=='Error':
        await bot.send_message(callback.from_user.id, "Свяжитесь с вашим ментором...")
    else:
        user_name = await sync_to_async(DevmanUser.objects.filter(telegram_id=callback.from_user.id).first)()
        start_time = await sync_to_async(StudyingTime.objects.filter(pk=time_shudule_id).first)()

        info = f'Студент создан {datetime.datetime.now()}.\nУказал удобное время {start_time}'
        # type = 'newbie' т.к. это уровень задаст ПМ в админке
        student = Student(user=user_name, level='newbie', preferred_time=start_time, info=info)
        await sync_to_async(student.save)()
        await bot.send_message(callback.from_user.id, info)

