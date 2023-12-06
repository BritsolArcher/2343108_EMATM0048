#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/2023
# @Author  : Yiming Qu

from data_load import DataLoad


class Barista:
    def __init__(self, name, speciality, is_special=False):
        self.__name = name
        self.__speciality = speciality if is_special else None
        self.__labour_time = 80 * 60  # minutes
        self.__paid_rate = 15
        self.__paid_hour = 120
        self.__coffe_produce_rate = DataLoad()("ingredients", "Coffee Types",
                                               "Time to Prepare (in minutes)")

        print(f"Barista {self.__name} has been employed. ")
        if is_special:
            self.__coffe_produce_rate[self.__speciality] *= 0.5
            print(f"{self.__name} specialises in {self.__speciality}")
        else:
            print(f"{self.__name} doesn't have a speciality")

    def get_name(self):
        return self.__name

    def get_speciality(self):
        return self.__speciality

    def get_salary(self):
        return self.__paid_rate * self.__paid_hour

    def labour_time_remain(self):
        pass

    def labour_time_reset(self):
        self.__labour_time = 80 * 60
        