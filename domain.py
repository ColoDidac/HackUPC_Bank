from utils import camel_to_snake


class ApiObject():
    def __repr__(self):
        if hasattr(self, 'id'):
            return "<{} {}>".format(self.__class__.__name__, self.id)
        return "<{}>".format(self.__class__.__name__)

    def __init__(self, data):
        self._data = data
        for key, value in data.items():
            if value:
                setattr(self, camel_to_snake(key), value)

    def to_json(self):
        return self.__dict__.pop('_data')


class Transaction(ApiObject):
    def __init__(self, data):
        super().__init__(data)
        self.category = Category(self.category)
        self.amount = TransactionAmount(self.amount)


class UpcomingTransaction(Transaction):
    def __init__(self, data):
        super().__init__(data)


class TransactionAmount(ApiObject):
    def __init__(self, data):
        super().__init__(data)


class Category(ApiObject):
    def __init__(self, data):
        super().__init__(data)
