from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Cancel
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.payment_dialog import getters

from states.state_groups import startSG, PaymentSG


payment_dialog = Dialog(
    Window(
        Const('🏦<b>Выберите способ оплаты</b>\n'),
        Format('{text}'),
        Column(
            #Button(Const('💲Крипта'), id='crypto_payment_choose', on_click=getters.payment_choose),
            Button(Const('💳Карта'), id='card_payment_choose', on_click=getters.payment_choose),
        ),
        Cancel(Const('◀️Назад'), id='close_dialog'),
        getter=getters.choose_payment_type_getter,
        state=PaymentSG.choose_payment_type
    ),
    Window(
        Const('<b>⌛️Ожидание оплаты</b>'),
        Format('{text}'),
        Column(
            Url(Const('🔗Оплатить'), id='url', url=Format('{url}')),
        ),
        Button(Const('◀️Назад'), id='back', on_click=getters.close_payment),
        getter=getters.process_payment_getter,
        state=PaymentSG.process_payment
    ),
)