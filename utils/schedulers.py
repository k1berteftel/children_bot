import asyncio
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram_dialog import DialogManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import child_data, recipe_data
from database.action_data_class import DataInteraction


async def send_messages(bot: Bot, session: DataInteraction, keyboard: InlineKeyboardMarkup|None, message: Message, **kwargs):
    users = await session.get_users()
    text = kwargs.get('text')
    caption = kwargs.get('caption')
    photo = kwargs.get('photo')
    video = kwargs.get('video')
    if text:
        for user in users:
            try:
                await bot.send_message(
                    chat_id=user.user_id,
                    text=text.format(name=user.name),
                    reply_markup=keyboard
                )
                if user.active == 0:
                    await session.set_active(user.user_id, 1)
            except Exception as err:
                print(err)
                await session.set_active(user.user_id, 0)
    elif caption:
        if photo:
            for user in users:
                try:
                    await bot.send_photo(
                        chat_id=user.user_id,
                        photo=photo,
                        caption=caption.format(name=user.name),
                        reply_markup=keyboard
                    )
                    if user.active == 0:
                        await session.set_active(user.user_id, 1)
                except Exception as err:
                    print(err)
                    await session.set_active(user.user_id, 0)
        else:
            for user in users:
                try:
                    await bot.send_video(
                        chat_id=user.user_id,
                        video=video,
                        caption=caption.format(name=user.name),
                        reply_markup=keyboard
                    )
                    if user.active == 0:
                        await session.set_active(user.user_id, 1)
                except Exception as err:
                    print(err)
                    await session.set_active(user.user_id, 0)


async def polling_user_sub(user_id: int, bot: Bot, session: DataInteraction, scheduler: AsyncIOScheduler):
    sub_data = await session.get_user_sub(user_id)
    if not sub_data.active:
        if sub_data.freeze_days == 1:
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text='🔔<b>Последний день</b> заморозки подписки подошел к концу, с завтрашнего дня вы '
                         'будете так же получать полезные материалы по вашему тарифу подписку'
                )
            except Exception:
                await session.set_active(user_id, 0)
            await session.update_user_sub(user_id, 'active', True)
        await session.update_user_sub(user_id, 'freeze_days', -1)
        return
    if sub_data.sub_days == 0:
        job = scheduler.get_job(f'polling_sub_{user_id}')
        if job:
            job.remove()
        await session.del_user_sub(user_id)
        return
    if sub_data.rate == 'child':
        try:
            await bot.send_message(
                chat_id=user_id,
                text=child_data.get(sub_data.days_count)
            )
        except Exception:
            await session.set_active(user_id, 0)
    elif sub_data.rate == 'recipe':
        try:
            await bot.send_message(
                chat_id=user_id,
                text=recipe_data.get(sub_data.days_count)
            )
        except Exception:
            await session.set_active(user_id, 0)
    else:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=child_data.get(sub_data.days_count)
            )
        except Exception:
            ...
        try:
            await bot.send_message(
                chat_id=user_id,
                text=recipe_data.get(sub_data.days_count)
            )
        except Exception:
            await session.set_active(user_id, 0)
    await session.update_user_sub(user_id, 'sub_days', -1)
    await session.update_user_sub(user_id, 'days_count', 1)


