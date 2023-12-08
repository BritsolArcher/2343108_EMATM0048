#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/8/2023
# @Author  : Yiming Qu

from barista import Barista
from pantry import Pantry


class CoffeeShop:
    def __init__(self):
        self.__baristas = {}
        self.__pantry = Pantry()
        self.__cash = 10000
        self.__specialists = {  # Baristas who has a speciality will be added
            "Expresso": [],
            "Americano": [],
            "Filter": [],
            "Macchiatto": [],
            "Flat White": [],
            "Latte": []
        }

    def add_baristas(self, numbers: int, names: list,  specialities: list):
        if numbers + self.baristas_number() <= 4:
            for name, speciality in zip(names, specialities):
                is_special = speciality in self.__specialists.keys()
                self.__baristas[name] = Barista(name, speciality, is_special=is_special)
                print(f"Barista {name} has been employed.")
                if is_special:
                    print(f"{name} specialises in {speciality}")
                else:
                    print(f"{name} doesn't have a speciality")

    def remove_baristas(self, numbers: int, *names):
        for name in names:
            del self.__baristas[name]

    def baristas_number(self):
        return len(self.__baristas)
