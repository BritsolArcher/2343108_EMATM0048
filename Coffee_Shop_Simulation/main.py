#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/4/2023
# @Author  : Yiming Qu

from coffee_shop import CoffeeShop
from data_load import DataLoad


def input_baristas(number: int):
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
        while name in baristas.keys() or is_blank(name):
            name = input("This name already exists or you didn't input anything, Please enter another: ")
        code = input("Please enter the code of coffee type: ")

        speciality = specialists[code] if code in specialists.keys() else None
        baristas[name] = speciality

    return baristas


def input_demand():
    max_demand = DataLoad()("demand", "Coffee Types",
                            "Monthly Demand")
    demand = {}

    for coffee in max_demand:
        try:
            print()
            demand[coffee] = int(input(f"{coffee} demand is: "))
            while demand[coffee] > max_demand[coffee]:
                print(f"{coffee} demand exceeded maximum demand!")
                demand[coffee] = int(input(f"{coffee} demand is: "))

        except ValueError:
            print(f"Invalid input! {coffee} demand will be set to maximum demand!")
            demand[coffee] = max_demand[coffee]

    return demand


def main():
    coffee_shop = CoffeeShop()

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
        print(f"====== SIMULATING month {opening_month} ======")
        print("================================")
        print("To add enter positive, to remove enter negative, no change enter 0.")
        try:
            update_number = int(input("Please enter the number of baristas you would like to add or remove: "))

            if update_number > 0:
                baristas = input_baristas(update_number)
                coffee_shop.add_baristas(update_number, baristas)

            elif update_number < 0:
                names = set()

                update_number = -update_number

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

        print(coffee_shop.barista_team_number())
        if coffee_shop.barista_team_number() == 0:
            print("The coffee shop must have at least one barista!\n")
            continue

        opening_month += 1


if __name__ == "__main__":
    main()
