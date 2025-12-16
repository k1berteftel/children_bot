import asyncio

from aiogram.types import CallbackQuery, User, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.payments.create_payment import (get_yookassa_url)
from utils.payments.process_payment import wait_for_payment
from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, PaymentSG


rates = {
    'child': 'Покупка "Развивашек"',
    'recipe': 'Покупка рецептов',
    'both': '"Развивашки" + рецепты'
}


async def choose_payment_type_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
    rate = dialog_manager.dialog_data.get('rate')
    rate_name = '"Развивашки"' if rate == 'child' else ('Рецепты' if rate == 'recipe' else '"Развивашки" + рецепты')
    if rate == 'child':
        rate_description = 'Включает более 50 развивашек за месяц: 2 штуки в день'
    elif rate == 'recipe':
        rate_description = 'Включает более 50 рецептов за месяц: 2 штуки в день'
    else:
        rate_description = 'Включает более 55 рецептов и более 50 развивашек за месяц'
    cost = dialog_manager.dialog_data.get('cost')
    text = f'<blockquote> - Тариф: {rate_name}\n - ({rate_description})\n - Сумма к оплате: {cost}₽</blockquote>'
    return {
        'text': text
    }


async def payment_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    scheduler: AsyncIOScheduler = dialog_manager.middleware_data.get('scheduler')
    rate = dialog_manager.dialog_data.get('rate')
    cost = dialog_manager.dialog_data.get('cost')
    payment_type = clb.data.split('_')[0]

    if payment_type == 'card':
        payment = await get_yookassa_url(cost, rates.get('rate'))
        task = asyncio.create_task(
            wait_for_payment(
                payment_id=payment.get('id'),
                user_id=clb.from_user.id,
                bot=clb.bot,
                session=session,
                rate=rate,
                scheduler=scheduler,
                currency=cost,
                payment_type='card',
            )
        )
        for active_task in asyncio.all_tasks():
            if active_task.get_name() == f'process_payment_{clb.from_user.id}':
                active_task.cancel()
    else:
        pass
    dialog_manager.dialog_data['url'] = payment.get('url')
    await dialog_manager.switch_to(PaymentSG.process_payment)


async def process_payment_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    cost = dialog_manager.dialog_data.get('cost')
    url = dialog_manager.dialog_data.get('url')
    text = f'<blockquote> - Сумма к оплате: {cost}₽</blockquote>'
    return {
        'text': text,
        'url': url
    }


async def close_payment(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    name = f'process_payment_{clb.from_user.id}'
    for task in asyncio.all_tasks():
        if task.get_name() == name:
            task.cancel()
    await dialog_manager.switch_to(PaymentSG.choose_payment_type)
