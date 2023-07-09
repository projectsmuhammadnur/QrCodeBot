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


@dp.message_handler(commands="create_qr")
async def delete_qr(msg : Message):
    async for i in async_range(10051):
        await QrCode.create(id=i, active=False)


@dp.message_handler(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext):
    await msg.answer(
        text=f"<b>Assalomu aleykum hurmatli {msg.from_user.full_name}👋️</b>",
        parse_mode="HTML")
    deep_user = msg.get_args()
    qr = await QrCode.get(int(deep_user))
    if qr.active is True:
        await msg.answer(text=f"<b>Ishlatilgan QrCode!</b>", parse_mode="HTML")

    else:
        await state.set_state("name")
        async with state.proxy() as data:
            data["qrcode_id"] = qr.id
        await QrCode.update(int(qr.id), active=True)
        await msg.answer(text=f"<b>Ismingiz</b>", parse_mode="HTML")



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
    await User.create(user_id=str(msg.from_user.id), fullname=data['name'], phone=data['phone'],qrcode_id=data['qrcode_id'])
    await state.finish()
