from datetime import datetime, timedelta

from aiogram.types import CallbackQuery, User, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, PaymentSG, SubSG


config: Config = load_config()


async def menu_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    scheduler: AsyncIOScheduler = dialog_manager.middleware_data.get('scheduler')
    sub_data = await session.get_user_sub(event_from_user.id)
    rate_name = '"Развивашки"' if sub_data.rate == 'child' else \
        ('"Рецепты"' if sub_data.rate == 'recipe' else '"Развивашки" + "Рецепты"')
    sub_date = datetime.now() + timedelta(days=sub_data.sub_days)

    now = datetime.now()
    today_noon = now.replace(hour=12, minute=0, second=0, microsecond=0)
    next_date = today_noon if now < today_noon else today_noon + timedelta(days=1)
    text = (f'Тариф: <em>{rate_name}</em>\nПодписка до: <em>{sub_date.strftime("%d.%m.%Y")}</em>\n'
            f'Следующий выдача материала: {next_date.strftime("%d.%m.%Y %H:%M") if sub_data.active else "Заморожено"}'
            f'\nДней свободной заморозки: {sub_data.freeze_days}')
    admin = False
    admins = [*config.bot.admin_ids]
    admins.extend([admin.user_id for admin in await session.get_admins()])
    if event_from_user.id in admins:
        admin = True
    return {
        'text': text,
        'sub_button': "Заморозить подписку" if sub_data.active else "Разморозить подписку",
        'admin': admin
    }


async def sub_toggle(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    sub_data = await session.get_user_sub(clb.from_user.id)
    if sub_data.active and sub_data.freeze_days == 0:
        await clb.answer('К сожалению дни заморозки подписки подошли к концу')
        return
    await session.set_user_sub(clb.from_user.id, 'active', not sub_data.active)
    await dialog_manager.switch_to(SubSG.menu)

