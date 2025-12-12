from datetime import datetime, timedelta

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.schedulers import polling_user_sub
from database.action_data_class import DataInteraction


async def start_schedulers(bot: Bot, session: DataInteraction, scheduler: AsyncIOScheduler):
    for user in await session.get_users():
        if user.sub:
            #await polling_user_sub(user.user_id, bot, session, scheduler)
            job_id = f'polling_sub_{user.user_id}'
            scheduler.add_job(
                polling_user_sub,
                'cron',
                args=[user.user_id, bot, session, scheduler],
                id=job_id,
                hour=12,
                minute=0
            )
