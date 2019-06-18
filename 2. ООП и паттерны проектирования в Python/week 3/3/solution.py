from abc import ABC, abstractmethod

#
# class Engine:
#     pass


class ObservableEngine(Engine):
    """Движок Engine, который может создавать уведомления о достижениях"""

    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self.__subscribers.remove(subscriber)

    def notify(self, new_ach):
        for subscriber in self.__subscribers:
            subscriber.update(new_ach)


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, new_ach):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, new_ach):
        self.achievements.add(new_ach['title'])

class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list()

    def update(self, new_ach):
        if new_ach not in self.achievements:
            self.achievements.append(new_ach)
