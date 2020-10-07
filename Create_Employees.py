# Final Project 17.10.19
# This file creates the Employee and DataForAll classes

job_titles = ["Server", "Bartender"]
exp_list = []

class Employee():
    def __init__(self, fn, ln, age, num, id):

        self.fn = fn
        self.ln = ln
        self.age = age
        self.num = num
        self.id = DataForAll.count



class Server(Employee):
    day_wage = 250

    def __init__(self, fn, ln, age, num, id, day_wage):
        Employee.__init__(self, fn, ln, age, num, id)

        self.fn = fn
        self.ln = ln
        self.age = age
        self.num = num
        self.id = DataForAll.count
        self.day_wage = day_wage

        DataForAll.count +=1
        DataForAll.all_emps_list.append(self)
        DataForAll.current_employees.append(self)
        DataForAll.emp_IDs.append(id)

        #fle = open("CurrentEmployees.txt", "a+")
        #fle.write(
        #    self.fn + ", " + self.ln + ", " + self.age + ", " + str(self.num) + ", " + str(
        #        self.id) + ", " + "Server, " + str(self.day_wage) + "\n")
        #fle.close()


class Bartender(Employee):

    day_wage = 300

    def __init__(self, fn, ln, age, num, id, day_wage):
        Employee.__init__(self, fn, ln, age, num, id)
        self.fn = fn
        self.ln = ln
        self.age = age
        self.num = num
        self.id = DataForAll.count
        self.day_wage = day_wage

        DataForAll.count +=1
        DataForAll.all_emps_list.append(self)
        DataForAll.current_employees.append(self)
        DataForAll.emp_IDs.append(id)
        #fle = open("CurrentEmployees.txt", "a+")
        #fle.write(
        #self.fn + ", " + self.ln + ", " + self.age + ", " + str(self.num) + ", " + str(self.id) + ", " + "Bartender, " +str(self.day_wage)+ "\n")
        #fle.close()





class DataForAll():
    count = 100
    all_emps_list = []
    current_employees = []
    emp_IDs = []
    emp_names = []
    at_work=[]

    def __init__(self):
        pass



    def adding_self(self):
        DataForAll.all_emps_list.append(self)







def create_manually():
    fn = input("Firstname: ")
    ln = input("Lastname: ")
    age = input("Age: ")
    num = input("Phone Number: ")

    Employee(fn, ln, age, num, id)

def delete_emp():
    emp = input("Firstname: ")
    emp_ln = input("Lastname: ")
    for i in DataForAll.current_employees:
        if (emp + " "+ emp_ln) in DataForAll.current_employees:
            DataForAll.current_employees.remove(emp + " "+ emp_ln)


def add_exp(a):
    for i in DataForAll.current_employees:
        if a == i.id:
            exp_list.append([a.fn, a.day_wage])
