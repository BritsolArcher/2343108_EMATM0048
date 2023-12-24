#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/4/2023
# @Author  : Yiming Qu

from coffee_shop import CoffeeShop


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

    for i in range(number):
        name = input("Please enter the name of the barista: ")
        code = input("Please enter the code of coffee type: ")

        speciality = specialists[code] if code in specialists.keys() else None
        baristas[name] = speciality

    return baristas


def main():
    coffee_shop = CoffeeShop()

    try:
        end_month = int(input("Please enter the month you would like to end the simulation: "))
        if end_month <= 0:
            print("Invalid input. The month will be set to 6")
            end_month = 6

    except ValueError:
        print("Invalid input. The month will be set to 6")
        end_month = 6

    opening_month = 1  # Opening month of the coffee shop

    while opening_month <= end_month:
        print("================================")
        print(f"====== SIMULATING month {opening_month} ======")
        print("================================")
        print("To add enter positive, to remove enter negative, no change enter 0.")
        while coffee_shop.barista_team_number() == 0:
            print("The coffee shop must have at least one barista!")
            try:
                update_number = int(input("Please enter the number of baristas you would like to add or remove"))

                if update_number > 0:
                    baristas = input_baristas(update_number)
                    coffee_shop.add_baristas(update_number, baristas)

                elif update_number < 0:
                    names = {}

                    for i in range(update_number):
                        name = input("Please enter the name of the coffee")
                        while name in names or name not in coffee_shop.get_baristas_names():
                            print("Invalid input. Please try again")
                            name = input("Please enter the name of the coffee")

                    coffee_shop.remove_baristas(names)

                elif update_number == 0:
                    print("This month will not have any change in baristas.")

            except ValueError:
                print("Invalid input. This month will not have any change in baristas.")


if __name__ == "__main__":
    main()
