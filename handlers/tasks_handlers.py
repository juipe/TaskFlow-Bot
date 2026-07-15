from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F, types
from aiogram.types import Message

from data.task_database import create_task, get_tasks_for_user

from keyboards.task_keyboard import get_priority_keyboard

task_router = Router()


class Task(StatesGroup):
    task_title = State()
    task_description = State()
    task_priority = State()
    task_deadline = State()

class ShowTask:
    PRIORITY = 3
    TITLE = 1
    DESCRIPTION = 2
    DEADLINE = 5
    STATUS = 4

class Priority:
    HIGH = 1
    MEDIUM = 2
    LOW = 3

@task_router.message(F.text == "➕ Добавить задачу")
async def command_task_create_handler(message: Message, state: FSMContext):
    await message.answer("Введите название задачи:")
    await state.set_state(Task.task_title)


@task_router.message(F.text, Task.task_title)
async def state_task_title_handler(message: Message, state: FSMContext):
    await state.update_data(task_title=message.text)
    await message.answer("Введите описание:")
    await state.set_state(Task.task_description)


@task_router.message(F.text, Task.task_description)
async def state_task_description_handler(message: Message, state: FSMContext):
    await state.update_data(task_description=message.text)
    await message.answer("Выбери приоритет:", reply_markup=get_priority_keyboard())
    await state.set_state(Task.task_priority)


@task_router.callback_query(F.data.endswith("_priority"), Task.task_priority)
async def state_task_priority_handler(callback: types.CallbackQuery, state: FSMContext):
    priority_map = {
        "low_priority": Priority.LOW,
        "middle_priority": Priority.MEDIUM,
        "high_priority": Priority.HIGH,
    }

    await state.update_data(
        task_priority=priority_map[callback.data]
    )
    await callback.message.answer("Введите дедлайн в формате 12-07-2026: ")
    await callback.answer()
    await state.set_state(Task.task_deadline)


@task_router.message(F.text, Task.task_deadline)
async def state_task_deadline_handler(message: Message, state: FSMContext):
    await state.update_data(task_deadline=message.text)
    task_data = await state.get_data()

    title = task_data["task_title"]
    description = task_data["task_description"]
    priority = task_data["task_priority"]
    status = 0
    deadline = task_data["task_deadline"]
    user_id = message.from_user.id
    task = [title, description, priority, status, deadline, user_id]

    if await create_task(task):
        await message.answer("Успешно")
    else:
        await message.answer("Ошибка")
    await state.clear()

# Check tasks
@task_router.message(F.text == "📋 Мои задачи")
async def command_help_handler(message: Message):
    priority_text = {
    1: "🔴 High",
    2: "🟡 Medium",
    3: "🟢 Low",
}
    text_for_message = ""
    result = await get_tasks_for_user(message.from_user.id)
    if not result:
        await message.answer("You have no tasks")
        return
    for task in result:
        text_for_message += f"Priority: {priority_text[task[ShowTask.PRIORITY]]}\nTitle: {task[ShowTask.TITLE]}\nDescription: {task[ShowTask.DESCRIPTION]}\nDeadline: {task[ShowTask.DEADLINE]}\n"
        if task[ShowTask.STATUS] == 0:
            text_for_message += "In process\n"
        else:
            text_for_message += "Done\n"
        text_for_message += "====================\n"
    await message.answer(text_for_message)