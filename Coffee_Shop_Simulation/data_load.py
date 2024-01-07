#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/5/2023
# @Author  : Yiming Qu

import csv


class DataLoad:
    """
    A class representing the cash status of the coffee shop.

    Attributes:
        __tables_path: A dictionary representing the path of the tables
    """
    def __init__(self):
        """
        Initializes the instance.
        """
        self.__tables_path = {
            "demand": "tables/demand.csv",
            "ingredients": "tables/ingredients.csv",
            "pantry": "tables/pantry.csv",
            "supplier": "tables/supplier.csv"
        }

    def csv_to_dict(self, table_name: str, key_column, value_column, is_float=True):
        """
        Transforms the csv table into a dictionary.

        Args:
            table_name: A string representing the table name.
            key_column: A string representing the column name of the table which is to set as the key
                        in the dictionary.
            value_column: A string representing the column name of the table which is to set as the value
                          in the dictionary.

        Returns:
          The transformed dictionary.
        """
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
        """
        Transforms the csv table into a dictionary.

        Args:
            table_name: A string representing the table name.
            key_column: A string representing the column name of the table which is to set as the key
                        in the dictionary.
            value_column: A string representing the column name of the table which is to set as the value
                          in the dictionary.

        Returns:
          The transformed dictionary.
        """
        return self.csv_to_dict(table_name, key_column, value_column, is_float=is_float)




