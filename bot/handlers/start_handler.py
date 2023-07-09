import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from bot.dispatcher import dp
from db.model import QrCode, User

async def async_range(count):
    for i in range(1 , count):
        yield(i)
        await asyncio.sleep(0.0)


@dp.message_handler(commands="restart_qr")
async def delete_qr(msg : Message):
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
    await state.set_state("phone")
    await msg.answer(text=f"<b>Telefon raqamingiz:</b>", parse_mode="HTML")


@dp.message_handler(state='phone')
async def phone_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = msg.text
    await msg.answer(text=f"<b>Qabul qilindi!</b>", parse_mode="HTML")
    await User.create(chat_id=str(msg.from_user.id), fullname=data['name'], phone_number=data['phone'],qr_code_id=data['qrcode_id'])
    await state.finish()
