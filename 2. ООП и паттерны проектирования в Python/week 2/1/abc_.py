""" How to use abc module """
from abc import ABC, abstractmethod  # ABC -> Abstract Base Class


class A(ABC):
    """ To create abstract method """

    @abstractmethod
    def do_something(self):
        print('TAAAAAANOS')


class B(A):
    def do_something_else(self):
        print('I don\'t want to do smt')

    def do_something(self):
        print('TONY_STARK!')


b = B()
b.do_something()
