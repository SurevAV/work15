from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def make_keyboard(item, return_to_menu=None):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(*(InlineKeyboardButton(text, callback_data=data) for text, data in item))
    if not return_to_menu:
        return kb
    else:
        return add_inline_back_button(kb, back_callback_data=return_to_menu)


def add_inline_back_button(kb: InlineKeyboardMarkup,
                           back_callback_data: str,
                           button_label: str = "< Назад") -> InlineKeyboardMarkup:
    kb.add(InlineKeyboardButton("< Назад", callback_data=back_callback_data))
    return kb
