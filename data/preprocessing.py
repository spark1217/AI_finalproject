import requests 
from bs4 import BeautifulSoup 
import json 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import csv
import pandas as pd
from pandas import DataFrame



data = pd.read_csv('course_list_table.csv')
x = data["Sections"]
x_1 = data.drop(["Sections"] ,axis = 1)

empty_df = pd.DataFrame()

for i in range(len(data)):
        temp_value = x_1.iloc[i].values
        temp = pd.DataFrame(columns=["Course code", "Course title", "Units", "Requisite"])
        temp.loc[0, "Course code"] = temp_value[0]
        temp.loc[0, "Course title"] = temp_value[1]
        temp.loc[0, "Units"] = temp_value[2]
        temp.loc[0, "Requisite"] = temp_value[3]

        y = x[i]
        z = y.strip().lstrip("[").rstrip("]")
        w = eval(z)

        if isinstance(w, dict):
                raw_data = w
                u = DataFrame(raw_data, index = [0])
                temp_1 = pd.concat([temp, u], axis = 1)
                empty_df = pd.concat((empty_df,temp_1),sort=False)

        else:
                for itr in range(len(w)):
                        raw_data = w[itr]
                        u = DataFrame(raw_data, index = [0])
                        temp_1 = pd.concat([temp, u], axis = 1)
                        empty_df = pd.concat((empty_df,temp_1),sort=False)


empty_df = empty_df.drop(["Topic", "Notes"], axis = 1).reset_index()
print(empty_df)
empty_df.to_csv("course_list_csp.csv")


