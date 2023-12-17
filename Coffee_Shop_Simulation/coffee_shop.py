#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/8/2023
# @Author  : Yiming Qu

from barista import Barista, BaristaTeam
from pantry import Pantry
from cash_status import CashStatus
from data_load import DataLoad


class CoffeeShop:
    def __init__(self, name):
        self.__name = name

        self.__barista_team = BaristaTeam()
        self.__pantry = Pantry()
        self.__cash_status = CashStatus()

        self.__max_demand = DataLoad()("demand", "Coffee Types",
                                       "Monthly Demand")

        self.__ingredients_consumption_rate = {
            "Expresso": {"Milk": 0, "Beans": 8, "Spices": 0},
            "Americano": {"Milk": 0, "Beans": 6, "Spices": 0},
            "Filter": {"Milk": 0, "Beans": 4, "Spices": 0},
            "Macchiatto": {"Milk": 100, "Beans": 8, "Spices": 2},
            "Flat White": {"Milk": 200, "Beans": 8, "Spices": 1},
            "Latte": {"Milk": 300, "Beans": 8, "Spices": 3}
        }

    def is_barista_name_exist(self, name):
        if name in self.__barista_team.get_baristas_names():
            return True
        else:
            return False

    def add_baristas(self, numbers: int, names: list, specialities: list):
        self.__barista_team.add_baristas(numbers, names, specialities)

    def remove_baristas(self, *names):
        self.__barista_team.remove_baristas(names)

    def barista_team_number(self):
        return self.__barista_team.baristas_number()

    def reset_baristas_labour_time(self):
        self.__barista_team.reset_total_labour_time()

    def update_baristas_labour_time(self, demand: dict):
        self.__barista_team.update_total_labour_time(demand)

    def is_demand_exceed(self, demand: dict):
        for coffee in demand.keys():
            if demand[coffee] > self.__max_demand[coffee]:
                return False
        return True

    def update_ingredients_consumption(self, demand: dict):
        consumption = {}
        for coffee in demand.keys():
            for ingredient in self.__ingredients_consumption_rate[coffee].keys():
                consumption[ingredient] = demand[coffee] * self.__ingredients_consumption_rate[coffee][ingredient]
        # Check whether ingredients are sufficient
        if self.__pantry.consume_and_update_quantity(consumption):
            return True
        else:
            return False

    def get_pantry_ingredients(self):
        return self.__pantry.get_quantity()

    def get_cash_amount(self):
        return self.__cash_status.get_cash_amount()

    def get_income(self, demand: dict):
        return self.__cash_status.update_income(demand)

    def get_pantry_costs(self, pantry_quantity, pantry_costs_rate):
        return self.__cash_status.update_pantry_costs(pantry_quantity, pantry_costs_rate)

    def get_supplies_costs(self):
        pantry_shortage = self.__pantry.get_shortage()
        return self.__cash_status.update_supplies_costs(pantry_shortage)

    def get_employee_costs(self, number: int):
        return self.__cash_status.update_employee_costs(number)

    def update_cash_amount(self):
        self.__cash_status.update_cash_amount()

    def profit_reset(self):
        self.__cash_status.profit_reset()




