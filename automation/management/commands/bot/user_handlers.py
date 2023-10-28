from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.state import StatesGroup, State

import logging
from datetime import datetime
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from environs import Env

from automation.management.commands.bot.user_menu import *
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

@router.message(F.text == "Расформировать команды")
async def create_order(message: Message):
    await sync_to_async(StudyGroup.objects.all().delete)()
    # await sync_to_async(StudyingTime.objects.all().delete)()
    await message.answer('Успешно...')

@router.message(F.text == "Показать команды")
async def create_order(message: Message):
    await message.answer('https://dvmn.org/')

@router.message(F.text == "Дополнить команды")
async def create_order(message: Message):
    # есть команды или нет ни одной, но тогда случай, когда Время по Выбору ПМ
    # цикл по студентам без времени, добавлять в пустое место команды
    students_free_time = []
    time_zero = await sync_to_async(StudyingTime.objects.get)(start_time='00:00:00')
    async for student in Student.objects.filter(preferred_time=time_zero):
        students_free_time.append(student)

    async for team in StudyGroup.objects.all():
        members_in_team = await sync_to_async(team.groups.all)()
        free_places = await sync_to_async(members_in_team.count)()
        if free_places >= LIMIT_USER_IN_TEAM: #await sync_to_async(members_in_team.count)() !!!
            await bot.send_message(message.from_user.id, f'{team}\nУже заполнена ! Мест - нет !')
        else: #т.е. места есть - добавляю
            available_places = LIMIT_USER_IN_TEAM - free_places
            logging.info(f'доступных мест = {available_places}')
            while students_free_time and available_places > 0: #т.е есть студенты или места
                free_student = await sync_to_async(students_free_time.pop)() #If no argument is provided, the last item in the list is removed.
                # студенту обновить поля команду и время ему тоже
                await sync_to_async(Student.objects.filter(id=free_student.id).update)(current_group=team, preferred_time=team.call_time_id)
                await bot.send_message(message.from_user.id, f'{team}\nДополнена студентом')
                available_places -= 1
    # else:
    #     await bot.send_message(message.from_user.id, f' Внимание !\nНет ни одной из доступных команд')

    #если остались студенты, которым не хватило команд - то просто сообщить это
    if students_free_time:
        await bot.send_message(message.from_user.id, f' Внимание ! Остались {len(students_free_time)} чел. без команды...')


@router.message(F.text == "Сформировать команды")
async def create_team(message: Message):
    await bot.send_message(message.from_user.id, 'Укажите тип формируемых команд',
                           reply_markup=get_type_of_commands())

@router.message(F.text == "Отказаться от созвона")
async def create_team(message: Message):
    # есть ли юзер в студентах
    curent_user = await sync_to_async(DevmanUser.objects.get)(telegram_id=message.from_user.id)
    if curent_user:
        time_zero = await sync_to_async(StudyingTime.objects.get)(start_time='00:00:00')
        await sync_to_async(Student.objects.filter(id=curent_user.id).update)(current_group=None, preferred_time=time_zero)
        await bot.send_message(message.from_user.id, '👌')
    else:
        await bot.send_message(message.from_user.id, 'Вы еще не студент Девман')


@router.callback_query(F.data.startswith('level-'))
async def get_level_handler(callback: CallbackQuery):
    # алгоритм :
    # удалить все команды, если какие-либо были ранее
    # по всем студентам сформировать id : время записи
    # организовать цикл по временным слотам ... и формировать новые группы
    logger.info(f'time handler - {callback.data}')
    student_level = callback.data.split('-')[-1]
    students = []
    await sync_to_async(StudyGroup.objects.all().delete)()
    async for student in Student.objects.all().order_by('preferred_time'):
        students.append(student)

    students = await sync_to_async(Student.objects.all)()
    student_id_time_id_qs = await sync_to_async(students.values_list)('id', 'preferred_time') #ключ-это id cтудента, значение - id времени слота
    student_id_time_id = await sync_to_async(dict)(student_id_time_id_qs)

    # цикл по слотам, исключая слот-время, которое "задаст ПМ сам", т.е. только по реальным указанным
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

    await bot.send_message(callback.from_user.id, 'Формирование закончено...')


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

    time_shudule_id = callback.data.split('_')[-1]
    if time_shudule_id=='Error':
        await bot.send_message(callback.from_user.id, "Свяжитесь с вашим ментором...")
    else:
        user_name = await sync_to_async(DevmanUser.objects.filter(telegram_id=callback.from_user.id).first)()
        start_time = await sync_to_async(StudyingTime.objects.filter(pk=time_shudule_id).first)()

        info = f'Студент создан {datetime.datetime.now()}.\nУказал удобное время {start_time}'
        # type = 'newbie' т.к. это уровень задаст ПМ в админке, пока по умолчанию
        student = Student(user=user_name, level='newbie', preferred_time=start_time, info=info)
        await sync_to_async(student.save)()
        await bot.send_message(callback.from_user.id, info)

