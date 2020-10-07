# This file writes the "original/first" employee data file
# this file creates the data file and adds the employees that will already be there

import csv
from Create_Employees import *




def get_ol():
    with open("AllEmployees.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        reader_list = list(reader)

        return (len(reader_list))


def e():

    with open("AllEmployees.csv", "w+") as csvfile:
        fieldnames = ["Firstname", "Lastname", "Phone", "Age", "ID", "Title", "Daily Salary"]
        # num of rows
        next_id = str(100 + get_ol())
        fn = "Ally"
        ln = "Shap"
        age = "24"
        p = "2222222222"
        t = "Bartender"
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"Firstname": fn, "Lastname": ln, "Age": age, "Phone": p, "ID":next_id, "Title": t, "Daily Salary": Bartender.day_wage})
        Bartender(fn, ln, age, p, next_id, Bartender.day_wage)

        csvfile.close()

    fle = open("CurrentEmployees.txt", "w+")
    fle.write(
        fn + ", " + ln + ", " + age + ", " + str(p) + ", " + str(
            next_id) + ", " + "Bartender, " + str(Bartender.day_wage) + "\n")
    fle.close()