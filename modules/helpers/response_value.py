class ResponseValue:
    value = None
    error = None

    def set_value(self, value):
        self.value = value
        return self

    def set_error(self, error):
        self.error = error
        return self


class ResponseError:
    id = ""
    text = ""

    def __init__(self, id, text):
        self.id = id
        self.text = text
