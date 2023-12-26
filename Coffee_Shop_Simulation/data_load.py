#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/5/2023
# @Author  : Yiming Qu

import csv


class DataLoad:
    def __init__(self):
        self.__tables_path = {
            "demand": "tables/demand.csv",
            "ingredients": "tables/ingredients.csv",
            "pantry": "tables/pantry.csv",
            "supplier": "tables/supplier.csv"
        }

    def csv_to_dict(self, table_name: str, key_column, value_column, is_float=True):
        data = {}
        with open(self.__tables_path[table_name]) as file:
            reader = csv.DictReader(file)
            if is_float:
                for row in reader:
                    data[row[key_column]] = float(row[value_column])
            else:
                for row in reader:
                    data[row[key_column]] = int(row[value_column])
        return data

    def __call__(self, table_name: str, key_column, value_column, is_float=True):
        return self.csv_to_dict(table_name, key_column, value_column, is_float=is_float)




