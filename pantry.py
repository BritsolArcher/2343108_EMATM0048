#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/5/2023
# @Author  : Yiming Qu

from data_load import DataLoad


class Pantry:
    def __init__(self):
        self.__quantity = DataLoad()("pantry", "Coffee Types", "Quantity")
        self.__depreciation = DataLoad()("pantry", "Coffee Types", "Depreciation")
        self.__pantry_costs = DataLoad()("pantry", "Coffee Types", "Pantry costs")

    def get_quantity(self):
        return self.__quantity

    def get_depreciation(self):
        return self.__depreciation

    def get_pantry_costs(self):
        return self.__pantry_costs

    def update_quantity(self):
        pass
