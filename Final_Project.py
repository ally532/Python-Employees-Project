from Create_Employees import *
import logging
import datetime
from Original_Emp_File import *
import csv
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import webbrowser
import tkinter.scrolledtext


import tkinter.filedialog as filedialog

logger = logging.getLogger("LateLog.log")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("LateLog.log")
logger.addHandler(file_handler)

logging.basicConfig(filename="AttendanceLog.log", level=logging.INFO)



class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.title(self, "Employee Management System")
        tk.Tk.config(self, bg="slategrey")

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}


        for F in (MainMenu, RollCall, ManageEmployees, atten_log, expense_report, remove_employees):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


    def open_manual(self):
        webbrowser.open_new("https://docs.google.com/document/d/1I7rGC4MinyfMwoaTdh0MneBuQkmgPx_XiE9gnvnV-AY/edit")

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        self.config(bg="slategrey")


        attend = tk.Button(self, text="Attendance", width=15, highlightbackground="slategrey", font="none 20 bold", command=lambda: controller.show_frame(RollCall))
        attend.place(relx=0.5, rely=0.30, anchor="center")


        empMan = tk.Button(self, text="Create Employee", width=15, highlightbackground="slategrey", font="none 20 bold", command=lambda: controller.show_frame(ManageEmployees))
        empMan.place(relx=0.5, rely=0.40, anchor="center")

        remEmp = tk.Button(self, text="Remove Employee", width=15, highlightbackground="slategrey", font="none 20 bold",
                           command=lambda: controller.show_frame(remove_employees))
        remEmp.place(relx=0.5, rely=0.50, anchor="center")

        at_log = tk.Button(self, text="Employee Files", width=15, highlightbackground="slategrey", font="none 20 bold", command=lambda: controller.show_frame(atten_log))
        at_log.place(relx=0.5, rely=0.60, anchor="center")

        ex_rep = tk.Button(self, text="Expense Report", width=15, highlightbackground="slategrey", font="none 20 bold",
                           command=lambda: controller.show_frame(expense_report))
        ex_rep.place(relx=0.5, rely=0.70, anchor="center")

        sysman = tk.Button(self, text="System Manual", width=15, highlightbackground="slategrey", font="none 20 bold",
                           command=controller.open_manual)
        sysman.place(relx=0.5, rely=0.80, anchor="center")


class RollCall(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="slategrey")


        self.container = tk.Frame(self)
        self.container.config(bg="slategrey")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.container.grid()

        self.label1 = tk.Label(self.container, text="Employee ID: ", font="none 20", background="slategrey", width=10)
        self.label1.grid(row=0, column=0)

        self.e1 = tk.Entry(self.container, highlightbackground="slategrey", width=10)
        self.e1.grid(row=0, column=1 )


        self.con1 = tk.Frame(self)
        self.con1.config(bg="slategrey", height=40, width=800)
        self.con1.grid()


        clockin = tk.Button(self.con1, text="Clock In", font="none 20 bold", highlightbackground="slategrey", width=10, command=self.clocking_in)
        clockin.grid(row=0, column=3)

        clockout = tk.Button(self.con1, text="Clock Out", font="none 20 bold", highlightbackground="slategrey", width=10, command=self.clocking_out)
        clockout.grid(row=0, column=2)

        button1 = tk.Button(self.con1, text="Menu", font="none 20 bold", highlightbackground="slategrey", width=10,command=lambda: controller.show_frame(MainMenu))
        button1.grid(row=0, column=0)

        clr = tk.Button(self.con1, text="Clear", font="none 20 bold", width=10, highlightbackground="slategrey", command=self.clear_text)
        clr.grid(row=0, column=1)


    def clear_text(self):
        self.e1.delete(0, "end")

    def clocking_in(self):
        now = datetime.datetime.today()
        clocked_in = False

        while not clocked_in:
            try:
                em = self.e1.get()


                if str(em) in DataForAll.emp_IDs:
                    if str(em) not in DataForAll.at_work:
                        DataForAll.at_work.append(em)
                        s2 = now.strftime("%d/%m/%Y, %H:%M:%S")
                        logging.basicConfig(filename=str(em), level=logging.DEBUG)

                        clocked_in = True
                        for i in DataForAll.current_employees:
                            if i.id == int(em):
                                name = i.fn
                                lname = i.ln


                                #late options

                                if now.hour>9 and now.minute>30:
                                    a = (s2 + "\n" + name + " " + lname + ", Employee #" + str(i.id) +"     !!! \n")
                                    messagebox.showinfo("Clocked In", a)

                                    logger.debug(s2+": " +name +" " + lname +", Employee #"+ str(i.id)+"     !!! \n")

                                    # this logs date, time, employee ID - clocked in
                                    fle = open(str(i.id)+".txt", "a+")
                                    fle.write(s2 + ": "+ name +" " + lname +", Employee #"+ str(i.id)+"     !!! \n")
                                    fle.close()
                                    atten_log(None, None).e1.insert(INSERT, em + a)
                                    for i in DataForAll.current_employees:
                                        if em == str(i.id):
                                            exp_list.append([i.fn, i.day_wage])

                                if now.hour>9 and now.minute<30:
                                    a = (s2 + "\n" + name + " " + lname + ", Employee #" + str(i.id) +"     !!! \n")
                                    messagebox.showinfo("Clocked In", a)

                                    logger.debug(s2+": " +name +" " + lname +", Employee #"+ str(i.id)+"     !!! \n")

                                    # this logs date, time, employee ID - clocked in
                                    fle = open(str(i.id)+".txt", "a+")
                                    fle.write(s2 + ": "+ name +" " + lname +", Employee #"+ str(i.id)+"     !!! \n")
                                    fle.close()
                                    atten_log(None, None).e1.insert(INSERT, em + a)
                                    for i in DataForAll.current_employees:
                                        if em == str(i.id):
                                            exp_list.append([i.fn, i.day_wage])

                                #early options

                                elif now.hour<9 and now.minute<30:

                                    a = (s2 + "\n" + name + " " + lname + ", Employee #" + str(
                                        i.id))
                                    messagebox.showinfo("Clocked In", a)
                                    logging.info(s2+": " + name + " " + lname + ", Employee #" + str(
                                        i.id))
                                    # this logs date, time, employee ID - clocked in
                                    fle = open(str(i.id)+".txt", "a+")
                                    fle.write(s2+": " + name + " " + lname + ", Employee #" + str(
                                        i.id) + "\n")
                                    fle.close()
                                    atten_log(None, None).e1.insert(INSERT, em + a)
                                    for i in DataForAll.current_employees:
                                        if em == str(i.id):
                                            exp_list.append([i.fn, i.day_wage])




                                elif now.hour <9 and now.minute>30:

                                    a = (s2 + "\n" + name + " " + lname + ", Employee #" + str(
                                        i.id))
                                    messagebox.showinfo("Clocked In", a)
                                    logging.info(s2 + ": " + name + " " + lname + ", Employee #" + str(
                                        i.id))
                                    # this logs date, time, employee ID - clocked in
                                    fle = open(str(i.id) + ".txt", "a+")
                                    fle.write(s2 + ": " + name + " " + lname + ", Employee #" + str(
                                        i.id) + " \n")
                                    fle.close()
                                    atten_log(None, None).e1.insert(INSERT, em + a)
                                    for i in DataForAll.current_employees:
                                        if em == str(i.id):
                                            exp_list.append([i.fn, i.day_wage])


                                #on time

                                elif now.minute<30 and now.hour ==9:
                                    a = (s2 + "\n" + name + " " + lname + ", Employee #" + str(
                                        i.id))
                                    messagebox.showinfo("Clocked In", a)
                                    logging.info(s2+": " + name + " " + lname + ", Employee #" + str(
                                        i.id))


                                    # this logs date, time, employee ID - clocked in
                                    fle = open(str(i.id)+".txt", "a+")
                                    fle.write(s2+": " + name + " " + lname + ", Employee #" + str(
                                        i.id) + "\n")
                                    fle.close()
                                    atten_log(None, None).e1.insert(INSERT, em + a)
                                    for i in DataForAll.current_employees:
                                        if em == str(i.id):
                                            exp_list.append([i.fn, i.day_wage])


                                        break


                    elif str(em) in DataForAll.at_work:
                        #print("Already clocked in. ")
                        messagebox.showerror("Error", "Employee ID already clocked in.")
                        break


                else:
                    #print("Invalid ID")
                    messagebox.showerror("Error", "The ID you have entered is invalid.")
                    break

            except KeyboardInterrupt:
                print("Keyboard Interrupt")
            except ValueError:
                    print("Value Error")

        self.clear_text()


    def clocking_out(self):


        now = datetime.datetime.today()
        clocked_in = True
        while clocked_in:
            try:
                em = self.e1.get()
                if em in DataForAll.emp_IDs:
                    if em in DataForAll.at_work:
                        DataForAll.at_work.remove(em)
                        s2 = now.strftime("%d/%m/%Y, %H:%M:%S")

                        for i in DataForAll.current_employees:
                            if str(i.id) == str(em):



                                c = s2 + ": " + i.fn + " " + i.ln + ", Employee #" + str(i.id) + " \n"
                                z = s2 + "\n" + i.fn + " " + i.ln + ", Employee #" + str(i.id)

                                messagebox.showinfo("Clocked Out", z)
                                logging.info(c)
                                clocked_in = False



                        #this logs date, time, employee ID - clocked in
                                fle = open(str(i.id)+".txt", "a+")
                                fle.write(c)
                                fle.close()

                                atten_log(None, None).e1.insert(INSERT, em + c)

                    elif str(em) not in DataForAll.at_work:
                        #print("Not clocked in. ")
                        messagebox.showerror("Error", "Employee ID not clocked in.")
                        break


                else:
                    #print("Invalid ID")
                    messagebox.showerror("Error", "The ID you have entered is invalid.")
                    break

            except KeyboardInterrupt:
                print("Keyboard Interrupt")
            except ValueError:
                print("Value Error")

        self.clear_text()

class atten_log(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="slategrey")
        self.container = tk.Frame(self)
        self.container.config(bg="slategrey")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.container.grid()


        self.e1 = tk.Text(self.container, highlightbackground="slategrey", width=90, height=20)
        self.e1.grid(row=0, padx=5, pady=5)


        self.con1 = tk.Frame(self)
        self.con1.config(bg="slategrey", height=40, width=800)
        self.con1.grid()


        button1 = tk.Button(self.con1, text="Menu", font="none 20 bold", highlightbackground="slategrey", width=10, command=lambda: [controller.show_frame(MainMenu),self.clear()])
        button1.grid(row=0, column=0)

        buttonc = tk.Button(self.con1, text="Clear", font="none 20 bold", highlightbackground="slategrey", width=10, command=self.clear)
        buttonc.grid(row=0, column=1)


        button3 = tk.Button(self.con1, text="Staff Files", font="none 20 bold", highlightbackground="slategrey", width=10, command=self.emp_files)
        button3.grid(row=0, column=3)






    def show_log(self):
        filename="AttendanceLog"
        file = open(filename)
        f = file.readlines()
        with open(filename, "r") as f:
            self.e1.insert(INSERT, f.read())

    def clear(self):
        self.e1.delete(1.0, "end")




    def emp_files(self):
        try:
            tk.Frame.fileName = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),("All Files", "*.*")))
            text = open(tk.Frame.fileName).read()
            self.e1.insert(END, text)
        except FileNotFoundError as Exception:
            messagebox.showinfo("File Not Found Error", "No File Selected.")



class ManageEmployees(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="slategrey")


        self.container = tk.Frame(self)
        self.container.config(bg="slategrey")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.container.grid()

        self.label1 = tk.Label(self.container, text="First Name: ", font="none 20", background="slategrey", width=10)
        self.label1.grid(row=0, column=0)

        self.e1 = tk.Entry(self.container, highlightbackground="slategrey", width=10)
        self.e1.grid(row=0, column=1)


        self.label2 = tk.Label(self.container, text="Last Name: ", font="none 20", background="slategrey", width=10)
        self.label2.grid(row=1, column=0)

        self.e2 = tk.Entry(self.container, highlightbackground="slategrey", width=10)
        self.e2.grid(row=1, column=1)



        self.label3 = tk.Label(self.container, text="Age: ", font="none 20", background="slategrey", width=10)
        self.label3.grid(column=0, row=2)

        self.e3 = tk.Entry(self.container, highlightbackground="slategrey", width=10)
        self.e3.grid(row=2, column=1)


        self.label4 = tk.Label(self.container, text="Telephone: ", font="none 20", background="slategrey", width=10)
        self.label4.grid(row=3, column=0)

        self.e4 = tk.Entry(self.container, highlightbackground="slategrey", width=10)
        self.e4.grid(row=3, column=1)

        self.label5 = tk.Label(self.container, text="Position: ", font="none 20", background="slategrey", width=10)
        self.label5.grid(row=4, column=0)

        self.e5 = tk.Entry(self.container, highlightbackground="slategrey", width=10)
        self.e5.grid(row=4, column=1)

        self.con1 = tk.Frame(self)
        self.con1.config(bg="slategrey", height=40, width=800)
        self.con1.grid()

        clockin = tk.Button(self.con1, text="Create", font="none 20 bold", highlightbackground="slategrey", width=10, command=self.append_data)
        clockin.grid(row=0, column=3)

        clockout = tk.Button(self.con1, text="Staff Files", font="none 20 bold", highlightbackground="slategrey", width=10, command=self.emp_files)
        clockout.grid(row=0, column=2)

        button1 = tk.Button(self.con1, text="Menu", font="none 20 bold", highlightbackground="slategrey", width=10, command=lambda: controller.show_frame(MainMenu))
        button1.grid(row=0, column=0)

        clr = tk.Button(self.con1, text="Clear", font="none 20 bold", highlightbackground="slategrey", width=10, command=self.clear_text)
        clr.grid(row=0, column=1)


    def clear_text(self):
        self.e1.delete(0, "end")
        self.e2.delete(0, "end")
        self.e3.delete(0, "end")
        self.e4.delete(0, "end")
        self.e5.delete(0, "end")



    def get_length(self):
        with open("AllEmployees.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            reader_list = list(reader)

            return(len(reader_list))

    def append_data(self):
        try:
            if self.e1.get().isalpha():
                fn = self.e1.get()
            else:
                # print("First name must only contain letters.")
                messagebox.showerror("Entry Error", "First name must only contain letters.")

            if self.e2.get().isalpha():
                ln = self.e2.get()
            else:
                # print("Last name must only contain letters.")
                messagebox.showerror("Field Error", "Last name must only contain letters.")

            if self.e3.get().isdigit() and int(self.e3.get()) < 100 and int(self.e3.get()) >= 18:

                age = self.e3.get()
            else:
                # print("Age must only contain numbers. Age must be between 18 and 100.")
                messagebox.showerror("Field Error", "Age must be a number between 18 and 100.")

            if self.e4.get().isdigit and len(self.e4.get()) == 10:
                if " " not in self.e4.get():
                    phone = self.e4.get()
            else:
                messagebox.showerror("Field Error", "Phone number must be 10 digits.")


            if self.e5.get() in job_titles:
                pass
            else:
                # print("Phone number must contain 10 numbers. Only numbers.")
                messagebox.showerror("Field Error", "Position must be Server or Bartender.")

            fieldnames = ["Firstname", "Lastname", "Phone", "Age", "ID", "Title", "Daily Salary"]
            # num of rows
            next_id = str(100 + self.get_length())
            pos = self.e5.get()
            d_s = ""
            if pos == "Server":
                d_s = Server.day_wage
            elif pos == "Bartender":
                d_s = Bartender.day_wage

            with open("AllEmployees.csv", "a+", newline='') as csvfile:

                if pos == "Server":
                    Server(fn, ln, age, phone, next_id, Server.day_wage)
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow(
                        {"Firstname": fn, "Lastname": ln, "Age": age, "Phone": phone, "ID": next_id, "Title": pos,
                         "Daily Salary": d_s})
                    messagebox.showinfo("Create New Employee",
                                        "Success!\nFirst Name: " + self.e1.get() + "\nLast Name: " + self.e2.get() +
                                        "\nAge: " + self.e3.get() + "\nTelephone: " + self.e4.get() + "\nEmployee ID: " + next_id)

                    fle = open("CurrentEmployees.txt", "a+")
                    fle.write(
                        self.e1.get() + ", " + self.e2.get() + ", " + self.e3.get() + ", " + str(
                            self.e4.get()) + ", " + str(
                            next_id) + ", " + "Server, " + str(Server.day_wage) + "\n")



                    fle.close()


                elif pos == "Bartender":
                    Bartender(fn, ln, age, phone, next_id, Bartender.day_wage)
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow(
                        {"Firstname": fn, "Lastname": ln, "Age": age, "Phone": phone, "ID": next_id, "Title": pos,
                         "Daily Salary": d_s})
                    messagebox.showinfo("Create New Employee",
                                        "Success!\nFirst Name: " + self.e1.get() + "\nLast Name: " + self.e2.get() +
                                        "\nAge: " + self.e3.get() + "\nTelephone: " + self.e4.get() + "\nEmployee ID: " + next_id)

                    fle = open("CurrentEmployees.txt", "a+")
                    fle.write(
                        self.e1.get() + ", " + self.e2.get() + ", " + self.e3.get() + ", " + str(self.e4.get()) + ", " + str(
                            next_id) + ", " + "Bartender, " + str(Bartender.day_wage) + "\n")
                    fle.close()

        except UnboundLocalError:
            #print("Must enter all fields.")
            messagebox.showerror("Field Error", "Must enter all fields.")


        self.clear_text()


    def emp_files(self):
        try:
            tk.Frame.fileName = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),("All Files", "*.*")))
            text = open(tk.Frame.fileName).read()
            self.e1.insert(END, text)
        except FileNotFoundError as Exception:
            messagebox.showinfo("File Not Found Error", "No File Selected.")







class remove_employees(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="slategrey")

        self.container = tk.Frame(self)
        self.container.config(bg="slategrey")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.container.grid()

        self.label1 = tk.Label(self.container, text="First Name: ", font="none 20", background="slategrey", width=10)
        self.label1.grid(row=0, column=0)

        self.e1 = tk.Entry(self.container, highlightbackground="slategrey", width=10)
        self.e1.grid(row=0, column=1)

        self.label2 = tk.Label(self.container, text="Last Name: ", font="none 20", background="slategrey", width=10)
        self.label2.grid(row=1, column=0)

        self.e2 = tk.Entry(self.container, highlightbackground="slategrey", width=10)
        self.e2.grid(row=1, column=1)

        self.label3 = tk.Label(self.container, text="Employee ID: ", font="none 20", background="slategrey", width=10)
        self.label3.grid(row=2, column=0)

        self.e3 = tk.Entry(self.container, highlightbackground="slategrey", width=10)
        self.e3.grid(row=2, column=1)


        self.con1 = tk.Frame(self)
        self.con1.config(bg="slategrey", height=40, width=800)
        self.con1.grid()

        clockin = tk.Button(self.con1, text="Staff Files", font="none 20 bold", highlightbackground="slategrey", width=10,
                            command=self.emp_files)
        clockin.grid(row=0, column=3)

        clockout = tk.Button(self.con1, text="Remove", font="none 20 bold", highlightbackground="slategrey", width=10,
                             command=self.remove_employee)
        clockout.grid(row=0, column=2)

        button1 = tk.Button(self.con1, text="Menu", font="none 20 bold", highlightbackground="slategrey", width=10,
                            command=lambda: controller.show_frame(MainMenu))
        button1.grid(row=0, column=0)

        clr = tk.Button(self.con1, text="Clear", font="none 20 bold", highlightbackground="slategrey", width=10, command=self.clear_text)
        clr.grid(row=0, column=1)

    def clear_text(self):
        self.e1.delete(0, "end")
        self.e2.delete(0, "end")
        self.e3.delete(0, "end")


    def get_length(self):
        with open("AllEmployees.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            reader_list = list(reader)

            return (len(reader_list))



    def remove_employee(self):
        try:

            if self.e1.get() == "" or self.e2.get() == "" or self.e3.get() == "":
                messagebox.showerror("Field Error", "Must Enter All Fields.")

            if self.e1.get().isalpha() == False or self.e2.get().isalpha() == False:
                messagebox.showerror("Field Error", "First and last name must only contain letters.")

            if self.e3.get() not in DataForAll.emp_IDs:
                messagebox.showerror("Field Error", "Invalid Employee ID. ")        

            elif self.e1.get().isalpha() and self.e2.get().isalpha() and self.e3.get().isalpha() == False:

                    fn = self.e1.get()
                    ln = self.e2.get()
                    id = self.e3.get()

                    if id not in DataForAll.emp_IDs:
                        messagebox.showerror("Field Error", "Invalid Employee ID. ")


                    for a in DataForAll.current_employees:
                        if id not in DataForAll.emp_IDs:
                            messagebox.showerror("Field Error", "Invalid Employee ID. ")
                            break
                        elif fn == a.fn and ln == a.ln and str(id) == str(a.id):
                            DataForAll.current_employees.remove(a)
                            DataForAll.emp_IDs.remove(str(a.id))



                            with open("CurrentEmployees.txt", "r") as f:
                                lines = f.readlines()
                            with open("CurrentEmployees.txt", "w") as f:
                                for line in lines:
                                    if self.e1.get() and self.e2.get() not in line:
                                        f.write(line)
                            self.clear_text()
                            messagebox.showinfo("Employee Removed",
                                                "Employee " + a.fn + " " + a.ln + " with ID# " + str(
                                                    a.id) + " has been removed. ")

                            break


            else:
                messagebox.showerror("Field Error", "Invalid First or Last Name.")









        except UnboundLocalError:
            messagebox.showerror("Field Error", "Must enter all fields.")
        self.clear_text()








    def emp_files(self):
        try:
            tk.Frame.fileName = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),("All Files", "*.*")))
            text = open(tk.Frame.fileName).read()
            self.e1.insert(END, text)
        except FileNotFoundError as Exception:
            messagebox.showinfo("File Not Found Error", "No File Selected.")




class expense_report(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="slategrey")
        self.container = tk.Frame(self)
        self.container.config(bg="slategrey")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.container.grid()


        self.e1 = tk.Text(self.container, highlightbackground="slategrey", width=90, height=20)
        self.e1.grid(row=0, padx=5, pady=5)


        self.con1 = tk.Frame(self)
        self.con1.config(bg="slategrey", height=40, width=800)
        self.con1.grid()


        button1 = tk.Button(self.con1, text="Menu", font="none 20 bold", highlightbackground="slategrey", width=10,command=lambda: [controller.show_frame(MainMenu),self.clear()])
        button1.grid(row=0, column=0)


        button2 = tk.Button(self.con1, text="Update", font="none 20 bold", highlightbackground="slategrey", width=10, command=self.calc_expenses)
        button2.grid(row=0, column=1)

        button3 = tk.Button(self.con1, text="Display Log", font="none 20 bold", highlightbackground="slategrey", width=10, command=self.show_expenses)
        button3.grid(row=0, column=2)


    def calc_expenses(self):
        now = datetime.datetime.today()
        s2 = now.strftime("%d/%m/%Y, %H:%M:%S")
        with open("Expense Report", "a+") as f:
            f.write(s2 + ": Employee, Daily Wage - " + str(exp_list) +"\n" +"Expense total = " + str(sum(i[1] for i in exp_list)) + "\n")
            f.close()
        exp_list.clear()

    def show_expenses(self):
        filename="Expense Report"
        file = open(filename)
        f = file.readlines()
        with open(filename, "r") as f:
            self.e1.insert(INSERT, f.read())

    def clear(self):
        self.e1.delete(1.0, "end")





e()
gui = MainFrame()
gui.geometry("900x400")





gui.mainloop()



# fix display (centered, etc)


#### MAKE FILE WITH CURRENT EMPLOYEE NAMES AND INFO THAT IS UPDATED WHEN REMOVING AND UPDATING NEW EMPS
## DATA.CSV WILL BE USED AS THE ALLEMPSEVER FILE 