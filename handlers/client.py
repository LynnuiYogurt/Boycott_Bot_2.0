from aiogram import types, Dispatcher
from aiogram.dispatcher import filters

from create_bot import dp, bot
from keyboards import kb_client_global, kb_client_list
from settings import PROJECT_ROOT


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
	try:
		await message.answer(
			text='Напишіть назву товару або компанії і ми скажемо чи пішла вона з росії.\n\n'
				 'Бойкотуємо росію разом – не купляємо товари та послуги компаній, які платять податки в '
				 'бюджет '
				 'рф та фінансують війну.\n'
				 'P.S. Цей бот створений виключно на волонтерських засадах і з великим бажанням бойкотувати '
				 'окупанта '
				 'і всіх його прибічників. Ми не є державною установою чи комерційною організацією.'
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


async def check_by_name(message: types.Message):
	pass


@dp.callback_query_handler(filters.Regexp('(ua|left|stay|root)'))
async def ua_list(callback_query: types.CallbackQuery):
	if callback_query.data == 'ua':
		file_name = 'Українські компанії.txt'
	elif callback_query.data == 'left':
		file_name = 'Компанії, що покинули ринок.txt'
	elif callback_query.data == 'stay':
		file_name = 'Компанії, що залишися на ринку.txt'
	elif callback_query.data == 'root':
		file_name = 'Компанії з рашистським корінням.txt'
	else:
		file_name = None
	if file_name is not None:
		with open(f'{PROJECT_ROOT}/Lists of companies/{file_name}', 'rb') as file_list:
			await bot.send_document(callback_query.message.chat.id, document=file_list)

	await callback_query.answer()


def register_handlers_client(dispatcher: Dispatcher):
	dispatcher.register_message_handler(command_start, commands=['start', 'help'])
	dispatcher.register_message_handler(global_action)
