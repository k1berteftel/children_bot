import asyncio
from asyncio import TimeoutError
from typing import Literal
from datetime import datetime, date, timedelta, time

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.schedulers import polling_user_sub
from utils.payments.create_payment import check_yookassa_payment
from database.action_data_class import DataInteraction
from config_data.config import Config, load_config


config: Config = load_config()


async def wait_for_payment(
        payment_id,
        user_id: int,
        bot: Bot,
        session: DataInteraction,
        scheduler: AsyncIOScheduler,
        currency: int,
        rate: str,
        payment_type: Literal['card'],
        timeout: int = 60 * 15,
        check_interval: int = 6
):
    """
    Ожидает оплаты в фоне. Завершается при оплате или по таймауту.
    """
    try:
        await asyncio.wait_for(_poll_payment(payment_id, user_id, currency, bot, session, scheduler, rate, payment_type, check_interval),
                               timeout=timeout)

    except TimeoutError:
        print(f"Платёж {payment_id} истёк (таймаут)")

    except Exception as e:
        print(f"Ошибка в фоновом ожидании платежа {payment_id}: {e}")


async def _poll_payment(payment_id, user_id: int, currency: int, bot: Bot, session: DataInteraction, scheduler: AsyncIOScheduler, rate: str, payment_type: str, interval: int):
    """
    Цикл опроса статуса платежа.
    Завершается, когда платёж оплачен.
    """
    while True:
        if payment_type == 'card':
            status = await check_yookassa_payment(payment_id)
        else:
            status = False
        if status:
            await bot.send_message(
                chat_id=user_id,
                text='✅Оплата прошла успешно'
            )
            await execute_rate(user_id, currency, rate, payment_type, bot, session, scheduler)
            break
        await asyncio.sleep(interval)


async def execute_rate(user_id: int, currency: int, rate: str, payment_type: str, bot: Bot, session: DataInteraction, scheduler: AsyncIOScheduler):
    sub_days = 30
    user = await session.get_user(user_id)
    if user.join:
        await session.update_deeplink_earn(user.join, currency)
    await session.add_user_sub(user_id, sub_days, rate)

    await session.update_static('sum', currency)
    await session.update_static('buys', 1)
    if rate == 'child':
        await session.update_static('child_buys', 1)
    elif rate == 'recipe':
        await session.update_static('recipe_buys', 1)

    rate_name = 'Развивашки' if rate == 'child' else ('Рецепты' if rate == 'recipe' else 'Развивашки + Рецепты')
    try:
        await bot.send_message(
            chat_id=user_id,
            text=f'Вы успешно приобрели тариф "{rate_name}", с завтрашнего дня в 12:00 по московскому времени вы '
                 f'будете ежедневно получать полезные материалы'
        )
    except Exception:
        ...
    job_id = f'polling_sub_{user_id}'
    job = scheduler.get_job(job_id)
    if job:
        job.remove()

    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
    scheduler.add_job(
        polling_user_sub,
        'cron',
        args=[user_id, bot, session, scheduler],
        id=job_id,
        hour=12,
        minute=0,
        next_run_time=tomorrow
    )

