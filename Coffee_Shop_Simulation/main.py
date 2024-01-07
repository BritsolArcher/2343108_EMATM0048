#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/4/2023
# @Author  : Yiming Qu

from coffee_shop import CoffeeShop
from data_load import DataLoad


def input_baristas(number: int, baristas_names):
    """
    This function is utilised for inputting baristas.

    Args:
      number: The number of baristas to add.
      baristas_names: The names of the baristas.

    Returns:
      A dictionary representing baristas.
    """
    baristas = {}
    specialists = {
        "0": "Expresso",
        "1": "Americano",
        "2": "Filter",
        "3": "Macchiatto",
        "4": "Flat White",
        "5": "Latte"
    }
    for code, speciality in specialists.items():
        print(f"Code {code} represents the barista will be specialised in {speciality}.")
    print("Other input represents the barista will not be specialise in any type of coffee.")

    def is_blank(barista_name: str):
        """
        Check whether the input name is blank or not.

        Args:
          barista_name: The names of the barista.

        Returns:
          A boolean indicating whether the name is blank or not.
        """
        if barista_name == "":
            return True

        if barista_name[0] != " ":
            return False

        for char in barista_name:
            if char != " ":
                return False
        return True

    for i in range(number):
        name = input("Please enter the name of the barista: ")
        while name in baristas.keys() or is_blank(name) or name in baristas_names:
            name = input("This name already exists or you didn't input anything, Please enter another: ")
        code = input("Please enter the code of coffee type: ")
        print("")

        speciality = specialists[code] if code in specialists.keys() else None
        baristas[name] = speciality

    return baristas


def input_demand():
    """
    This function is utilised for inputting coffee demands.

    Returns:
      A dictionary representing demand.
    """
    max_demand = DataLoad()("demand", "Coffee Types",
                            "Monthly Demand", False)
    demand = {}

    for coffee in max_demand:
        try:
            print()
            demand[coffee] = int(input(f"{coffee} max demand is: {max_demand[coffee]}, "
                                       f"please set this month's demand: "))

            while demand[coffee] > max_demand[coffee] or demand[coffee] < 0:
                print(f"Invalid input! {coffee}, please reset the demand!")
                demand[coffee] = int(input(f"{coffee} demand is: "))

        except ValueError:
            print(f"Invalid input! {coffee} demand will be set to maximum demand!")
            demand[coffee] = max_demand[coffee]
        print("")
    return demand


def main():
    """
    Main function of the program.
    """
    name = input("Please input the coffee shop name: ")

    input_flag = True
    while input_flag:
        if name == "":
            name = input("Invalid input, please reenter the name: ")
        elif name != "":
            for s in name:
                if s != " ":
                    input_flag = False
                break
            if not input_flag:
                break
            name = input("Invalid input, please reenter the name: ")

    coffee_shop = CoffeeShop(name)

    try:
        end_month = int(input("Please enter the month you would like to end the simulation: "))
        if end_month <= 0:
            print("Invalid input. The month will be set to 6\n")
            end_month = 6

    except ValueError:
        print("Invalid input. The month will be set to 6\n")
        end_month = 6

    opening_month = 1  # Opening month of the coffee shop
    while opening_month <= end_month:
        print("================================")
        print(f"====== SIMULATING MONTH {opening_month} ======")
        print("================================")
        print("To add enter positive, to remove enter negative, no change enter 0.")

        baristas_names = coffee_shop.get_baristas_names()
        try:
            update_number = int(input("Please enter the number of baristas you would like to add or remove: "))

            if update_number > 0:
                baristas = input_baristas(update_number, baristas_names)
                coffee_shop.add_baristas(update_number, baristas)

            elif update_number < 0:
                names = set()

                update_number = -update_number

                if coffee_shop.barista_team_number() < update_number:
                    print("Invalid input!")
                    update_number = coffee_shop.barista_team_number() - 1 if coffee_shop.barista_team_number() > 1 else 0
                    if update_number == 0:
                        print("This month will not have any change in baristas.")
                    else:
                        print(f"The number of baristas to remove will be set to {update_number}")

                for i in range(update_number):
                    name = input("Please enter the name of barista: ")
                    while name not in coffee_shop.get_baristas_names() or name in names:
                        print("Invalid input!")
                        name = input("Please enter the name of barista: ")
                    names.add(name)

                coffee_shop.remove_baristas(update_number, names)

            elif update_number == 0:
                print("This month will not have any change in baristas.")

        except ValueError:
            print("Invalid input. This month will not have any change in baristas.")

        if coffee_shop.barista_team_number() == 0:
            print("The coffee shop must have at least one barista!\n")
            continue

        demand = input_demand()
        coffee_shop.update_demand(demand)

        print("")
        for coffee in demand.keys():
            print(f" {coffee} demand is {demand[coffee]}.")
        print("")

        for barista in coffee_shop.get_baristas_names():
            print(f"Paid {barista}, hourly rate=15 hours, amount £1800.")
        coffee_shop.update_baristas_costs()

        print("")

        print("Paid rent/utilities £1500")

        print("")

        print("------------Pantry--------------\n")
        pantry_costs = coffee_shop.update_pantry_costs()
        for ingredient, costs in pantry_costs.items():
            print(f"Pantry {ingredient} cost £{costs}")

        print("")

        print("After coffee production: ")
        quantity = coffee_shop.get_pantry_ingredients()
        print(f"Pantry milk remain {quantity['Milk']} L, capacity = 300L.")
        print(f"Pantry beans remain {quantity['Beans']} g, capacity = 20000g.")
        print(f"Pantry spices remain {quantity['Spices']} g, capacity = 4000g.")

        print("")

        print("After depreciation: ")
        pantry_remain = coffee_shop.depreciate_and_update_quantity()
        print(f"Pantry milk remain {pantry_remain['Milk']} L, capacity = 300L.")
        print(f"Pantry beans remain {pantry_remain['Beans']} g, capacity = 20000g.")
        print(f"Pantry spices remain {pantry_remain['Spices']} g, capacity = 4000g.")

        print("")

        pantry_supplies_costs = coffee_shop.update_supplies_costs()
        for ingredient, costs in pantry_supplies_costs.items():
            print(f"Supply {ingredient} cost £{costs}")
        coffee_shop.pantry_quantity_reset()
        print("")

        income = coffee_shop.update_income(demand)
        for coffee in income.keys():
            print(f"Income from {coffee} is £{income[coffee]}.")
        coffee_shop.update_cash_amount()
        coffee_shop.profit_reset()

        print("")
        print(f"Coffee Shop {coffee_shop.get_coffee_shop_name()}, cash £{coffee_shop.get_cash_amount()}.")

        print("")
        print("------------Barista-------------\n")
        coffee_shop.get_baristas_info()

        if coffee_shop.is_not_bankrupt():
            opening_month += 1
        else:
            print("")
            print(f"====== FINAL MONTH {opening_month} ======")
            print(f"Coffee Shop {coffee_shop.get_coffee_shop_name()} has been bankrupt.")
            break


if __name__ == "__main__":
    main()
