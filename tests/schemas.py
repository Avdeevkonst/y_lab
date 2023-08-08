from dataclasses import dataclass


@dataclass
class Menu:
    id: str
    title: str
    description: str


@dataclass
class Submenu(Menu):
    pass


@dataclass
class Dish(Menu):
    price: str
