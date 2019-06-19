# Задание по программированию: Реализовать Chain of Responsibility

Вам дан объект класса SomeObject, содержащего три поля: __integer_field__, __float_field__ и __string_field__:

```python
class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""
```

Необходимо реализовать:

* __EventGet(<type>)__ создаёт событие получения данных соответствующего типа
* __EventSet(<value>)__ создаёт событие изменения поля типа __type(<value>)__

Необходимо реализовать классы __NullHandler__, __IntHandler__, __FloatHandler__, __StrHandler__ так, чтобы можно было создать цепочку:

```python
chain = IntHandler(FloatHandler(StrHandler(NullHandler())))
```

* __Chain.handle(obj, EventGet(int))__ — вернуть значение __obj.integer_field__
* __Chain.handle(obj, EventGet(str))__ — вернуть значение __obj.string_field__
* __Chain.handle(obj, EventGet(float))__ — вернуть значение __obj.float_field__
* __Chain.handle(obj, EventSet(1))__ — установить значение __obj.integer_field =1__
* __Chain.handle(obj, EventSet(1.1))__ — установить значение __obj.float_field = 1.1__
* __Chain.handle(obj, EventSet("str"))__ — установить значение __obj.string_field = "str"__

### Пример работы:

```python
>>> obj = SomeObject()
>>> obj.integer_field = 42
>>> obj.float_field = 3.14
>>> obj.string_field = "some text"
>>> chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
>>> chain.handle(obj, EventGet(int))
42
>>> chain.handle(obj, EventGet(float))
3.14
>>> chain.handle(obj, EventGet(str))
'some text'
>>> chain.handle(obj, EventSet(100))
>>> chain.handle(obj, EventGet(int))
100
>>> chain.handle(obj, EventSet(0.5))
>>> chain.handle(obj, EventGet(float))
0.5
>>> chain.handle(obj, EventSet('new text'))
>>> chain.handle(obj, EventGet(str))
'new text'
```
