from aiogram_pagination.utils.callback_stack_factory import CallbackStackFactory


class Callback:
    def __init__(self, factory: CallbackStackFactory, data: dict = None, query: str = None):

        self.factory = factory
        if not (data or query):
            raise ValueError

        self.data = data if data else self._get_callback_data()
        self._validate_callback_data()
        self.query = query if query else self._get_callback_query()

    def _get_callback_query(self):
        return self.factory.new(**self.data)

    def _get_callback_data(self):
        return self.factory.parse(self.query)

    def _validate_callback_data(self) -> None:
        if '@' in self.data:
            self.data.pop('@')


class PreviousCallback(Callback):

    def __init__(self, factory: CallbackStackFactory, data: dict = None, query: str = None):
        super().__init__(factory, data, query)
        self.separator = '¦'
        self.previous_callback_data = self.get_previous_callback_data()

    def get_previous_callback_data(self) -> list[str]:
        return list(filter(None, self.data['previous'].split(self.separator)))

    def get_previous_callback_queries(self) -> str:
        return self.separator.join(self.previous_callback_data)

    def get_current_callback_query(self) -> str:
        return self.factory.new(**self.get_current_callback_data())

    def get_current_callback_data(self) -> dict:
        callback_data = self.data.copy()
        callback_data['previous'] = ''
        return callback_data

    @staticmethod
    def validate_callback_query(current_callback_query, previous_callback_queries):
        callback_query = f'{current_callback_query}{previous_callback_queries}'
        while len(callback_query) > 64:
            previous_callback_queries = previous_callback_queries[1:]
            callback_query = f'{current_callback_query}{previous_callback_queries}'
        return callback_query
