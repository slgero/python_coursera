from abc import ABC, abstractmethod
import pygame
import random
import os
import Service


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class AbstractObject(ABC):
    def __init__(self):
        self.sprite = None
        self.position = None
    
    def draw(self, display):
        offset = display.screen_offset()
        display.blit(self.sprite, ((self.position[0] - offset[0]) * display.game_engine.sprite_size,
                                      (self.position[1] - offset[1]) * display.game_engine.sprite_size))


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats.copy()
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.get_stats()["endurance"] * 4
        
    def get_stats(self):
        return self.stats
        

class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, xp, position, name):
        self.name = name
        self.xp = xp
        super().__init__(icon, stats, position)
    
    def interact(self, engine, hero):
        if self.name == 'shadow' and isinstance(hero, Darkness):
            self.hp = 10**10
            engine.notify('Beware shadows in the dark!')
            
        while self.hp > 0 and hero.hp > 0:
            hero_critical = 5 if random.uniform(0, 100) < hero.get_stats()['luck'] else 0
            enemy_critical = 5 if random.uniform(0, 100) < self.get_stats()['luck'] else 0
            self.hp -= hero.get_stats()['strength'] * (1 + hero_critical)
            hero.hp -= self.get_stats()['strength'] * (1 + enemy_critical)
        if hero.hp <= 0:
            engine.level = 5
            hero = Hero(hero.base_stats, Service.create_sprite(
                    os.path.join("texture", "grave.png"), engine.sprite_size))
            engine.notify('You died. Press "R" to restart.')
            Service.reload_game(engine, hero)
        else:
            hero.exp += self.xp
            for message in hero.level_up():
                engine.notify(message)


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.item_level = 0
        self.base_stats = stats
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "Level up!"
            self.level += 1
            entity = self
            while isinstance(entity, Effect):
                entity.stats["strength"] += 2
                entity.stats["endurance"] += 2
                entity = entity.base
            entity.stats["strength"] += 2
            entity.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp
            
            
    def get_stats(self):
        return {"strength": self.stats["strength"] * 2**self.item_level,
                "endurance": self.stats["endurance"] * 2**self.item_level,
                "intelligence": self.stats["intelligence"], 
                "luck": self.stats["luck"]}


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()
        
    @property
    def base_stats(self):
        return self.base.base_stats
        
    @property
    def item_level(self):
        return self.base.item_level

    @item_level.setter
    def item_level(self, value):
        if value < 4:
            self.base.item_level = value

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite
    
    @sprite.setter
    def sprite(self, value):
        self.base.sprite = value

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):
    def apply_effect(self):
        self.stats['strength'] += 50
        self.stats['endurance'] -= 20 if self.stats['endurance'] > 20 else self.stats['endurance']
        self.calc_max_HP()
        self.hp = self.max_hp
    
    
class Blessing(Effect):
    def apply_effect(self):
        self.stats['strength'] += 5
        self.stats['endurance'] += 5
        self.stats['luck'] += 5
        self.stats['intelligence'] += 5
        self.hp += 10
        if self.hp > self.max_hp:
            self.max_hp = self.hp


class Weakness(Effect):
    def apply_effect(self):
        self.stats['strength'] = 15


class Darkness(Effect):
    def apply_effect(self):
        self.stats['strength'] -= 5
        self.stats['endurance'] -= 5
        self.stats['luck'] -= 5
        self.stats['intelligence'] -= 5
        self.hp -= 10 if self.hp > 10 else self.hp - 1
