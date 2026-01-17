import random

from aiogram.types import CallbackQuery, User, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput

from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, PaymentSG


config: Config = load_config()


async def start_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    admin = False
    admins = [*config.bot.admin_ids]
    admins.extend([admin.user_id for admin in await session.get_admins()])
    if event_from_user.id in admins:
        admin = True
    return {'admin': admin}


async def form_switcher(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['mode'] = clb.data.split('_')[0]
    await dialog_manager.switch_to(startSG.choose_time)


async def choose_rate_switcher(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    mode = dialog_manager.dialog_data.get('mode')
    if mode == 'child':
        await dialog_manager.switch_to(startSG.child_rate_choose)
    else:
        await dialog_manager.switch_to(startSG.recipe_rate_choose)


async def child_rate_choose_getter(dialog_manager: DialogManager, **kwargs):
    text = (f'<b>Спасибо за ваши ответы!</b> На основе анкеты я составил небольшой портрет вашей ситуации '
            f'с развивающими играми.\n\n<b>Ваш результат готов!</b>\n💡<b>Уровень игрового ресурса для развития малыша: '
            f'{random.randint(35, 65)}%.</b>\n\n<blockquote>Этот показатель говорит о том, что у вас есть большое '
            f'желание дарить ребенку полезные впечатления, но часто не хватает готовых решений и системы, '
            f'чтобы превратить это в ежедневную лёгкую привычку без поисков и подготовки.</blockquote>\n\n'
            f'<b>🧩Позвольте представить решение — тариф <u>«Развивашки» от логопеда</u>!</b>\nКаждый день вы будете получать '
            f'готовую игру, которая:\n • <b>Развивает конкретный навык</b> (логику, речь, моторику) через веселье.\n'
            f' • <b>Не требует долгой подготовки</b> — материалы есть в каждом доме.\n • <b>Дарит вам уверенность</b>, '
            f'что время с ребенком проходит с максимальной пользой и радостью.\n\nЭто ваш шанс заменить «во что бы '
            f'поиграть?» на готовый план развития, освободив время для себя.\n\n<blockquote>🍽 Обратите внимание: '
            f'Часто мамы, которые берут игры, вскоре спрашивают и про рецепты, чтобы выстроить весь день ребенка '
            f'гармонично. Объединенный тариф «Всё включено» (Развивашки от логопеда + Меню) помогает создать полноценную '
            f'развивающую среду и экономит максимум сил</blockquote>')
    return {
        'text': text
    }


async def recipe_rate_choose_getter(dialog_manager: DialogManager, **kwargs):
    text = ('<b>Спасибо за ваши ответы!</b> На основе анкеты я составил небольшой портрет вашей ситуации.\n\n'
            f'<b>Ваш результат готов!</b>\n💡<b>Уровень кулинарной ресурсности: '
            f'{random.randint(35, 65)}%.</b>\n\n<blockquote>Этот показатель отражает, насколько легко вам сейчас даются '
            f'регулярные развивающие игры. Часто забота о быте и планировании меню забирает те силы и время, '
            f'которые хотелось бы направить на общение и развитие ребенка.</blockquote>\n\n<b>🍕 Идеальное решение — начать с '
            f'тарифа «Меню на месяц»!</b>\nПорядок в вопросах питания создает фундамент для всего остального. '
            f'Подписка даст вам:\n • <b>Ежедневный простой рецепт</b>, который понравится всей семье.\n • <b>Четкий '
            f'список покупок</b>, чтобы не тратить время в магазине.\n • <b>Освободившиеся часы и энергию</b>, '
            f'которые можно смело посвятить играм и развитию.\nНаведите порядок на кухне — и вы удивитесь, сколько '
            f'ресурсов откроется для всего остального!\n\n<blockquote>🎨 Обратите внимание: Когда готовка перестанет '
            f'быть рутиной, вы сможете с новыми силами взяться за развивающие игры. Объединенный тариф «Всё включено» '
            f'(Меню + Развивашки от логопеда) — это полный цикл заботы: полезная еда для энергии и готовые игры для развития. '
            f'Это самый выгодный и системный подход.</blockquote>')
    return {
        'text': text
    }


async def rate_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    rate = clb.data.split('_')[0]
    cost = 299 if rate in ['child', 'recipe'] else 499
    data = {
        'rate': rate,
        'cost': cost
    }
    await dialog_manager.start(PaymentSG.choose_payment_type, data=data)
