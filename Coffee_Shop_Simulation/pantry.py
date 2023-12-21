#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/5/2023
# @Author  : Yiming Qu

from data_load import DataLoad
import math


class Pantry:
    def __init__(self):
        self.__full_quantity = DataLoad()("pantry", "Ingredient",  # can't be modified
                                          "Quantity(ml or g)")

        self.__quantity = DataLoad()("pantry", "Ingredient",
                                     "Quantity(ml or g)")
        self.__depreciation = DataLoad()("pantry", "Ingredient",
                                         "Depreciation(ratio/month)")
        self.__pantry_costs_rate = DataLoad()("pantry", "Ingredient",
                                              "Pantry costs(pounds/ml or pounds/g)")

    def get_quantity(self):
        return self.__quantity

    def is_full(self):
        for ingredient in self.__full_quantity.keys():
            if self.__quantity[ingredient] < self.__full_quantity[ingredient]:
                return False
        return True

    def get_depreciation(self):
        return self.__depreciation

    def get_pantry_costs_rate(self):
        return self.__pantry_costs_rate

    def is_ingredients_demand_exceed(self, consumption: dict):
        quantity = self.__quantity
        for ingredient in quantity.keys():
            quantity[ingredient] -= consumption[ingredient]
            if quantity[ingredient] < 0:  # Check whether ingredients are insufficient
                return True
            else:
                return False

    def consume_and_update_quantity(self, consumption: dict):  # Update quantity after consumption
        for ingredient in self.__quantity.keys():
            self.__quantity[ingredient] -= consumption[ingredient]

    def depreciate_and_update_quantity(self):  # update quantity after depreciation
        for ingredient in self.__quantity.keys():
            depreciation = math.ceil(self.__quantity[ingredient] * self.__depreciation[ingredient])
            self.__quantity[ingredient] -= depreciation

    def get_supplies_amount(self):
        supplies_amount = {}
        for ingredient in self.__quantity.keys():
            supplies_amount[ingredient] = self.__full_quantity[ingredient] - self.__quantity[ingredient]
        return supplies_amount

    def pantry_quantity_reset(self):
        self.__quantity = self.__full_quantity

