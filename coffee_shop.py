#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/8/2023
# @Author  : Yiming Qu

from barista import Barista
from pantry import Pantry
from cash_status import CashStatus
from data_load import DataLoad


class CoffeeShop:
    def __init__(self, name):
        self.__name = name
        self.__baristas = {}
        self.__specialists = {  # Barista who has a speciality will be added
            "Expresso": set(),  # Specialities are keys, while baristas' names are values
            "Americano": set(),
            "Filter": set(),
            "Macchiatto": set(),
            "Flat White": set(),
            "Latte": set()
        }

        self.__pantry = Pantry()
        self.__cash_status = CashStatus()

        self.__max_demand = DataLoad()("demand", "Coffee Types",
                                       "Monthly Demand")
        self.__demand = self.__ingredients_consumption_rate = {
            "Expresso": 0,
            "Americano": 0,
            "Filter": 0,
            "Macchiatto": 0,
            "Flat White": 0,
            "Latte": 0
        }
        self.__ingredients_consumption = {
            "Milk": 0,
            "Beans": 0,
            "Spices": 0
        }

        self.__ingredients_consumption_rate = {
            "Expresso": {"Milk": 0, "Beans": 8, "Spices": 0},
            "Americano": {"Milk": 0, "Beans": 6, "Spices": 0},
            "Filter": {"Milk": 0, "Beans": 4, "Spices": 0},
            "Macchiatto": {"Milk": 100, "Beans": 8, "Spices": 2},
            "Flat White": {"Milk": 200, "Beans": 8, "Spices": 1},
            "Latte": {"Milk": 300, "Beans": 8, "Spices": 3}
        }

    def add_baristas(self, numbers: int, names: list,  specialities: list):
        if numbers + self.baristas_number() <= 4:
            for name, speciality in zip(names, specialities):
                is_special = speciality in self.__specialists.keys()
                self.__baristas[name] = Barista(name, speciality, is_special=is_special)
                print(f"Barista {name} has been employed.")
                if is_special:
                    self.__specialists[speciality].add(name)
                    print(f"{name} specialises in {speciality}")
                else:
                    print(f"{name} doesn't have a speciality")
            return True

        else:
            return False

    def remove_baristas(self, *names):
        for name in names:
            del self.__baristas[name]

    def baristas_number(self):
        return len(self.__baristas)

    def update_demand(self, **demand):
        origin_demand = self.__demand

        for coffee in demand.keys():
            if demand[coffee] <= self.__max_demand[coffee]:
                self.__demand[coffee] = demand[coffee]
            else:
                self.__demand = origin_demand
                return False

    def update_ingredients_consumption(self):
        pass

    def demand_reset(self):
        self.__demand = self.__ingredients_consumption_rate = {
            "Expresso": 0,
            "Americano": 0,
            "Filter": 0,
            "Macchiatto": 0,
            "Flat White": 0,
            "Latte": 0
        }

    def ingredients_consumption_reset(self):
        self.__ingredients_consumption = {
            "Milk": 0,
            "Beans": 0,
            "Spices": 0
        }
