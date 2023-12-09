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

    def get_cash_amount(self):
        return self.__cash_amount

    def update_pantry_costs(self):
        pass

    def update_supplies_costs(self):
        pass

    def update_employee_costs(self):
        pass

    def update_cash_amount(self):
        pass
    