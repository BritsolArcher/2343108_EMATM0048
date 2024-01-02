#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/5/2023
# @Author  : Yiming Qu

from data_load import DataLoad
import math


class Pantry:
    """
    A class representing a pantry.

    Attributes:
        __full_quantity: A dictionary representing the max quantity of each ingredient.
        __quantity: A dictionary representing the current quantity of each ingredient.
        __depreciation: A dictionary representing the depreciation rate of each ingredient.
    """

    def __init__(self):
        """
        Initializes the instance.
        """
        self.__full_quantity = DataLoad()("pantry", "Ingredient",  # can't be modified
                                          "Quantity(L or g)")

        self.__quantity = DataLoad()("pantry", "Ingredient",
                                     "Quantity(L or g)")
        self.__depreciation = DataLoad()("pantry", "Ingredient",
                                         "Depreciation(ratio/month)")

    def get_quantity(self):
        """
        Gets the quantity of the pantry.

        Returns:
            A dictionary representing the pantry quantity.
        """
        return self.__quantity

    def is_full(self):
        """
        Checks if the pantry is full.

        Returns:
            A boolean representing whether the pantry is full.
        """
        for ingredient in self.__quantity.keys():
            if self.__quantity[ingredient] < self.__full_quantity[ingredient]:
                return False
        return True

    def get_depreciation(self):
        """
        Gets the depreciation of the pantry.

        Returns:
            A dictionary representing the depreciation rate.
        """
        return self.__depreciation

    def is_ingredients_demand_exceed(self, consumption: dict):
        """
        Check whether the ingredients exceed the pantry's capacity.

        Returns:
            A boolean representing the status.
        """
        quantity = self.__quantity
        for ingredient in quantity.keys():
            # Check whether ingredients are insufficient
            if quantity[ingredient] - consumption[ingredient] < 0:
                return True
        return False

    def consume_and_update_quantity(self, consumption: dict):  # Update quantity after consumption
        """
        Calculate the consumption of the pantry and update the pantry's quantity.
        """
        for ingredient in self.__quantity.keys():
            self.__quantity[ingredient] -= consumption[ingredient]

    def depreciate_and_update_quantity(self):
        """
        Calculate the depreciation and update the pantry's capacity.
        """
        for ingredient in self.__quantity.keys():
            depreciation = math.ceil(self.__quantity[ingredient] * self.__depreciation[ingredient])
            self.__quantity[ingredient] -= depreciation

    def get_supplies_amount(self):
        """
        Get the amount of ingredients that should be supplied.

        Returns:
            A dictionary representing the amount of ingredients that should be supplied.
        """
        supplies_amount = {}
        for ingredient in self.__quantity.keys():
            supplies_amount[ingredient] = self.__full_quantity[ingredient] - self.__quantity[ingredient]

        return supplies_amount

    def pantry_quantity_reset(self):
        """
        Reset the quantity to full quantity.
        """
        for ingredient in self.__quantity.keys():
            self.__quantity[ingredient] = self.__full_quantity[ingredient]
