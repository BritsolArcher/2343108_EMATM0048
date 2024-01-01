#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/2023
# @Author  : Yiming Qu

from typing import Dict


class Barista:
    """
    A class representing a Barista.

    Attributes:
       __speciality: A string representing the coffee type that the barista is specialised in.
       __salary: An integer representing the salary of the barista.
    """

    def __init__(self, speciality, is_special=False):
        """
        Initializes the instance.
        Args:
        speciality: The coffee type that the barista specialised in.
        is_special: Whether the barista specialises in one type of coffee
        """
        self.__speciality = speciality if is_special else None
        self.__salary = 15 * 120

    def is_special(self):
        """
        Check if the barista is specialised in one type of coffee.

        returns:
          A boolean indicating if the name already exists.
        """
        return True if self.__speciality is not None else False

    def get_speciality(self):
        """
        Check if the name already exists in the name list of barista team.
        returns:
          A boolean indicating if the name already exists.
        """
        return self.__speciality


class BaristaTeam:
    """
    A class representing a Barista Team.

    Attributes:
       __baristas: A dictionary to representing the barista team.
                   key is the barista name and the value is Barista instance.
       __specialists: A dictionary to record any barista who is specialised in one type of coffee.
       __total_labour_time: An integer representing the total labour of he barista team.
    """

    def __init__(self):
        """
        Initializes the instance.
        """
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
                # while self.is_barista_name_exist(name) or name is None:
                #     name = input("This name already exists, Please enter another: ")
                # Check whether speciality in coffee type sets
                is_special = speciality in self.__specialists.keys()
                self.__baristas[name] = Barista(speciality, is_special=is_special)
                print(f"Barista {name} has been added.")

                if is_special:
                    self.__specialists[speciality].add(name)
                    print(f"Barista {name} specialises in {speciality}.", end=" ")
                else:
                    print(f"Barista {name} doesn't have any speciality.", end=" ")
                print("Hourly rate = 15 hours")
        else:
            if self.baristas_number() == 4:
                print("This coffee shop has already been fully employed. "
                      "This month will not have any change in baristas.")

            elif self.baristas_number() < 4:
                add_number = 4 - self.baristas_number()
                print(f"Only {add_number} baristas will be added.")
                count = 0
                for name, speciality in baristas.items():
                    if count == add_number:
                        break
                    # Check whether barista name exists or the input is null
                    # while self.is_barista_name_exist(name) or name is None:
                    #     name = input("This name already exists, Please enter another: ")

                    # Check whether speciality in coffee type sets
                    is_special = speciality in self.__specialists.keys()
                    self.__baristas[name] = Barista(speciality, is_special=is_special)
                    print(f"Barista {name} has been added.", end=" ")

                    if is_special:
                        self.__specialists[speciality].add(name)
                        print(f"Barista {name} specialises in {speciality}.", end=" ")
                    else:
                        print(f"Barista {name} doesn't have any speciality.", end=" ")
                    print("Hourly rate = 15 hours")
                    count += 1
        self.reset_total_labour_time()

    def remove_baristas(self, number: int, names: set):
        """
        Dismiss baristas in barista team.

        Args:
          number: The number of baristas to be removed
          names: The name of baristas to dismiss.
        """
        if self.baristas_number() - number >= 1:
            for name in names:
                if self.__baristas[name].is_special():
                    speciality = self.__baristas[name].get_speciality()
                    self.__specialists[speciality].discard(name)
                del self.__baristas[name]

        else:
            remove_number = self.baristas_number() - 1
            if self.baristas_number() == 0:
                print(f"No baristas will be removed because coffee shop must have at least one barista.")
                return
            else:
                print(f"Only {remove_number} baristas will be removed "
                      f"because coffee shop must have at least one barista.")

                for name in names:
                    if self.baristas_number() > 1:
                        if self.__baristas[name].is_special():
                            speciality = self.__baristas[name].get_speciality()
                            self.__specialists[speciality].discard(name)
                        del self.__baristas[name]
                        print(f"Barista {name} has been removed.")
        self.reset_total_labour_time()

    def baristas_number(self):
        """
        Get the number of baristas.

        Returns:
          An integer representing the number of baristas.
        """
        return len(self.__baristas)

    def get_baristas_info(self):
        """
        Get the baristas who specialised in one type of coffee.

        Returns:
          An integer representing the number of baristas.
        """
        for name in self.__baristas:
            if self.__baristas[name].is_special():
                speciality = self.__baristas[name].get_speciality()
                print(f"Barista {name} specialises in {speciality}, hourly rate = 15 hours.")
            else:
                print(f"Barista {name}, hourly rate = 15 hours.")

    def get_specialists(self):
        """
        Get the baristas who specialised in one type of coffee.

        Returns:
          An integer representing the number of baristas.
        """
        return self.__specialists

    def reset_total_labour_time(self):
        """
        Reset labour status of all baristas.
        """
        self.__total_labour_time = self.baristas_number() * 80 * 60

    def get_total_labour_time(self):
        """
        Get labour status of all baristas.
        """
        return self.__total_labour_time
