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

        self.__pantry = Pantry()
        self.__cash_status = CashStatus()

        self.__max_demand = DataLoad()("demand", "Coffee Types",
                                       "Monthly Demand")
        self.__demand = {
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

    def is_demand_exceed(self, demand: dict):
        for coffee in demand.keys():
            if demand[coffee] > self.__max_demand[coffee]:
                return False
        return True

    def update_ingredients_consumption(self, demand: dict):
        for coffee in demand.keys():
            for ingredient in self.__ingredients_consumption_rate[coffee].keys():
                self.__ingredients_consumption[ingredient] = demand[coffee] * \
                                                             self.__ingredients_consumption_rate[coffee][ingredient]
        # Check whether ingredients are sufficient
        if self.__pantry.consume_and_update_quantity(self.__ingredients_consumption):
            return True
        else:
            return False

    def ingredients_consumption_reset(self):
        self.__ingredients_consumption = {
            "Milk": 0,
            "Beans": 0,
            "Spices": 0
        }

