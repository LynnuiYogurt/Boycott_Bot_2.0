from aiogram import types, Dispatcher
from aiogram.dispatcher import filters

from create_bot import dp, bot
from keyboards import kb_client_global, kb_client_list, client_kb, cb_inline

from aiogram.dispatcher.filters import Text, Command
from aiogram.types import ReplyKeyboardRemove, InputFile
from aiogram.types.base import TelegramObject

from settings import PROJECT_ROOT


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
	try:
		await message.answer(
			text='Напишіть назву товару або компанії і ми скажемо чи пішла вона з росії.\n\n'
				 'Бойкотуємо росію разом – не купляємо товари та послуги компаній, які платять податки в бюджет рф та фінансують війну.\n'
				 'P.S. Цей бот створений виключно на волонтерських засадах і з великим бажанням бойкотувати окупанта і всіх його прибічників. Ми не є державною установою чи комерційною організацією.'
				 ' Вся інформація береться з відкритих джерел і несе суто інформаційний характер.'
				 'Все буде Україна 🇺🇦❤️',
			reply_markup=kb_client_global)
	except Exception as e:
		print(e)


async def global_action(message: types.Message):
	try:
		match message.text:
			case 'Перевірка за назвою':
				await message.reply('Введіть назву бренду / компанії')
			case 'Списки компаній':
				await message.reply(text='Які компанії вас цікавлять? 🤔', reply_markup=kb_client_list)
			case 'Перевірка за фото':
				await message.reply('Відправте фото з назвою')
	except Exception as e:
		print(e)


async def chek_by_name(message: types.Message):
	pass


@dp.callback_query_handler(cb_inline.filter(action='myact'))
async def ua_list(callback_query: types.CallbackQuery):
			with  open(f'{PROJECT_ROOT}/Lists of companies/Українські компанії.txt','rb') as ua_list:
				await bot.send_document(callback_query.message.chat.id, document=ua_list)@dp.callback_query_handler(cb_inline.filter(action='myact'))

async def left_list(callback_query: types.CallbackQuery):
			with  open(f'{PROJECT_ROOT}/Lists of companies/Компанії, що покинули ринок.txt','rb') as left_list:
				await bot.send_document(callback_query.message.chat.id, document=left_list)@dp.callback_query_handler(cb_inline.filter(action='myact'))

async def stay_list(callback_query: types.CallbackQuery):
			with  open(f'{PROJECT_ROOT}/Lists of companies/Українські компанії.txt','rb') as ua_list:
				await bot.send_document(callback_query.message.chat.id, document=ua_list)


async def root_list(callback_query: types.CallbackQuery):
	with  open(f'{PROJECT_ROOT}/Lists of companies/Українські компанії.txt', 'rb') as ua_list:
		await bot.send_document(callback_query.message.chat.id, document=ua_list)



def register_handlers_client(dp: Dispatcher):
	dp.register_message_handler(command_start, commands=['start', 'help'])
	dp.register_message_handler(global_action)
	dp.register_message_handler(ua_list, commands=['ua_list'])
