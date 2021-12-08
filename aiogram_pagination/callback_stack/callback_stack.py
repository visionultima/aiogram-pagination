from ..utils.callback_stack_factory import CallbackStackFactory


class CallbackStack:
    def __init__(self, callback_data: dict, callback_factory: CallbackStackFactory):
        self.separator = '¦'
        self.callback_factory = callback_factory
        self.callback_data = callback_data
        self.validate_callback_data()

    def validate_callback_data(self) -> None:
        if '@' in self.callback_data:
            self.callback_data.pop('@')

    def generate_previous_callback_data(self) -> list:
        return list(filter(None, self.callback_data.pop('previous').split(self.separator)))

    def get_complete_string_callback_data(
            self,
            callback_data: dict,
            callback_factory: CallbackStackFactory,
            previous_callback_data: list) -> str:

        try:
            return callback_factory.new(
                **callback_data,
                previous=self.get_string_previous_callback_data(previous_callback_data)
            )
        except ValueError:
            if not previous_callback_data:
                raise ValueError
            self.get_complete_string_callback_data(
                callback_data,
                callback_factory,
                previous_callback_data[1:]
            )

    def get_string_previous_callback_data(self, previous_callback_data: list) -> str:
        return self.separator.join(previous_callback_data)

    def get_string_callback_data(self) -> str:
        return self.callback_factory.new(
            **self.callback_data,
            previous=str())
