from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    """
    class for set up state user
    """
    start: State = State()
    end: State = State()
    contact: State = State()
    geo: State = State()
    get_mail: State = State()
    mail_ver: State = State()
    save_json: State = State()
    search_json: State = State()
    send_paste: State = State()
