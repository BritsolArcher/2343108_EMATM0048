#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/2023
# @Author  : Yiming Qu

from typing import Dict


class Barista:
    def __init__(self, name, speciality, is_special=False):
        self.__name = name
        self.__speciality = speciality if is_special else None
        self.__labour_time = 80 * 60  # minutes
        self.__paid_rate = 15
        self.__paid_hour = 120

    def is_special(self):
        return True if self.__speciality is not None else False

    def get_speciality(self):
        """
        Check if the name already exists in the name list of barista team.

        Args:
          name: The name of a new barista.

        returns:
          A boolean indicating if the name already exists.
        """
        return self.__speciality

    def get_salary(self):
        return self.__paid_rate * self.__paid_hour

    def labour_time_reset(self):
        self.__labour_time = 80 * 60


class BaristaTeam:
    def __init__(self):
        self.__baristas: Dict[str, Barista] = {}
        self.__specialists = {
            "Expresso": set(),
            "Americano": set(),
            "Filter": set(),
            "Macchiatto": set(),
            "Flat White": set(),
            "Latte": set()
        }
        self.__total_labour_time = 0

    def get_baristas_names(self):
        """
        Get baristas names.

        returns:
          A set of the baristas names.
        """
        return self.__baristas.keys()

    def is_barista_name_exist(self, name):
        """
        Check if the name already exists in the name list of barista team.

        Args:
          name: The name of a new barista.

        returns:
          A boolean indicating if the name already exists.
        """
        if name in self.get_baristas_names():
            return True
        else:
            return False

    def add_baristas(self, number: int, baristas: dict):
        """
        Add new baristas in barista team.

        Args:
          number: The number of new baristas.
          baristas : The baristas <name, speciality> need to add
        """

        # Check whether the total number of baristas is exceeded
        if number + self.baristas_number() <= 4:
            for name, speciality in baristas.items():

                # Check whether barista name exists or the input is null
                while self.is_barista_name_exist(name) or name is None:
                    name = input("This name already exists, Please enter another: ")

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
        """
        Dismiss baristas in barista team.

        Args:
          names: The name of baristas to dismiss.
        """
        for name in names:
            if self.__baristas[name].is_special():
                speciality = self.__baristas[name].get_speciality()
                self.__specialists[speciality].discard(name)
            del self.__baristas[name]

    def baristas_number(self):
        return len(self.__baristas)

    def get_specialists(self):
        return self.__specialists

    def reset_total_labour_time(self):
        self.__total_labour_time = self.baristas_number() * 80 * 60

    def get_total_labour_time(self):
        return self.__total_labour_time
