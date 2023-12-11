#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/9/2023
# @Author  : Yiming Qu


class CashStatus:
    def __init__(self):
        self.__cash_amount = 10000

        self.__rent_costs = 1500

        self.__pantry_costs = 0
        self.__supplies_costs = 0
        self.__employee_costs = 0

        self.__income = 0

    def get_cash_amount(self):
        return self.__cash_amount

    def update_pantry_costs(self, pantry_quantity: dict, pantry_costs_rate: dict):
        pantry_costs = {}
        for ingredient in pantry_quantity.keys():
            pantry_costs[ingredient] = pantry_quantity[ingredient] * pantry_costs_rate[ingredient]
            self.__pantry_costs += pantry_costs[ingredient]

        return pantry_costs

    def update_supplies_costs(self, pantry_shortage: dict, supplies_price: dict):
        for ingredient in pantry_shortage.keys():
            self.__supplies_costs += pantry_shortage[ingredient] * supplies_price[ingredient]

    def update_employee_costs(self, numbers: int):
        paid_rate = 15
        paid_hour = 120
        self.__employee_costs = numbers * paid_rate * paid_hour

    def update_cash_amount(self):
        self.__cash_amount += (self.__income - self.__rent_costs - self.__pantry_costs
                               - self.__supplies_costs - self.__employee_costs)

    def profit_reset(self):
        self.__pantry_costs = 0
        self.__supplies_costs = 0
        self.__employee_costs = 0

        self.__income = 0
