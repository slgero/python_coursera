# Задание по программированию: Создание декоратора класса

Представьте себя ненадолго разработчиком компьютерной игры в стиле фэнтези. Вы будете прописывать систему эффектов, которые могут быть наложены на героя вашей игры.

У вас есть герой, который обладает некоторым набором характеристик. Враги и союзники могут накладывать на героя положительные и отрицательные эффекты. Эти эффекты каким-то образом изменяют характеристики героя. На героя можно накладывать бесконечно много эффектов, действие одинаковых эффектов суммируется. Игрок должен знать, какие положительные и какие отрицательные эффекты на него были наложены и в каком порядке.

Класс герой описан следующим образом (характеристики могут быть другими):

```python
class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        
        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,
            
            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        } 
        
    def get_positive_effects(self):
        return self.positive_effects.copy()
    
    def get_negative_effects(self):
        return self.negative_effects.copy()
    
    def get_stats(self):
        return self.stats.copy()
        
    ...
```

Описывать класс героя в коде НЕ НУЖНО.

Вам нужно написать систему декораторов, представленную на UML-диаграмме:

![text](https://d3c33hcgiwev3.cloudfront.net/imageAssetProxy.v1/fXs5G_96EeeAPQprC3K2Bg_8e1189dd970d8e6270b7fbe567341f44_Decorator.JPG?expiry=1560902400000&hmac=pdNP9PxKsg6Ldet33X5WPs6FQtW6Keq2c6m6-0EDXpQ)

Названия наложенных положительных и отрицательных эффектов добавляются каждое в свой счетчик. Названия эффектов совпадают с названиями классов.

Описания эффектов:

* __Берсерк__ — Увеличивает параметры Сила, Выносливость, Ловкость, Удача на 7; уменьшает параметры Восприятие, Харизма, Интеллект на 3. Количество единиц здоровья увеличивается на 50.
* __Благословение__ — Увеличивает все основные характеристики на 2.
* __Слабость__ — Уменьшает параметры Сила, Выносливость, Ловкость на 4.
* __Сглаз__ — Уменьшает параметр Удача на 10.
* __Проклятье__ — Уменьшает все основные характеристики на 2.

К основным характеристикам относятся Сила (Strength), Восприятие (Perception), Выносливость (Endurance), Харизма (Charisma), Интеллект (Intelligence), Ловкость (Agility), Удача (Luck).

При выполнении задания учитывайте, что:

* Изначальные характеристики базового объекта не должны меняться.
* Изменения характеристик и накладываемых эффектов (баффов/дебаффов) должно происходить динамически, то есть при запросе get_stats, get_positive_effects, get_negative_effects
* Абстрактные классы AbstractPositive, AbstractNegative и соответственно их потомки могут принимать любой параметр base при инициализации объекта (_ _ init _ _ (self, base))
* Проверяйте, что эффекты корректно снимаются, в том числе и из середины стека

__Пример работы:__

```python
>>> from deco import *
>>> # создаем героя
>>> hero = Hero()
>>> hero.get_stats()
{'HP': 128, 'MP': 42, 'SP': 100, 'Strength': 15, 'Perception': 4, 'Endurance': 8, 'Charisma': 2, 'Intelligence': 3, 'Agility': 8, 'Luck': 1}
>>> hero.stats
{'HP': 128, 'MP': 42, 'SP': 100, 'Strength': 15, 'Perception': 4, 'Endurance': 8, 'Charisma': 2, 'Intelligence': 3, 'Agility': 8, 'Luck': 1}
>>> hero.get_negative_effects()
[ ]
>>> hero.get_positive_effects()
[ ]
>>> # накладываем эффект
>>> brs1 = Berserk(hero)
>>> brs1.get_stats()
{'HP': 178, 'MP': 42, 'SP': 100, 'Strength': 22, 'Perception': 1, 'Endurance': 15, 'Charisma': -1, 'Intelligence': 0, 'Agility': 15, 'Luck': 8}
>>> brs1.get_negative_effects()
[ ]
>>> brs1.get_positive_effects()
['Berserk']
>>> # накладываем эффекты
>>> brs2 = Berserk(brs1)
>>> cur1 = Curse(brs2)
>>> cur1.get_stats()
{'HP': 228, 'MP': 42, 'SP': 100, 'Strength': 27, 'Perception': -4, 'Endurance': 20, 'Charisma': -6, 'Intelligence': -5, 'Agility': 20, 'Luck': 13}
>>> cur1.get_positive_effects()
['Berserk', 'Berserk']
>>> cur1.get_negative_effects()
['Curse']
>>> # снимаем эффект Berserk
>>> cur1.base = brs1
>>> cur1.get_stats()
{'HP': 178, 'MP': 42, 'SP': 100, 'Strength': 20, 'Perception': -1, 'Endurance': 13, 'Charisma': -3, 'Intelligence': -2, 'Agility': 13, 'Luck': 6}
>>> cur1.get_positive_effects()
['Berserk']
>>> cur1.get_negative_effects()
['Curse']
>>>
```
