#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/8/2023
# @Author  : Yiming Qu

from barista import BaristaTeam
from pantry import Pantry
from cash_status import CashStatus
from data_load import DataLoad


class CoffeeShop:
    """
    A class representing a coffee shop.

    Attributes:
        __barista_team: A class representing baristas
        __pantry: A class representing the pantry of the coffee shop
        __cash_status: A class representing the cash status of the coffee shop
        __max_demand: A dictionary with coffee types as keys and their corresponding maximum demand as values.
        __ingredients_consumption_rate: A nested dictionary recording ingredients consumption rate
        __coffe_produce_rate: A dictionary with coffee types as keys and their corresponding production time as values.
        __ingredients_consumption: A dictionary recording the ingredients consumption
    """

    def __init__(self):
        """
        Initializes the instance.
        """
        self.__barista_team = BaristaTeam()
        self.__pantry = Pantry()
        self.__cash_status = CashStatus()

        self.__max_demand = DataLoad()("demand", "Coffee Types",
                                       "Monthly Demand", False)

        self.__ingredients_consumption_rate = {
            "Expresso": {"Milk": 0, "Beans": 8, "Spices": 0},
            "Americano": {"Milk": 0, "Beans": 6, "Spices": 0},
            "Filter": {"Milk": 0, "Beans": 4, "Spices": 0},
            "Macchiatto": {"Milk": 100, "Beans": 8, "Spices": 2},
            "Flat White": {"Milk": 200, "Beans": 8, "Spices": 1},
            "Latte": {"Milk": 300, "Beans": 8, "Spices": 3}
        }

        self.__coffe_produce_rate = DataLoad()("ingredients", "Coffee Types",
                                               "Time to Prepare (in minutes)", False)

        self.__ingredients_consumption = {
            "Milk": 0,
            "Beans": 0,
            "Spices": 0
        }

    def add_baristas(self, number: int, baristas: dict):
        """
        Add new baristas in barista team.

        Args:
          number: The number of new baristas.
          baristas : The baristas <name, speciality> need to add
        """
        self.__barista_team.add_baristas(number, baristas)

    def remove_baristas(self, number: int, names: set):
        """
        Dismiss baristas in barista team.

        Args:
          number: The number of baristas to dismiss
          names: The name of baristas to dismiss.
        """
        self.__barista_team.remove_baristas(number, names)

    def get_baristas_names(self):
        """
        Get baristas names.

        returns:
          A set of the baristas names.
        """
        return self.__barista_team.get_baristas_names()

    def barista_team_number(self):
        """
        Get the number of baristas.

        Returns:
          An integer representing the number of baristas.
        """
        return self.__barista_team.baristas_number()

    def reset_baristas_labour_time(self):
        """
        Reset baristas labour.
        """
        self.__barista_team.reset_total_labour_time()

    def reset_demand(self, demand: dict, coffee_type: str, ingredients_consumption: dict, reset_value: int):
        """
        Reset demand if ingredients are not sufficient and update the ingredients_consumption
        based on the demand.

        Args:
          coffee_type: The coffee type
          demand: The coffee demand.
          ingredients_consumption: The ingredients consumption of the coffee.
          reset_value: The reset value for the demand.

        Returns:
          A dictionary recording the previous ingredients consumption
        """
        demand[coffee_type] = reset_value
        self.update_ingredients_consumption(demand, coffee_type, ingredients_consumption)

    def update_ingredients_consumption(self, demand: dict, coffee_type: str, ingredients_consumption: dict):
        """
        Update ingredients consumption based on a particular coffee's demand.

        Args:
          demand: The coffee demand.
          coffee_type: The coffee type
          ingredients_consumption: The ingredients consumption need to update

        Returns:
          A dictionary recording the updated ingredients' consumption.
        """
        for ingredient in self.__ingredients_consumption_rate[coffee_type].keys():
            # Calculate the total ingredients consumption
            ingredients_consumption[ingredient] = (
                    demand[coffee_type] * self.__ingredients_consumption_rate[coffee_type][ingredient])

        return ingredients_consumption

    def update_demand(self, demand: dict):
        current_specialists_number = {}  # A dictionary recording the specialists number in each coffee type
        specialists_time_consumption = {}  # A dictionary recording the total specialists labour in different coffee

        specialists = self.__barista_team.get_specialists()
        total_labour_time = self.__barista_team.get_total_labour_time()
        # Record the ingredients TOTAL consumption
        ingredients_consumption = {
            "Milk": 0,
            "Beans": 0,
            "Spices": 0
        }
        # Count the number of specialists in different coffee types
        for coffee, names in specialists.items():
            if len(names) > 0:
                current_specialists_number[coffee] = len(names)

        def reset_value(coffee_demand: dict, coffee_type: str):
            """
            Resets the demand values for a given coffee

            Returns:
                An integer representing the reset demand value.
            """
            try:
                value = int(input(f"Please reset the demand of {coffee_type}: "))
                while value < 0:
                    print("Please enter a non-negative integer!")
                    value = int(input(f"Please reset the demand of {coffee_type}: "))

            except ValueError:
                print("Please enter a non-negative integer!")
                value = coffee_demand[coffee_type]
            return value

        def is_ingredients_demand_exceed(ingredient_consumption: dict):
            """
            Checks if the ingredients exceed the pantry's capacity

            Returns:
                A boolean indicating whether the ingredients exceed the pantry's capacity.
            """
            consumption = {}
            for ingredient in ingredient_consumption:
                consumption[ingredient] = self.__ingredients_consumption[ingredient] + ingredient_consumption[
                    ingredient]
            return self.__pantry.is_ingredients_demand_exceed(consumption)

        # Let specialists provide the coffee they specialised first
        if len(current_specialists_number) > 0:
            for coffee in current_specialists_number.keys():
                ingredients_consumption = self.update_ingredients_consumption(demand, coffee, ingredients_consumption)

                # Check whether ingredients demand is exceeded
                while is_ingredients_demand_exceed(ingredients_consumption):
                    quantity = self.__pantry.get_quantity()
                    print("Ingredients are not sufficient.")
                    print(f"Milk need {ingredients_consumption['Milk']} mL, "
                          f"pantry remain {quantity['Milk'] - self.__ingredients_consumption['Milk']} mL")

                    print(f"Beans need {ingredients_consumption['Beans']} g, "
                          f"pantry remain {quantity['Beans'] - self.__ingredients_consumption['Beans']} g")

                    print(f"Spices need {ingredients_consumption['Spices']} g, "
                          f"pantry remain {quantity['Spices'] - self.__ingredients_consumption['Spices']} g")
                    reset_demand_value = reset_value(demand, coffee)
                    self.reset_demand(demand, coffee, ingredients_consumption, reset_value=reset_demand_value)

                # Record the specialists labour time
                specialists_labour_time = current_specialists_number[coffee] * 80 * 60
                # Specialists can make coffee in half a time
                time_consumption = 0.5 * demand[coffee] * self.__coffe_produce_rate[coffee]

                # Check whether specialists labour exceeds constrain
                if time_consumption <= specialists_labour_time:
                    # Update total_labour_time
                    total_labour_time -= time_consumption

                    # Update __ingredients_consumption
                    for ingredient in ingredients_consumption:
                        self.__ingredients_consumption[ingredient] += ingredients_consumption[ingredient]
                else:
                    specialists_time_consumption[coffee] = specialists_labour_time

            if len(specialists_time_consumption) > 0:
                for coffee in specialists_time_consumption.keys():
                    coffee_finished = specialists_time_consumption[coffee] / (self.__coffe_produce_rate[coffee] * 0.5)
                    coffee_remain = demand[coffee] - int(coffee_finished)

                    # Remaining coffee will be produced at regular rate
                    remain_time_consumption = coffee_remain * self.__coffe_produce_rate[coffee]
                    time_consumption = remain_time_consumption + specialists_time_consumption[coffee]
                    while total_labour_time < remain_time_consumption + specialists_time_consumption[coffee]:

                        print(f"Labour is not sufficient, "
                              f"need {remain_time_consumption + specialists_time_consumption[coffee]}, "
                              f"remain {total_labour_time}.")

                        demand[coffee] = reset_value(demand, coffee)

                        ingredients_consumption = (
                            self.update_ingredients_consumption(demand, coffee, ingredients_consumption))

                        if demand[coffee] <= coffee_finished:
                            time_consumption = 0.5 * demand[coffee] * self.__coffe_produce_rate[coffee]
                            while total_labour_time < time_consumption:
                                print(f"Labour is not sufficient, "
                                      f"need {time_consumption}, "
                                      f"remain {total_labour_time}.")

                                reset_demand = reset_value(demand, coffee)
                                self.reset_demand(demand, coffee, ingredients_consumption, reset_value=reset_demand)
                                time_consumption = 0.5 * demand[coffee] * self.__coffe_produce_rate[coffee]
                            break
                        else:
                            coffee_remain = demand[coffee] - int(coffee_finished)
                            remain_time_consumption = coffee_remain * self.__coffe_produce_rate[coffee]
                            time_consumption = remain_time_consumption + specialists_time_consumption[coffee]

                    total_labour_time -= time_consumption
                    for ingredient in ingredients_consumption:
                        self.__ingredients_consumption[ingredient] += ingredients_consumption[ingredient]

        for coffee in demand.keys():
            if coffee not in current_specialists_number.keys():
                self.update_ingredients_consumption(demand, coffee, ingredients_consumption)
                while is_ingredients_demand_exceed(ingredients_consumption):
                    quantity = self.__pantry.get_quantity()
                    print("Ingredients are not sufficient.")
                    for ingredient in self.__ingredients_consumption.keys():
                        capacity = "g"
                        if ingredient == "Milk":
                            capacity = "mL"
                        print(f"{ingredient} need {ingredients_consumption[ingredient]} {capacity}, "
                              f"pantry remain {quantity[ingredient] - self.__ingredients_consumption[ingredient]} "
                              f"{capacity}")

                    reset_demand_value = reset_value(demand, coffee)
                    self.reset_demand(demand, coffee, ingredients_consumption, reset_value=reset_demand_value)

                time_consumption = demand[coffee] * self.__coffe_produce_rate[coffee]
                while total_labour_time - time_consumption < 0:
                    print(f"Labour is not sufficient, "
                          f"need {time_consumption} minutes, "
                          f"remain {total_labour_time} minutes.")

                    reset_demand = reset_value(demand, coffee)
                    self.reset_demand(demand, coffee, ingredients_consumption, reset_value=reset_demand)
                    time_consumption = demand[coffee] * self.__coffe_produce_rate[coffee]

                total_labour_time -= time_consumption
                for ingredient in ingredients_consumption:
                    self.__ingredients_consumption[ingredient] += ingredients_consumption[ingredient]

        return demand

    def get_pantry_ingredients(self):
        """
        Get the quantity of ingredients.

        Returns:
          A dictionary recording the quantity of ingredients.
        """
        return self.__pantry.get_quantity()

    def get_cash_amount(self):
        """
        Get the cash amount.

        Returns:
          An integer representing the cash amount.
        """
        return self.__cash_status.get_cash_amount()

    def is_not_bankrupt(self):
        """
        Check if the coffee shop is bankrupt.

        Returns:
          An boolean representing the status of the coffee shop.
        """
        coffee_shop_status = (self.get_cash_amount() >= 0)
        return coffee_shop_status

    def get_income(self, demand: dict):
        """
        Update and get the income (not the pure profit) from coffee sales.

        Args:
            demand: A dictionary representing the coffee demand.

        Returns:
          A dictionary representing the income from coffee sales.
        """
        return self.__cash_status.update_income(demand)

    def get_pantry_costs(self, pantry_quantity, pantry_costs_rate):
        """
        Update and get the costs from pantry.

        Returns:
          An integer representing the costs from pantry.
        """
        return self.__cash_status.update_pantry_costs(pantry_quantity, pantry_costs_rate)

    def get_supplies_costs(self):
        """
        Update and get the costs from supplies.

        Returns:
          A dictionary representing the cost from ingredients.
        """
        pantry_supplies_amount = self.__pantry.get_supplies_amount()
        return self.__cash_status.update_supplies_costs(pantry_supplies_amount)

    def get_baristas_costs(self, number: int):
        """
        Update and get the costs from baristas.

        Args:
          number: The number of baristas need to be paid.

        Returns:
          An integer representing the costs from baristas.
        """
        return self.__cash_status.update_baristas_costs(number)

    def update_cash_amount(self):
        """
        Update cash amount.
        """
        self.__cash_status.update_cash_amount()

    def profit_reset(self):
        """
        Reset attributes related to profit in __cash_status.
        """
        self.__cash_status.profit_reset()
