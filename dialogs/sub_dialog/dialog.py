from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.sub_dialog import getters

from states.state_groups import startSG, adminSG, SubSG


sub_dialog = Dialog(
    Window(
        Format('<b>Сведения о вашей подписке:</b>\n<blockquote>{text}</blockquote>'),
        Column(
            Button(Format('{sub_button}'), id='freeze_sub_toggle', on_click=getters.sub_toggle),
            Start(Const('Админ панель'), id='admin', state=adminSG.start, when='admin')
        ),
        getter=getters.menu_getter,
        state=SubSG.menu
    ),
)