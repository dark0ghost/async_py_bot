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
    v_mail: State = State()
