class Item(object):
    def __init__(self, name, price):
        self.name = name
        self.price = price


def __iter__(self):
    yield 'name', self.name
    yield 'price', self.price
    yield 'type', 'item'


class Weapon(Item):
    def __init__(self, name, price, damage=1):
        Item.__init__(self, name, int(price))
        self.damage = damage
        # print(dict(self))

    def __iter__(self):
        yield 'type', 'weapon'
        yield 'damage', self.damage
        yield 'name', self.name
        yield 'price', self.price


class Armor(Item):
    def __init__(self, name, price, defense=1):
        Item.__init__(self, name, int(price))
        self.defense = defense
        # print(dict(self))

    def __iter__(self):
        yield 'type', 'armor'
        yield 'defense', self.defense
        yield 'name', self.name
        yield 'price', self.price


class Potion(Item):
    def __init__(self, name, price, health=1):
        Item.__init__(self, name, int(price))
        self.health = health
        # print(dict(self))

    def __iter__(self):
        yield 'type', 'armor'
        yield 'health', self.health
        yield 'name', self.name
        yield 'price', self.price