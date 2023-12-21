#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/9/2023
# @Author  : Yiming Qu

from data_load import DataLoad


class CashStatus:
    def __init__(self):
        self.__cash_amount = 10000

        self.__income = 0
        self.__coffee_price = DataLoad()("demand", "Coffee Types",
                                         "Price(pounds)")
        self.__supplies_price = {
            "Milk": 0.0003,
            "Beans": 0.10,
            "Spices": 0.05
        }

        self.__rent_costs = 1500

        self.__pantry_costs = 0
        self.__supplies_costs = 0
        self.__baristas_costs = 0

    def get_cash_amount(self):
        return self.__cash_amount

    def update_income(self, demand: dict):
        income = {}
        for coffee in self.__coffee_price.keys():
            income[coffee] = demand[coffee] * self.__coffee_price[coffee]
            self.__income += income[coffee]
        return income

    def update_pantry_costs(self, pantry_quantity: dict, pantry_costs_rate: dict):
        pantry_costs = {}
        for ingredient in pantry_quantity.keys():
            pantry_costs[ingredient] = pantry_quantity[ingredient] * pantry_costs_rate[ingredient]
            self.__pantry_costs += pantry_costs[ingredient]

        return pantry_costs

    def update_supplies_costs(self, pantry_shortage: dict):
        supplies_costs = {}
        for ingredient in pantry_shortage.keys():
            supplies_costs[ingredient] = pantry_shortage[ingredient] * self.__supplies_price[ingredient]
            self.__supplies_costs += supplies_costs[ingredient]
        return supplies_costs

    def update_baristas_costs(self, number: int):
        paid_rate = 15
        paid_hour = 120
        self.__baristas_costs = number * paid_rate * paid_hour
        return self.__baristas_costs

    def update_cash_amount(self):
        self.__cash_amount += (self.__income - self.__rent_costs - self.__pantry_costs
                               - self.__supplies_costs - self.__baristas_costs)

    def profit_reset(self):
        self.__income = 0

        self.__pantry_costs = 0
        self.__supplies_costs = 0
        self.__baristas_costs = 0
