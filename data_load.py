#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/5/2023
# @Author  : Yiming Qu

import pandas as pd


class DataLoad:
    def __init__(self):
        self.__tables = {
            "demand": pd.read_excel("tables/demand.xlsx"),
            "ingredients": pd.read_excel("tables/ingredients.xlsx"),
            "pantry": pd.read_excel("tables/pantry.xlsx"),
            "supplier": pd.read_excel("tables/supplier.xlsx")
        }

    def read_excel_columns(self, table_name: str, *args):
        column_names = [name for name in args]
        data = self.__tables[table_name].loc[:, column_names]
        return data

    def excel_to_dict(self, table_name: str, key_column, value_column):
        return self.read_excel_columns(table_name, key_column, value_column).\
            set_index(key_column)[value_column].to_dict()

    def __call__(self, table_name: str, key_column, value_column, is_structured=False):
        if is_structured:
            return self.read_excel_columns(table_name, key_column, value_column)
        else:
            return self.excel_to_dict(table_name, key_column, value_column)




