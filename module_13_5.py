from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = "7280212963:AAFNyiTmnSPXEbtJpDuPS8zG1jl_pgK2pu4"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


def create_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_calculate = KeyboardButton('Рассчитать')
    button_info = KeyboardButton('Информация')
    keyboard.add(button_calculate, button_info)  # добавляем сразу две кнопки
    return keyboard


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = create_keyboard()
    await message.answer("Нажмите 'Рассчитать' для начала.", reply_markup=keyboard)


@dp.message_handler(text='Рассчитать')
async def set_age(message: types.Message, state: FSMContext):
    await UserState.age.set()
    await message.answer("Введите ваш возраст:")


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.answer("Введите свой рост:")


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.answer("Введите свой вес:")


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))

    calories = 66 + (13.75 * weight) + (5 * growth) - (6.75 * age)

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал.")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)