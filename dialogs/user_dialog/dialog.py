from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.user_dialog import getters

from states.state_groups import startSG, adminSG

user_dialog = Dialog(
    Window(
        Const('Привет, мама! 💛 Добро пожаловать в пространство, где твою усталость понимают с полуслова, '
              'а помощь приходит в один тап.'),
        Column(
            Button(Const('Персональные "развивашки"'), id='child_form_switcher', on_click=getters.form_switcher),
            Button(Const('Индивидуальные рецепты'), id='recipe_form_switcher', on_click=getters.form_switcher),
            Start(Const('Админ панель'), id='admin', state=adminSG.start, when='admin')
        ),
        getter=getters.start_getter,
        state=startSG.start
    ),
    Window(
        Const('Как часто вам удаётся найти время для себя?🧖‍'),
        Column(
            SwitchTo(Const('А) Почти никогда'), id='choose_time_option_a', state=startSG.choose_sufficiency),
            SwitchTo(Const('Б) Иногда'), id='choose_time_option_b', state=startSG.choose_sufficiency),
            SwitchTo(Const('В) Достаточно часто'), id='choose_time_option_c', state=startSG.choose_sufficiency),
        ),
        Back(Const('⬅️Назад'), id='back'),
        state=startSG.choose_time
    ),
    Window(
        Const('Как вы считаете, ваш малыш получает достаточно развивающих игр и активности каждый день?🥁'),
        Column(
            SwitchTo(Const('А) Скорее нет'), id='choose_sufficiency_option_a', state=startSG.choose_cooking),
            SwitchTo(Const('Б) Иногда'), id='choose_sufficiency_option_b', state=startSG.choose_cooking),
            SwitchTo(Const('В) Да, у нас есть план развития'), id='choose_sufficiency_option_c', state=startSG.choose_cooking),
        ),
        Back(Const('⬅️Назад'), id='back_choose_time'),
        state=startSG.choose_sufficiency
    ),
    Window(
        Const('С приготовление еды для семьи у вас… 🍕'),
        Column(
            SwitchTo(Const('А) Постоянно стресс, не хватает идей'), id='choose_cooking_option_a', state=startSG.choose_ideas),
            SwitchTo(Const('Б) Иногда всё успеваю, иногда нет'), id='choose_cooking_option_b', state=startSG.choose_ideas),
            SwitchTo(Const('В) Всё продумано, знаю, что приготовить'), id='choose_cooking_option_c', state=startSG.choose_ideas),
        ),
        Back(Const('⬅️Назад'), id='back_choose_sufficiency'),
        state=startSG.choose_cooking
    ),
    Window(
        Const('Как часто вам хочется качественно поиграть с ребёнком, но не хватает идей? ⏰'),
        Column(
            SwitchTo(Const('А) Почти всегда'), id='choose_ideas_option_a', state=startSG.choose_planning),
            SwitchTo(Const('Б) Иногда'), id='choose_ideas_option_b', state=startSG.choose_planning),
            SwitchTo(Const('В) Редко'), id='choose_ideas_option_c', state=startSG.choose_planning),
        ),
        Back(Const('⬅️Назад'), id='back_choose_cooking'),
        state=startSG.choose_ideas
    ),
    Window(
        Const('Сколько времени вы тратите на планирование меню и покупок?🛍️ '),
        Column(
            SwitchTo(Const('А) Очень много, сил не хватает'), id='choose_planning_option_a', state=startSG.choose_usefulness),
            SwitchTo(Const('Б) Иногда успеваю спланировать'), id='choose_planning_option_b', state=startSG.choose_usefulness),
            SwitchTo(Const('В) У меня уже есть удобные схемы и рецепты'), id='choose_planning_option_c', state=startSG.choose_usefulness),
        ),
        Back(Const('⬅️Назад'), id='back_choose_ideas'),
        state=startSG.choose_planning
    ),
    Window(
        Const('Вам важно, чтобы игры развивали малыша не только весело, но и полезно? 🧸'),
        Column(
            SwitchTo(Const('А) Да, но сложно подобрать'), id='choose_usefulness_option_a', state=startSG.choose_readiness),
            SwitchTo(Const('Б) Иногда задумываюсь'), id='choose_usefulness_option_b', state=startSG.choose_readiness),
            SwitchTo(Const('В) Да, у нас есть своя система'), id='choose_usefulness_option_c', state=startSG.choose_readiness),
        ),
        Back(Const('⬅️Назад'), id='back_choose_planning'),
        state=startSG.choose_usefulness
    ),
    Window(
        Const('Хотели бы вы получать готовые решения, которые экономят время и силы, '
              'а ребёнку дают пользу и радость? ☀️'),
        Column(
            Button(Const('А) Да, очень'), id='choose_readiness_option_a', on_click=getters.choose_rate_switcher),
            Button(Const('Б) Возможно, интересно'), id='choose_readiness_option_b', on_click=getters.choose_rate_switcher),
            Button(Const('В) Уже пользуемся подобными решениями'), id='choose_readiness_option_c', on_click=getters.choose_rate_switcher),
        ),
        Back(Const('⬅️Назад'), id='back_choose_usefulness'),
        state=startSG.choose_readiness
    ),
    Window(
        Format('{text}'),
        Column(
            Button(Const('Купить "Развивашки"'), id='child_rate_choose', on_click=getters.rate_choose),
            Button(Const('🔥"Развивашки" + рецепты'), id='both_rate_choose', on_click=getters.rate_choose),
        ),
        getter=getters.child_rate_choose_getter,
        state=startSG.child_rate_choose
    ),
    Window(
        Format('{text}'),
        Column(
            Button(Const('Купить рецепты'), id='recipe_rate_choose', on_click=getters.rate_choose),
            Button(Const('🔥Рецепты + "Развивашки"'), id='both_rate_choose', on_click=getters.rate_choose),
        ),
        getter=getters.recipe_rate_choose_getter,
        state=startSG.recipe_rate_choose
    )
)