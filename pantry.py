#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/5/2023
# @Author  : Yiming Qu

from data_load import DataLoad


class Pantry:
    def __init__(self):
        self.__quantity = DataLoad()("pantry", "Ingredient",
                                     "Quantity(ml or g)")
        self.__depreciation = DataLoad()("pantry", "Ingredient",
                                         "Depreciation(ratio/month)")
        self.__pantry_costs_rate = DataLoad()("pantry", "Ingredient",
                                              "Pantry costs(pounds/ml or pounds/g)")

    def get_quantity(self):
        return self.__quantity

    def get_depreciation(self):
        return self.__depreciation

    def get_pantry_costs_rate(self):
        return self.__pantry_costs_rate

    def update_quantity(self):
        pass
