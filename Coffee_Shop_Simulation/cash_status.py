#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/9/2023
# @Author  : Yiming Qu

from data_load import DataLoad


class CashStatus:
    """
    A class representing the cash status of the coffee shop.

    Attributes:
        __cash_amount: An integer representing the cash amount of the coffee shop.
        __income: An integer representing the income from coffee sales.
        __coffee_price: A dictionary representing the price of the coffee
        __supplies_price: A dictionary representing price of ingredients.
        __rent_costs: An integer representing the rent costs.
        __pantry_costs: An integer representing the pantry costs.
        __supplies_costs: An integer representing the supplies costs.
        __baristas_costs: An integer representing the baristas costs.
    """
    def __init__(self):
        """
        Initializes the instance.
        """
        self.__cash_amount = 10000

        self.__income = 0
        self.__coffee_price = DataLoad()("demand", "Coffee Types",
                                         "Price(pounds)")
        self.__supplies_price = {
            "Milk": 0.3,
            "Beans": 0.10,
            "Spices": 0.05
        }

        self.__pantry_costs_rate = {
            "Milk": 0.1,
            "Beans": 0.001,
            "Spices": 0.001
        }

        self.__rent_costs = 1500

        self.__pantry_costs = 0
        self.__supplies_costs = 0
        self.__baristas_costs = 0

    def get_cash_amount(self):
        """
        Get the cash amount.

        Returns:
          An integer representing the cash amount.
        """
        return self.__cash_amount

    def update_income(self, demand: dict):
        """
        Update and get the income (not the pure profit) from coffee sales.

        Args:
            demand: A dictionary representing the coffee demand.

        Returns:
          A dictionary representing the income from coffee sales.
        """
        income = {}
        for coffee in self.__coffee_price.keys():
            income[coffee] = demand[coffee] * self.__coffee_price[coffee]
            self.__income += income[coffee]
        return income

    def update_pantry_costs(self, pantry_quantity: dict):
        pantry_costs = {}
        for ingredient in pantry_quantity.keys():
            pantry_costs[ingredient] = pantry_quantity[ingredient] * self.__pantry_costs_rate[ingredient]
            self.__pantry_costs += round(pantry_costs[ingredient], 2)
        return pantry_costs

    def update_supplies_costs(self, pantry_shortage: dict):
        """
        Update and get the costs from supplies.

        Returns:
          A dictionary representing the cost from ingredients.
        """
        supplies_costs = {}
        for ingredient in pantry_shortage.keys():
            supplies_costs[ingredient] = pantry_shortage[ingredient] * self.__supplies_price[ingredient]
            self.__supplies_costs += round(supplies_costs[ingredient], 2)
        return supplies_costs

    def update_baristas_costs(self, number: int):
        """
        Update and get the costs from baristas.

        Args:
          number: The number of baristas need to be paid.

        Returns:
          An integer representing the costs from baristas.
        """
        paid_rate = 15
        paid_hour = 120
        self.__baristas_costs = number * paid_rate * paid_hour
        return self.__baristas_costs

    def update_cash_amount(self):
        """
        Update cash amount.
        """
        self.__cash_amount += (self.__income - self.__rent_costs - self.__pantry_costs
                               - self.__supplies_costs - self.__baristas_costs)

    def profit_reset(self):
        """
        Reset attributes related to profit.

        """
        self.__income = 0

        self.__pantry_costs = 0
        self.__supplies_costs = 0
        self.__baristas_costs = 0
