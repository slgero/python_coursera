# Реализация паттерна Strategy (стратегия)
# http://cpp-reference.ru/patterns/behavioral-patterns/strategy/

class ZIP_Comp:
    def compress(self, file_name):
        print('ZIP compress' + file_name)


class ARJ_Comp:
    def compress(self, file_name):
        print('ARJ compress' + file_name)


class Compressor:
    def __init__(self, file_name, compress_strategy):
        self._file_name = file_name
        self._strategy = compress_strategy

    def compress(self):
        self._strategy.compress(self._file_name)