class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet:
    def __init__(self, typ):
        self.typ = typ
        self.cmd = 'GET'


class EventSet:
    def __init__(self, val):
        self.val = val
        self.cmd = "SET"


class NullHandler:
    """Нулевое звено цепочки"""

    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.cmd == "SET":
            if isinstance(event.val, int):
                obj.integer_field = event.val
                return

        elif event.cmd == "GET":
            if event.typ is int:
                return obj.integer_field

        return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.cmd == "SET":
            if isinstance(event.val, float):
                obj.float_field = event.val
                return

        elif event.cmd == "GET":
            if event.typ is float:
                return obj.float_field

        return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.cmd == "SET":
            if isinstance(event.val, str):
                obj.string_field = event.val
                return

        elif event.cmd == "GET":
            if event.typ is str:
                return obj.string_field

        return super().handle(obj, event)


# obj = SomeObject()
# obj.integer_field = 42
# obj.float_field = 3.14
# obj.string_field = "some text"
# chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
# print(chain.handle(obj, EventGet(int)))
# print(chain.handle(obj, EventGet(float)))
# print(chain.handle(obj, EventGet(str)))
# chain.handle(obj, EventSet(100))
# print(chain.handle(obj, EventGet(int)))
# chain.handle(obj, EventSet(0.5))
# print(chain.handle(obj, EventGet(float)))
# chain.handle(obj, EventSet('new text'))
# print(chain.handle(obj, EventGet(str)))
