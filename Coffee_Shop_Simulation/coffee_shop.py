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

        self.__coffe_produce_rate = DataLoad()("ingredients", "Coffee Types",
                                               "Time to Prepare (in minutes)")

        self.__ingredients_consumption = {
            "Milk": 0,
            "Beans": 0,
            "Spices": 0
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

    def is_demand_exceed_max_demand(self, demand: dict):
        for coffee in demand.keys():
            if demand[coffee] > self.__max_demand[coffee]:
                return False
        return True

    # def update_consumption(self, coffee: str, demand: dict, total_labour_time, ingredients_consumption):
    #     time_consumption = demand[coffee] * self.__coffe_produce_rate[coffee]
    #     if total_labour_time - time_consumption < 0:  # Check whether the labour constraints is exceeded
    #         pass
    #     else:
    #         for ingredient in self.__ingredients_consumption_rate[coffee].keys():
    #             # Calculate the total ingredients consumption
    #             ingredients_consumption[ingredient] += (
    #                     demand[coffee] * self.__ingredients_consumption_rate[coffee][ingredient])
    #         if self.__pantry.is_ingredients_demand_exceed(ingredients_consumption):
    #             ingredients_consumption = self.__ingredients_consumption
    #             '''pass'''
    #         else:  # Update ingredients consumption, total_labour_time
    #             self.__ingredients_consumption = ingredients_consumption
    #             total_labour_time -= time_consumption
    #             return ingredients_consumption, total_labour_time
    def reset_demand(self, demand: dict, coffee_type: str, reset_value: int):
        ingredients_consumption = self.__ingredients_consumption
        demand[coffee_type] = reset_value
        ingredients_consumption = self.update_ingredients_consumption(demand, coffee_type, ingredients_consumption)
        return ingredients_consumption

    def update_ingredients_consumption(self, demand: dict, coffee_type: str, ingredients_consumption: dict):
        for ingredient in self.__ingredients_consumption_rate[coffee_type].keys():
            # Calculate the total ingredients consumption
            ingredients_consumption[ingredient] += (
                    demand[coffee_type] * self.__ingredients_consumption_rate[coffee_type][ingredient])
        return ingredients_consumption

    def is_demand_exceed(self, demand: dict):
        current_specialists_number = {}  # Count the number of specialists
        specialists_time_consumption = {}

        specialists = self.__barista_team.get_specialists()
        total_labour_time = self.__barista_team.get_total_labour_time()
        ingredients_consumption = {  # Record the ingredients consumption
            "Milk": 0,
            "Beans": 0,
            "Spices": 0
        }
        for coffee, names in specialists.items():  # Count the number of specialists
            if len(names) > 0:
                current_specialists_number[coffee] = len(names)

        # Provide coffee of specialised type first
        if len(current_specialists_number) > 0:
            for coffee in current_specialists_number.keys():
                ingredients_consumption = self.update_ingredients_consumption(demand, coffee, ingredients_consumption)

                # Check whether ingredients demand is exceeded
                while self.__pantry.is_ingredients_demand_exceed(ingredients_consumption):
                    ingredients_consumption = self.reset_demand(demand, coffee, reset_value=-1)

                # Record the specialists labour time
                specialists_labour_time = current_specialists_number[coffee] * 80 * 60
                # Specialists can make coffee in half a time
                time_consumption = 0.5 * demand[coffee] * self.__coffe_produce_rate[coffee]

                # Check whether specialists labour exceeds constrain
                if time_consumption <= specialists_labour_time:
                    total_labour_time -= time_consumption
                    self.__ingredients_consumption = ingredients_consumption
                else:
                    specialists_time_consumption[coffee] = specialists_labour_time

            if len(specialists_time_consumption) > 0:
                for coffee in specialists_time_consumption.keys():
                    coffee_finished = specialists_time_consumption[coffee]/(self.__coffe_produce_rate[coffee]*0.5)
                    coffee_remain = demand[coffee] - int(coffee_finished)
                    time_consumption = coffee_remain * self.__coffe_produce_rate[coffee]

                    while total_labour_time - time_consumption - specialists_time_consumption[coffee] < 0:
                        demand[coffee] = -1  # reset
                        if demand[coffee] <= coffee_finished:
                            time_consumption = 0.5 * demand[coffee] * self.__coffe_produce_rate[coffee]
                            total_labour_time -= time_consumption
                            self.__ingredients_consumption = (
                                self.update_ingredients_consumption(demand, coffee, ingredients_consumption))
                            break
                        else:
                            coffee_remain = demand[coffee] - int(coffee_finished)
                            time_consumption = coffee_remain * self.__coffe_produce_rate[coffee]

                    total_labour_time -= (time_consumption + specialists_time_consumption[coffee])
                    self.__ingredients_consumption = ingredients_consumption

        for coffee in demand.keys():
            if coffee not in specialists_time_consumption.keys():
                ingredients_consumption = self.update_ingredients_consumption(demand, coffee, ingredients_consumption)
                while self.__pantry.is_ingredients_demand_exceed(ingredients_consumption):
                    ingredients_consumption = self.reset_demand(demand, coffee, reset_value=-1)

                time_consumption = demand[coffee] * self.__coffe_produce_rate[coffee]
                while total_labour_time - time_consumption < 0:
                    ingredients_consumption = self.reset_demand(demand, coffee, reset_value=-1)

                total_labour_time -= time_consumption
                self.__ingredients_consumption = ingredients_consumption

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




