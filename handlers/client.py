from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import threading
from create_bot import dp, bot
from keyboards import kb_client_global, kb_client_list, CompanySearchOptions
from models import DBSession, CompanyName, Company
from settings import PROJECT_ROOT
import logging
from fuzzywuzzy import fuzz


class CheckByName(StatesGroup):
	options = []
	waiting_for_company_selection = State()
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
		if message.text == 'Перевірка за назвою':
			await message.reply('Введіть назву бренду / компанії')
		elif message.text == 'Списки компаній':
			await message.reply(text='Які компанії вас цікавлять? 🤔', reply_markup=kb_client_list)
		elif message.text == 'Перевірка за фото':
			await message.reply('Відправте фото з назвою')
	except Exception as e:
		print(e)


@dp.message_handler(filters.Regexp('Перевірка за назвою'))
async def check_by_name(message: types.Message):
	await message.reply('Введіть назву бренду / компанії')
	await CheckByName.waiting_for_name.set()


@dp.message_handler(state=CheckByName.waiting_for_name)
async def process_check_name(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['company_name'] = message.text

	try:
		db = DBSession
		company_name = data['company_name']

		# Check if company_name is already registered in the database
		existing_company = db.query(CompanyName).filter_by(name=company_name).first()
		if existing_company:
			company_id = existing_company.company_id
		else:
			# If not, try to find a matching company name in the database
			companies = db.query(CompanyName).all()
			matching_companies = []
			for company in companies:
				ratio = fuzz.ratio(company.name.lower(), company_name.lower())
				if ratio >= 80:  # threshold for a "good enough" match
					matching_companies.append(company)
			if len(matching_companies) == 0:
				await message.reply(f"Компанію '{company_name}' не знайдено", reply_markup=kb_client_global)
				return
			elif len(matching_companies) == 1:
				company_id = matching_companies[0].company_id
			else:
				# If multiple matching companies were found, ask the user to select one
				search_options = CompanySearchOptions(matching_companies)
				keyboard = search_options.get_inline_keyboard()
				reply_text = f"Знайдено декілька компаній, виберіть будь ласка потрібну:"
				await message.reply(reply_text, reply_markup=keyboard)
				async with state.proxy() as data:
					data['matching_companies'] = matching_companies
				await CheckByName.waiting_for_company_selection.set()
				return

		# If we found a company ID, get the description and reply to the user
		company_obj = db.query(Company).filter_by(id=company_id).first()
		if company_obj is None:
			await message.reply(f"Для компанії '{company_name}' не знайдено опис", reply_markup=kb_client_global)
		else:
			await message.reply(f'{company_name}: {company_obj.description}', reply_markup=kb_client_global)

	except Exception as e:
		await message.reply(f"Під час пошуку компанії сталася помилка: {e}", reply_markup=kb_client_global)
	finally:
		CheckByName.options.clear()
		await state.finish()


@dp.message_handler(state=CheckByName.waiting_for_company_selection)
async def process_company_selection(message: types.Message, state: FSMContext):
	company_id_to_name = {}
	async with state.proxy() as data:
		company_id = data['company_id']
		company_name = data['company_name']
		company_id_to_name[data[company_id]] = data[company_name]
	selected_company_id = int(message.text)
	# Ensure that the user has selected a valid company
	if selected_company_id not in company_id_to_name:
		await message.answer("Помилка, оберіть компанію зі списку")
		return
	# Get the name of the selected company
	selected_company_name = company_id_to_name[selected_company_id]
	# Get the description of the selected company
	try:
		description = process_check_name(selected_company_id)
	except:
		await message.answer("Помилка при спробі дістати опис")
		return
	# Send the company description back to the user
	await message.answer(f"{selected_company_name}: {description}")
	# Clear the conversation state
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
