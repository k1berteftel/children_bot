from aiogram.fsm.state import State, StatesGroup

# Обычная группа состояний


class startSG(StatesGroup):
    start = State()

    choose_time = State()

    choose_sufficiency = State()

    choose_cooking = State()

    choose_ideas = State()

    choose_planning = State()

    choose_usefulness = State()

    choose_readiness = State()

    child_rate_choose = State()
    recipe_rate_choose = State()


class adminSG(StatesGroup):
    start = State()

    get_mail = State()
    get_time = State()
    get_keyboard = State()
    confirm_mail = State()

    deeplinks_menu = State()
    get_deeplink_name = State()
    deeplink_menu = State()

    admin_menu = State()
    admin_del = State()
    admin_add = State()

    get_user_data = State()
    choose_rate = State()

    audience_choose = State()


class PaymentSG(StatesGroup):
    choose_payment_type = State()
    process_payment = State()


class SubSG(StatesGroup):
    menu = State()