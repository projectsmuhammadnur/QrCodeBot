from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from bot.dispatcher import dp
from db.model import Qrcodes, Users


@dp.message_handler(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext):
    await msg.answer(
        text=f"<b>Assalomu aleykum hurmatli {msg.from_user.full_name}👋️</b>",
        parse_mode="HTML")
    deep_user = msg.get_args()
    qr = Qrcodes().select(int(deep_user))
    if qr.active is True:
        await msg.answer(text=f"<b>Ishlatilgan QrCode!</b>", parse_mode="HTML")
        return
    else:
        await state.set_state("name")
        async with state.proxy() as data:
            data["qrcode_id"] = qr.id
        Qrcodes().update(qrcode_id=qr.id, active=True)
        await msg.answer(text=f"<b>Ismingiz</b>", parse_mode="HTML")
        return


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
    Users().insert_into(user_id=str(msg.from_user.id), name=data['name'], phone=data['phone'],
                        qrcode_id=data['qrcode_id'])
    await state.finish()
