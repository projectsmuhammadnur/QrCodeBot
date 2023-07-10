import asyncio
import csv
import os
from random import randint
from time import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ContentType
from aiogram.utils.exceptions import ChatNotFound

from bot.dispatcher import dp, bot
from db.model import QrCode, User


admins = ["abdusamad_nodirovich", "Dilshod_Absaitov", "ruz_9003"]

async def async_range(count):
    for i in range(1, count):
        yield (i)
        await asyncio.sleep(0.0)


@dp.message_handler(commands="restart_qr")
async def delete_qr(msg: Message):
    await QrCode.delete()

    async for i in async_range(10051):
        await QrCode.create(id=i, active=False)


@dp.message_handler(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext):
    deep_user = msg.get_args()
    if deep_user != "":
        qr = await QrCode.get(int(deep_user))

        if qr[0].active == True:
            await msg.answer(text=f"<b>Bu QR-code ishlatilgan!</b>", parse_mode="HTML")
            await state.finish()
        else:
            await msg.answer_photo(photo="https://telegra.ph/file/d2a51afb3fab6e7c0c95e.png",
                                   caption=f"""<b>Assalomu aleykum hurmatli mijoz!
Ishtirokchiga aylanish uchun ISM SHARIFINGIZNI va TELAFON RAQAMINGIZNI kiriting!
            </b>""",
                                   parse_mode="HTML")
            await state.set_state("name")
            async with state.proxy() as data:
                data["qrcode_id"] = deep_user
            await QrCode.update(int(deep_user), active=True)
            await msg.answer(text=f"<b>Ro'yhatdan o'tishni boshlimiz 😊</b>", parse_mode="HTML")
            await msg.answer(text=f"<b>Ismingizni kiriting ✍️:</b>", parse_mode="HTML")


@dp.message_handler(state='name')
async def name_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    k = KeyboardButton(text="TELEFON RAQAM📲", request_contact=True)
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb_client.add(k)
    await state.set_state("phone")
    await msg.answer(text=f"<b>Telefon raqamingiz:</b>", parse_mode="HTML", reply_markup=kb_client)


@dp.message_handler(state='phone', content_types='contact')
async def phone_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = msg.contact.phone_number
    await msg.answer(text=f"""<b>Siz BONVI Aksiyasi ishtirokchisi bo’dingiz! Aksiya tugagunga qadar QR-kodingizni tashlab yubormang!

Aksiya 25 sentabr kuni yakunlanadi!
30 sentabr kuni jonli efirda o’ynaladi, aloqada bo’ling! OMAD!</b>""", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    await User.create(chat_id=str(msg.from_user.id), fullname=data['name'], phone_number=data['phone'],
                      qr_code_id=data['qrcode_id'])
    await state.finish()


async def send_csv(chat_id, file_path):
    with open(file_path+'.csv', 'rb') as file:
        await bot.send_document(chat_id, document=file)
    os.remove(file_path + '.csv')


@dp.message_handler(commands='users')
async def users_handler(msg: types.Message):
    if msg.from_user.username in admins:
        file_path = str(randint(10000, 99999))
        users = await User.get_all()
        with open(file_path+'.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file, delimiter=',')
            csv_writer.writerow(['ID', 'Chat ID', 'FullName', "Phone Number", 'QRCode ID', 'Created at'])
            for i in users:
                csv_writer.writerow(
                    [i[0].id, i[0].chat_id, i[0].fullname, i[0].phone_number, i[0].qr_code_id, i[0].created_at])
        await send_csv(msg.chat.id, file_path)


@dp.message_handler(commands='advert')
async def advert_handler(msg: types.Message, state: FSMContext):
    await state.set_state('advert')
    await msg.answer("<b>Habarni yuboring!</b>", parse_mode="HTML")


@dp.message_handler(state='advert', content_types=ContentType.ANY)
async def get_user_id_for_send_to_user(msg: Message, state: FSMContext):
    await state.finish()
    users = await User.get_all()
    succ = 0
    fail = 0
    text = "*Session Started:*"
    session = await msg.bot.send_message(msg.chat.id, text, 'MarkdownV2')
    for user in users:
        try:
            await msg.copy_to(user[0].chat_id, msg.caption, caption_entities=msg.caption_entities,
                              reply_markup=msg.reply_markup)
            await sleep(0.05)
            succ += 1
        except ChatNotFound:
            pass
            try:
                pass
            except Exception:
                pass
            fail += 1
        except Exception:
            pass
            fail += 1
    else:
        await session.delete()
        await msg.answer(f"Habar *{succ}*ta userga tarqatildi✅\n*{fail}*ta user botni bloklagan❌", 'MarkdownV2')