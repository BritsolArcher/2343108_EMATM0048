#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/2023
# @Author  : Yiming Qu

from data_load import DataLoad
from typing import Dict


class Barista:
    def __init__(self, name, speciality, is_special=False):
        self.__name = name
        self.__speciality = speciality if is_special else None
        self.__labour_time = 80 * 60  # minutes
        self.__paid_rate = 15
        self.__paid_hour = 120

    def get_name(self):
        return self.__name

    def is_special(self):
        return True if self.__speciality is not None else False

    def get_speciality(self):
        return self.__speciality

    def get_salary(self):
        return self.__paid_rate * self.__paid_hour

    def labour_time_reset(self):
        self.__labour_time = 80 * 60


class BaristaTeam:
    def __init__(self):
        self.__baristas: Dict[str, Barista] = {}  # Key: name; Value: Barista
        self.__specialists = {  # Barista who has a speciality will be added
            "Expresso": set(),  # Specialities are keys, while baristas names are values
            "Americano": set(),
            "Filter": set(),
            "Macchiatto": set(),
            "Flat White": set(),
            "Latte": set()
        }
        self.__total_labour_time = 0
        self.__coffe_produce_rate = DataLoad()("ingredients", "Coffee Types",
                                               "Time to Prepare (in minutes)")

    def get_baristas_names(self):
        return self.__baristas.keys()

    def add_baristas(self, numbers: int, names: list, specialities: list):
        if numbers + self.baristas_number() <= 4:
            for name, speciality in zip(names, specialities):
                is_special = speciality in self.__specialists.keys()
                self.__baristas[name] = Barista(name, speciality, is_special=is_special)
                print(f"Barista {name} has been employed.")
                if is_special:
                    self.__specialists[speciality].add(name)
                    print(f"{name} specialises in {speciality}")
                else:
                    print(f"{name} doesn't have a speciality")
            return True

        else:
            return False

    def remove_baristas(self, *names):
        for name in names:
            if self.__baristas[name].is_special():
                speciality = self.__baristas[name].get_speciality()
                self.__specialists[speciality].discard(name)
            del self.__baristas[name]

    def baristas_number(self):
        return len(self.__baristas)

    def reset_total_labour_time(self):
        self.__total_labour_time = self.baristas_number() * 80 * 60

    def update_total_labour_time(self, demand: dict):
        current_specialists_number = {}
        for coffee, names in self.__specialists.items():
            if len(names) > 0:
                current_specialists_number[coffee] = len(names)

        if len(current_specialists_number) == 0:  # If there is not any specialists
            for coffee in demand.keys():
                time_consumption = demand[coffee] * self.__coffe_produce_rate[coffee]
                self.__total_labour_time -= time_consumption
        else:
            for coffee in current_specialists_number.keys():
                # Specialists can make the specialised coffee in 1/2 the time
                time_consumption = 0.5 * demand[coffee] * self.__coffe_produce_rate[coffee]
                specialists_labour_time = current_specialists_number[coffee] * 80 * 60

                # Check whether specialists' labour_time is ran out
                if time_consumption <= specialists_labour_time:
                    self.__total_labour_time -= time_consumption
                    demand[coffee] = 0  # Update demand
                else:
                    self.__total_labour_time -= specialists_labour_time
                    demand[coffee] -= int(specialists_labour_time /
                                          (self.__coffe_produce_rate[coffee] * 0.5))  # Update demand

            for coffee in demand.keys():
                time_consumption = demand[coffee] * self.__coffe_produce_rate[coffee]
                self.__total_labour_time -= time_consumption

        if self.__total_labour_time > 0:
            return True
        else:
            self.reset_total_labour_time()
            return False
