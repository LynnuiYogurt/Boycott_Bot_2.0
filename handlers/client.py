from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import threading
from create_bot import dp, bot
from keyboards import kb_client_global, kb_client_list
from models import DBSession, CompanyName, Company
from settings import PROJECT_ROOT


class CheckByName(StatesGroup):
	waiting_for_name = State()


class SendList(StatesGroup):
	waiting_for_company = State()


class CheckByPhoto(StatesGroup):
	waiting_for_photo = State()


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


@dp.message_handler(filters.Regexp('Перевірка за назвою'))
async def check_by_name(message: types.Message):
	await message.reply('Введіть назву бренду / компанії')
	await CheckByName.waiting_for_name.set()


@dp.message_handler(state=CheckByName.waiting_for_name)
async def process_check_name(message: types.Message, state: FSMContext):
	try:
		company_name = message.text.lower()
		session = DBSession
		company = session.query(Company).join(CompanyName).filter(CompanyName.name.ilike(f'%{company_name}%')).first()
		company_id = company.id
		list_of_names = session.query(CompanyName).filter_by(company_id=company_id).all()
		name = ''
		for it in list_of_names:
			if company_name.lower() in it.name.lower(): name = it.name
		if company:
			description = company.description
			await message.reply(f'{name}:{description}', reply_markup=kb_client_global)
		# else:
		# 	await message.reply(f"Компанію: {company_name} не знайдено ", reply_markup=kb_client_global)
		await state.finish()
	except AttributeError:
		await message.reply(f"Компанію: {company_name} не знайдено ", reply_markup=kb_client_global)
		await state.finish()

@dp.message_handler(filters.Regexp('Списки компаній'))
async def send_list(message: types.Message):
	await message.reply(text='Які компанії вас цікавлять? 🤔', reply_markup=kb_client_list)
	await SendList.waiting_for_company.set()


@dp.callback_query_handler(filters.Regexp('(ua|left|stay|root)'), state=SendList.waiting_for_company)
async def process_send_list(callback_query: types.CallbackQuery, state: FSMContext):
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
		with open(f'{PROJECT_ROOT}/List_of_companies/{file_name}', 'rb') as file_list:
			await bot.send_document(callback_query.message.chat.id, document=file_list)
	await callback_query.answer()
	await state.finish()


@dp.message_handler(filters.Regexp('Перевірка за фото'))
async def check_by_name(message: types.Message):
	await message.reply('Буде додано пізніше')
