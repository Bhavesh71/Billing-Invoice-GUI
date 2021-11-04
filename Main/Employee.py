from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter import ttk
import datetime
# import mysql.connector as mysql
import sqlite3

# Creating Mysql connection
dbconn = sqlite3.connect("./Database/RSgroceries.db")


# Create a cursor to give commands
cursor = dbconn.cursor()

# Create Tables
# category Table
cursor.execute("""CREATE TABLE if not exists category(
category varchar(100) NOT NULL primary key
    )
    """)
dbconn.commit()
cursor.execute("""CREATE TABLE if not exists products(
    product_id int  not null primary key,
    product_name varchar(100) not null,
    product_rate int not null,
    category varchar(100) not null references category(category)
    )
    """)
dbconn.commit()



cursor.execute("""
Select * From category
""")
Category_1 = cursor.fetchall()

# Creating TKinter Window
billing = Tk()
billing.geometry("1330x750")
billing.resizable(0, 0)
billing.iconbitmap("./images/Logo.ico")
billing.title("Employee")
font_1 = Font(family="Calibri",size=15,weight="bold")


# Fixing GUI Background
Background = PhotoImage(file="./images/Employee_bg.png")
Bg_label = Label(billing, image=Background)
Bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Logout command
def Exit():
    sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=billing)
    if sure == True:
        billing.destroy()

# Creating logout button
logout_img = PhotoImage(file="./images/logout.png")
logout_button = Button(billing, image=logout_img, borderwidth=0,relief="flat",overrelief="flat", command=Exit)
logout_button.place(relx=0.0155, rely=0.038,width=39,height=31)

"______________________________________________________________________________________________________________________"

# Creating invoice
invoice = ttk.Treeview(billing)
invoice["columns"] = ("Product Name", "Qty", "Rate", "Cost")

invoice.column("#0", width=0,stretch=NO)
invoice.column("#1", width=301,anchor="center")
invoice.column("#2", width=80,anchor="center")
invoice.column("#3",width=120,anchor="center")
invoice.column("#4",width=120,anchor="center")

invoice.heading("#0",text="")
invoice.heading("#1",text="Product Name")
invoice.heading("#2",text="Qty")
invoice.heading("#3",text="Rate")
invoice.heading("#4",text="Cost")
invoice.place(relx=0.5032,rely=0.4517,height=245)

Scroll_invoice = Scrollbar(orient="vertical",command=invoice.yview)
invoice.configure(yscroll=Scroll_invoice.set)
Scroll_invoice.place(relx=0.9593,rely=0.4537, height=275)
"______________________________________________________________________________________________________________________"

# Creating all the entry fields
# Creating Entry for name and contact
# Name
Name_entry = Entry(billing,font=font_1,relief="flat",bg="#0089fe")
Name_entry.bind("")
Name_entry.place(relx=0.619,rely=0.124,width=140,height=30)
# Contact
contact_entry = Entry(billing,font=font_1,relief="flat",bg="#0089fe")
contact_entry.place(relx=0.869,rely=0.124,width=140,height=30)

# Creating entry for product and quantity
# List of categories
category = ["Choose the Category"]
for cat_n in Category_1:
    category.append(cat_n[0])




# defining required functions
global Rate
global Final_prod
Rate = []
Final_prod = ["Choose product"]
def sel_cat(n):
    global Rate
    global Final_prod
    if Items.get() == "" or Items.get() == "Choose the Category":
        Items_1.configure(values=Final_prod)
        Items_1.current(0)

    cursor.execute("SELECT product_name, product_rate FROM products WHERE category='{}'".format(Items.get()))
    prod_and_rate = cursor.fetchall()
    prods = ["Choose product"]
    rates = []
    for i in prod_and_rate:
        prods.append(i[0])
        rates.append(i[1])
    Final_prod=prods
    Rate=rates
    Items_1.configure(value=Final_prod)
    Items_1.current(0)
    # Rate = []
    # Final_prod = ["Choose product"]
    # print(Final_prod)
    # print(Rate)




# Items category Drop Down
Items = ttk.Combobox(billing,values=category,font=font_1)
Items.current(0)
Items.place(relx=0.049,rely=0.355,width=428,height=53)

# Bind Items
Items.bind("<<ComboboxSelected>>", sel_cat)

# Product drop down
Items_1 = ttk.Combobox(billing, values=["Choose product"],font=font_1)
Items_1.current(0)
Items_1.place(relx=0.049,rely=0.536,width=430,height=53)


# Creating entry box for quantity
quantity_entry = Entry(billing,font=font_1,relief="flat")
quantity_entry.place(relx=0.050,rely=0.730,width=423,height=48)
"______________________________________________________________________________________________________________________"

# Defining Funtions
# Non billing commands
# Add to Cart
def add_to_cart():
    global Final_prod
    global Rate
    if (quantity_entry.get().isdigit()) or (quantity_entry.get()== ""):
        if (Items_1.get()!="" and quantity_entry.get()!="" and Items.get().lower()!="choose the category" and Items_1.get()!="Choose product"):
            n = Final_prod.index(Items_1.get())
            rate_n = Rate[n - 1]
            if Items.get() in category:
                invoice.insert("",index="end",values=(Items_1.get(),quantity_entry.get(),rate_n,int(quantity_entry.get())*rate_n))
                Items.current(0)
                quantity_entry.delete(0,END)
                Items_1.current(0)
                # Rate = []
                # Final_prod = ["Choose product"]
            else:
                messagebox.showerror("Error","Item not in the cart!")
        else:
            messagebox.showerror("Error", "Please fill the details")

    else:
        messagebox.showerror("Error", "Please Enter Correct Quantity!")

# Clear
def clear():
    Items.current(0)
    quantity_entry.delete(0, END)
    Items_1.current(0)

# Billing commands

font_3 = Font(family="Calibri",size=11,weight="bold")

global cust_name
global cust_contact
global date_time
global cust_no
global Total_n
global dummy
cust_name = ""
cust_contact = ""
date_time = ""
cust_no = ""
Total_n = ""
dummy = 0
def generate_bill():
    all_rec = invoice.get_children()
    Rows = []
    for rec in all_rec:
        values = invoice.item(rec).get("values")
        Rows.append(values)
    confirm_1 = messagebox.askyesno("Generate Bill", "Do you want to generate bill?")
    if confirm_1 == 1:
        if Name_entry.get() != "" and contact_entry.get() != "":
            if Rows!=[]:
                costs_n = []
                if len(contact_entry.get()) == 10:
                    Delete_btn.configure(state="disabled")
                    global cust_name
                    global cust_contact
                    global date_time
                    global cust_no
                    global Total_n
                    global dummy
                    dummy = 1
                    all_rec = invoice.get_children()
                    for rec in all_rec:
                        values = invoice.item(rec).get("values")
                        costs_n.append(values[3])
                    Total_n = sum(costs_n)
                    # Customer number reading and writing from/to(respectively) a file
                    cust_no_read = open("Customer_number_counter.txt", "r")
                    count = cust_no_read.read()
                    cust_no_read.close()
                    cust_no = count
                    cust_no_write = open("Customer_number_counter.txt", "w")
                    count_inc = str(int(count) + 1)
                    cust_no_write.write(count_inc)
                    cust_no_write.close()

                    # Other labels
                    cust_name=Name_entry.get()
                    cust_contact=contact_entry.get()
                    date_time = datetime.datetime.now()
                    # Adding customer name
                    label_1 = Label(billing, text=cust_name, font=font_3, bg="#dae2f2", anchor="w")
                    label_1.place(relx=0.602, rely=0.368, width=250, height=40)

                    # Adding customer number
                    label_2 = Label(billing, text=cust_no, font=font_3, bg="#dae2f2", anchor="w")
                    label_2.place(relx=0.593, rely=0.423, width=70, height=15)

                    # Adding customer contact
                    label_3 = Label(billing, text=cust_contact, font=font_3,bg="#dae2f2", anchor="w")
                    label_3.place(relx=0.899,rely=0.368, width=80, height=40)

                    # Adding date and time
                    label_4 = Label(billing, text=date_time, font=font_3, bg="#dae2f2", anchor="w")
                    label_4.place(relx=0.886, rely=0.423, width=104, height=15)

                    # Total
                    font_4 = Font(family="Calibri", size=18, weight="bold")
                    label_5 = Label(billing, text="Total = {}".format(Total_n), font=font_4, bg="#ffffff", anchor="e")
                    label_5.place(relx=0.800, rely=0.780, width=200, height=31)
                    Name_entry.delete(0,END)
                    contact_entry.delete(0,END)

                else:
                    messagebox.showerror("Error", "Please enter correct contact number")
            else:
                messagebox.showerror("Error", "Cart is empty")
        else:
            messagebox.showerror("Error", "Fill the details of the customer")
    else:
        pass

# Clear function definition
def clear_all():
    Delete_btn.configure(state="active")
    all_rec = invoice.get_children()
    Rows = []
    for rec in all_rec:
        values = invoice.item(rec).get("values")
        Rows.append(values)
    if Rows == []:
        messagebox.showerror("Error","Cart is already empty")
    else:
        # Overwriting customer name
        label_1 = Label(billing, text="", font=font_3, bg="#dae2f2", anchor="w")
        label_1.place(relx=0.602, rely=0.368, width=250, height=40)

        # Overwriting customer number
        label_2 = Label(billing, text="", font=font_3, bg="#dae2f2", anchor="w")
        label_2.place(relx=0.593, rely=0.423, width=70, height=15)

        # Overwriting customer contact
        label_3 = Label(billing, text="", font=font_3, bg="#dae2f2", anchor="w")
        label_3.place(relx=0.899, rely=0.368, width=80, height=40)

        # Overwriting date and time
        label_4 = Label(billing, text="", font=font_3, bg="#dae2f2", anchor="w")
        label_4.place(relx=0.886, rely=0.423, width=104, height=15)

        # Overwriting
        font_4 = Font(family="Calibri", size=18, weight="bold")
        label_5 = Label(billing, text="", font=font_4, bg="#ffffff", anchor="e")
        label_5.place(relx=0.800, rely=0.780, width=200, height=31)
        for rows in invoice.get_children():
            invoice.delete(rows)
        Save_btn.configure(state="active")
        Generate_btn.configure(state="active")
        Delete_btn.configure(state="active")


def delete_many():
    items_n = invoice.selection()
    if items_n == ():
        messagebox.showerror("Error","No Item(s) selected")
    else:
        for rows_n in items_n:
            invoice.delete(rows_n)



def save_bill():
    global cust_name
    global cust_contact
    global date_time
    global cust_no
    global Total_n
    global dummy
    all_rec = invoice.get_children()
    if dummy == 0:
        messagebox.showerror("Error", "Please Generate the bill first")
    else:
        yes_no = messagebox.askyesno("Save Bill", "Are you sure you want to Save Bill?")
        if yes_no == 1:
            Delete_btn.configure(state="active")
            bill_n = open("./All_bills/zBill_{}.txt".format(cust_no), "w")
            cust_det = [cust_name, cust_contact, cust_no, date_time,Total_n]
            for i in cust_det:
                bill_n.write(str(i) + "`")
            bill_n.write("\n")
            all_rec = invoice.get_children()
            for rec in all_rec:
                values = invoice.item(rec).get("values")
                for j in values:
                    bill_n.write(str(j) + "`")
                bill_n.write("\n")
            cust_name = ""
            cust_contact = ""
            date_time = ""
            cust_no = ""
            Total_n = ""
            clear_all()
            dummy = 0
        else:
            pass



"______________________________________________________________________________________________________________________"
# Creating main button widgets
# ***** Non billing widgets *****
# Add to invoice
Add_btn_1 = Button(billing,text="Add to cart",bg="#ff1616",fg="black",font=font_1,command=add_to_cart)
Add_btn_1.configure(activebackground="#ff1616")
Add_btn_1.configure(activeforeground="black")
Add_btn_1.configure(relief="flat")
Add_btn_1.configure(borderwidth="0")
Add_btn_1.place(relx=0.064,rely=0.882,width=135,height=43)

# Clear
Clear_btn_1 = Button(billing,text="Clear",bg="#ff1616",fg="black",font=font_1,command=clear)
Clear_btn_1.configure(activebackground="#ff1616")
Clear_btn_1.configure(activeforeground="black")
Clear_btn_1.configure(relief="flat")
Clear_btn_1.configure(borderwidth="0")
Clear_btn_1.place(relx=0.256,rely=0.882,width=135,height=43)



# ***** Billing widgets *****
font_2 = Font(family="Calibri",size=13,weight="bold")
# Save bill
Save_btn = Button(billing, text="Save Bill", bg="#ff1616",fg="black",font=font_2, command=save_bill)
Save_btn.configure(activebackground="#ff1616")
Save_btn.configure(activeforeground="black")
Save_btn.configure(relief="flat")
Save_btn.configure(borderwidth="0")
Save_btn.place(relx=0.861,rely=0.887,width=135,height=43)


# Generate Bill
Generate_btn=Button(billing,text="Generate Invoice",bg="#ff1616",fg="black",font=font_2,command=generate_bill)
Generate_btn.configure(activebackground="#ff1616")
Generate_btn.configure(activeforeground="black")
Generate_btn.configure(relief="flat")
Generate_btn.configure(borderwidth="0")
Generate_btn.place(relx=0.5165,rely=0.887,width=135,height=43)

# Delete Item
Delete_btn=Button(billing,text="Delete Item(s)",bg="#ff1616",fg="black",font=font_2, command=delete_many)
Delete_btn.configure(activebackground="#ff1616")
Delete_btn.configure(activeforeground="black")
Delete_btn.configure(relief="flat")
Delete_btn.configure(borderwidth="0")
Delete_btn.place(relx=0.631,rely=0.887,width=135,height=43)

# Clear Items
Clear_btn_2=Button(billing,text="Clear",bg="#ff1616",fg="black",font=font_2, command=clear_all)
Clear_btn_2.configure(activebackground="#ff1616")
Clear_btn_2.configure(activeforeground="black")
Clear_btn_2.configure(relief="flat")
Clear_btn_2.configure(borderwidth="0")
Clear_btn_2.place(relx=0.745,rely=0.887,width=135,height=43)

"______________________________________________________________________________________________________________________"
# Search Bills
# Defining funciton for searching bill
def search_bill():
    for rows in invoice.get_children():
        invoice.delete(rows)
    bill_no_2 = Cust_no_entry.get()
    try:
        # Getting and adding other details
        bill = open("./All_bills/zBill_{}.txt".format(bill_no_2),"r")
        other_details = bill.readline().split("`")
        customer_name = other_details[0]
        customer_contact = other_details[1]
        customer_id = bill_no_2
        date_time_n = other_details[3]
        Total_bill = other_details[4]
        # writing customer name
        label_1 = Label(billing, text=customer_name, font=font_3, bg="#dae2f2", anchor="w")
        label_1.place(relx=0.602, rely=0.368, width=250, height=40)

        # writing customer number
        label_2 = Label(billing, text=customer_id, font=font_3, bg="#dae2f2", anchor="w")
        label_2.place(relx=0.593, rely=0.423, width=70, height=15)

        # writing customer contact
        label_3 = Label(billing, text=customer_contact, font=font_3, bg="#dae2f2", anchor="w")
        label_3.place(relx=0.899, rely=0.368, width=80, height=40)

        # writing date and time
        label_4 = Label(billing, text=date_time_n, font=font_3, bg="#dae2f2", anchor="w")
        label_4.place(relx=0.886, rely=0.423, width=104, height=15)

        # writing Total
        font_4 = Font(family="Calibri", size=18, weight="bold")
        label_5 = Label(billing, text="Total = {}".format(Total_bill), font=font_4, bg="#ffffff", anchor="e")
        label_5.place(relx=0.800, rely=0.780, width=200, height=31)

        # Reading records
        records = bill.readlines()
        for i in records:
            splitted = i.split("`")
            invoice.insert("", index="end", values=(splitted[0],splitted[1],splitted[2],splitted[3]))
            Save_btn.configure(state="disabled")
            Generate_btn.configure(state="disabled")
            Delete_btn.configure(state="disabled")

    except FileNotFoundError:
        messagebox.showerror("Error","No such Bill")
    Cust_no_entry.delete(0, END)


# Creating search button
search_img = PhotoImage(file="./images/search.png")
search_button = Button(billing, image=search_img, borderwidth=0,relief="flat",overrelief="flat",command=search_bill)
search_button.place(relx=0.3613, rely=0.1202)

# Creating entry box for search bill
Cust_no_entry = Entry(billing,font=font_1,relief="flat")
Cust_no_entry.place(relx=0.148,rely=0.12,width=261,height=40)


def Exit():
    sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=billing)
    if sure == True:
        billing.destroy()

billing.protocol("WM_DELETE_WINDOW", Exit)

# dbconn.close()
billing.mainloop()
