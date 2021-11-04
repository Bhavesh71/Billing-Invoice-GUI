from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter import ttk
# import mysql.connector as mysql
import sqlite3

# Creating Tkinter Window
Admin = Tk()
Admin.geometry("1330x750")
Admin.resizable(0, 0)
Admin.iconbitmap("./images/Logo.ico")
Admin.title("Admin")

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

cursor.execute("SELECT * FROM products")
prod_1 = cursor.fetchall()
# print(prod_1)
dbconn.commit()



# Fixing GUI Background
Background = PhotoImage(file="./images/Admin_bg.png")
Bg_label = Label(Admin, image=Background)
Bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Creating invoice
table = ttk.Treeview(Admin)
table["columns"] = ("ID","Product Name","Category", "Rate")

table.column("#0", width=0,stretch=NO)
table.column("#1", width=50,anchor="center")
table.column("#2", width=230,anchor="center")
table.column("#3",width=230,anchor="center")
table.column("#4",width=120,anchor="center")

table.heading("#0",text="")
table.heading("#1",text="ID")
table.heading("#2",text="Product Name")
table.heading("#3",text="Category")
table.heading("#4",text="Rate")
table.place(relx=0.50,rely=0.1139,height=528.8, width=630)

Scroll_invoice = Scrollbar(orient="vertical",command=table.yview)
table.configure(yscroll=Scroll_invoice.set)
Scroll_invoice.place(relx=0.961,rely=0.1140, height=527.3)

for row in prod_1:
    table.insert("",index="end",values=(row[0],row[1],row[3],row[2]))
# Defining Exit function
def Exit():
    sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=Admin)
    if sure == True:
        Admin.destroy()
        # adm.destroy()


# Creating logout button
logout_img = PhotoImage(file="./images/logout.png")
logout_button = Button(Admin, image=logout_img, borderwidth=0,relief="flat",overrelief="flat", command=Exit)
logout_button.place(relx=0.0155, rely=0.038,width=39,height=31)


# Creating all the required widgets
# Creating text variables
cat = StringVar()
pro_name = StringVar()
pro_rate = StringVar()

font_1 = Font(family="Calibri",size=15,weight="bold")
# All Entry widgets
# Product Category Widget
Entry_1 = Entry(Admin,font=font_1,relief="flat",bg="#fefffe")
Entry_1.place(relx=0.043,rely=0.622,width=423,height=50)

# Product Rate Widget
Entry_2 = Entry(Admin, font=font_1,relief="flat",bg="#fefffe")
Entry_2.place(relx=0.043,rely=0.780,width=423,height=50)

# Product Name Widget
Entry_3 = Entry(Admin,font=font_1,relief="flat",bg="#fefffe")
Entry_3.place(relx=0.043,rely=0.463,width=423,height=50)

# Product Id Widget
Entry_4 = Entry(Admin,font=font_1,relief="flat",bg="#fefffe")
Entry_4.place(relx=0.043,rely=0.3205,width=423,height=50)

# Search code Entry Widget
Entry_5 = Entry(Admin, font=font_1,relief="flat",bg="#fefafa")
Entry_5.place(relx=0.161,rely=0.115,width=255,height=40)


# Defining all the required functions
# CREATING FUNCTION TO REMOVE UNWANTED CATEGORY
def unwanted_cat():
    category_delete_1 = table.get_children()
    categories_avail = []
    for rec in category_delete_1:
        values = table.item(rec).get("values")[2]
        categories_avail.append(values)
    cursor.execute("SELECT category FROM category")
    cat_t = cursor.fetchall()
    all_cat = []
    for i in cat_t:
        all_cat.append(i[0])
    available_category = []
    for fin in all_cat:
        if fin in categories_avail:
            available_category.append(fin)
        else:
            pass
    cursor.execute("DROP TABLE category")
    dbconn.commit()
    # Creating table product if not exist
    cursor.execute("""CREATE TABLE if not exists category(
       category varchar(100) NOT NULL primary key
           )
           """)
    dbconn.commit()
    for last in available_category:
        try:
            cursor.execute("INSERT INTO category VALUES('{}')".format(last))
            dbconn.commit()
        except sqlite3.IntegrityError:
            pass


# Add to cart
def add_to_cart():
    # Creating table product if not exist
    cursor.execute("""CREATE TABLE if not exists category(
    category varchar(100) NOT NULL primary key
        )
        """)
    cursor.execute("""CREATE TABLE if not exists products(
        product_id int  not null primary key,
        product_name varchar(100) not null,
        product_rate int not null,
        category varchar(100) not null references category(category)
        )
        """)
    dbconn.commit()
    all_rec = table.get_children()
    ids = []
    for rec in all_rec:
        values = table.item(rec).get("values")[0]
        ids.append(values)
    if (Entry_2.get().isdigit() or Entry_2.get()==""):
        try:
            if Entry_1.get() != "" and Entry_2.get() != "" and Entry_3.get() != "" and Entry_4.get() != "":
                n = messagebox.askyesno("Add to Market", "Are you sure you want to add it to the Market?")
                if n == 1:
                    cursor.execute("SELECT product_id FROM products")
                    id_check = cursor.fetchall()
                    id_check_fin = []
                    dbconn.commit()
                    if (int(Entry_4.get()),) in id_check:
                        messagebox.showerror("Error", "Product id already in the market")
                    else:
                        table.insert("", index="end", values=(Entry_4.get(), Entry_3.get(), Entry_1.get(), Entry_2.get()))
                        cursor.execute("INSERT INTO products VALUES(:product_id, :product_name, :product_rate, :category)",
                                       {
                                           "product_id": Entry_4.get(),
                                           "product_name": Entry_3.get(),
                                           "product_rate": Entry_2.get(),
                                           "category": Entry_1.get()
                                       }
                                       )
                        cursor.execute("SELECT category FROM category")
                        categories_db = cursor.fetchall()
                        categories = []
                        for i in categories_db:
                            categories.append(i[0])
                        if Entry_1.get() not in categories:
                            cursor.execute("INSERT INTO category VALUES(:category)",
                                           {"category": Entry_1.get()})
                            dbconn.commit()
                        else:
                            pass
                        dbconn.commit()
                        Entry_1.delete(0, END)
                        Entry_2.delete(0, END)
                        Entry_3.delete(0, END)
                        Entry_4.delete(0, END)
                        unwanted_cat()

                else:
                    pass
            else:
                messagebox.showerror("Error", "Please fill the details")
        except ValueError:
            messagebox.showerror("Error", "Please enter correct product ID!")
    else:
        Entry_2.delete(0, END)
        messagebox.showerror("Error", "Please enter correct quantity!")

# Update
def update():
    # Creating table product if not exist
    cursor.execute("""CREATE TABLE if not exists category(
        category varchar(100) NOT NULL primary key
            )
            """)
    cursor.execute("""CREATE TABLE if not exists products(
        product_id int  not null primary key,
        product_name varchar(100) not null,
        product_rate int not null,
        category varchar(100) not null references category(category)
        )
        """)
    dbconn.commit()

    Button_1.configure(state="active")
    if Entry_1.get() != "" and Entry_2.get() != "" and Entry_3.get() != "" and Entry_4.get() != "":
        cursor.execute("SELECT product_id FROM products")
        id_check = cursor.fetchall()
        dbconn.commit()
        if (int(Entry_4.get()),) in id_check:
            all_rows = table.get_children()
            k = []
            for i in all_rows:
                if table.item(i).get("values")[0] == int(Entry_4.get()):
                    k.append(i)
                else:
                    pass
            table.item(k[0], text="", values=(int(Entry_4.get()) ,Entry_3.get(), Entry_1.get(), Entry_2.get()))
            cursor.execute("""
            UPDATE products SET product_name = '{}', category = '{}', product_rate = {} WHERE product_id = {}"""
                           .format(Entry_3.get(), Entry_1.get(), Entry_2.get(), int(Entry_4.get())))
            dbconn.commit()
            cursor.execute("SELECT category FROM category")
            categories_db = cursor.fetchall()
            categories = []
            for i in categories_db:
                categories.append(i[0])
            if Entry_1.get() not in categories:
                cursor.execute("INSERT INTO category VALUES(:category)",
                               {"category": Entry_1.get()})
                dbconn.commit()
            Entry_1.delete(0, END)
            Entry_2.delete(0, END)
            Entry_3.delete(0, END)
            Entry_4.delete(0, END)
            unwanted_cat()

        else:
            messagebox.showerror("Error", "Product ID not in the market")
    else:
        messagebox.showerror("Error", "Fill all the details")

# Clear
def clear():
    # Creating table product if not exist
    cursor.execute("""CREATE TABLE if not exists category(
        category varchar(100) NOT NULL primary key
            )
            """)
    cursor.execute("""CREATE TABLE if not exists products(
        product_id int  not null primary key,
        product_name varchar(100) not null,
        product_rate int not null,
        category varchar(100) not null references category(category)
        )
        """)
    dbconn.commit()

    Entry_1.delete(0, END)
    Entry_2.delete(0, END)
    Entry_3.delete(0, END)
    Entry_4.delete(0, END)
    Button_1.configure(state="active")
    unwanted_cat()

# Select Item
def select_item():
    # Creating table product if not exist
    cursor.execute("""CREATE TABLE if not exists category(
        category varchar(100) NOT NULL primary key
            )
            """)
    cursor.execute("""CREATE TABLE if not exists products(
        product_id int  not null primary key,
        product_name varchar(100) not null,
        product_rate int not null,
        category varchar(100) not null references category(category)
        )
        """)
    dbconn.commit()

    items_n = table.selection()
    if len(items_n)>1:
        messagebox.showerror("Error", "Two or more items are selected")
    else:
        if items_n == ():
            messagebox.showerror("Error", "No Item(s) selected")
        else:
            Entry_1.delete(0, END)
            Entry_2.delete(0, END)
            Entry_3.delete(0, END)
            Entry_4.delete(0, END)
            sel_item = []
            for i in items_n:
                k = table.item(i, "values")
                for j in k:
                    sel_item.append(j)
            Entry_4.insert(0, sel_item[0])
            Entry_3.insert(0, sel_item[1])
            Entry_2.insert(0, sel_item[3])
            Entry_1.insert(0, sel_item[2])
            unwanted_cat()
            Button_1.configure(state="disabled")

# Delete item(s)
def delete_many():
    # Creating table product if not exist
    cursor.execute("""CREATE TABLE if not exists category(
        category varchar(100) NOT NULL primary key
            )
            """)
    cursor.execute("""CREATE TABLE if not exists products(
        product_id int  not null primary key,
        product_name varchar(100) not null,
        product_rate int not null,
        category varchar(100) not null references category(category)
        )
        """)
    dbconn.commit()

    items_n = table.selection()
    if items_n == ():
        messagebox.showerror("Error", "No Item(s) selected")

    else:
        n = messagebox.askyesno("Delete item(s)","Are you sure you want to delete the selected item(s)?")
        if n == 1:
            pro_id = []
            for i in items_n:
                k = table.item(i, "values")
                pro_id.append(k[0])
            for rows_n in items_n:
                table.delete(rows_n)
            for row in pro_id:
                cursor.execute("DELETE FROM products WHERE product_id={}".format(row))
                dbconn.commit()
            unwanted_cat()
        else:
            pass

# Clear All
def clear_all():
    # Creating table product if not exist
    cursor.execute("""CREATE TABLE if not exists category(
       category varchar(100) NOT NULL primary key
           )
           """)
    cursor.execute("""CREATE TABLE if not exists products(
        product_id int  not null primary key,
        product_name varchar(100) not null,
        product_rate int not null,
        category varchar(100) not null references category(category)
        )
        """)
    dbconn.commit()

    if table.get_children() == ():
        messagebox.showerror("Error","No Items in the Market")
    else:
        n = messagebox.askyesno("Clear All", "Are you sure you want to clear all the items?")
        if n == 1:
            for rows in table.get_children():
                table.delete(rows)
            cursor.execute("DROP TABLE products")
            dbconn.commit()
            unwanted_cat()
        else:
            pass

def search_id():
    if Entry_5.get() == "":
        messagebox.showerror("Error", "Enter ID to search")
    else:
        id = int(Entry_5.get())
        cursor.execute("SELECT product_id FROM products")
        id_check = cursor.fetchall()
        dbconn.commit()
        all_rows = table.get_children()
        row = []
        for i in all_rows:
            if table.item(i).get("values")[0] == id:
                row.append(i)
        if row == []:
            messagebox.showerror("Error", "No product with ID {}".format(id))
        else:
            Button_1.configure(state="disabled")
            for j in row:
                Entry_1.delete(0, END)
                Entry_2.delete(0, END)
                Entry_3.delete(0, END)
                Entry_4.delete(0, END)
                values = table.item(j).get("values")
                Entry_4.insert(0, values[0])
                Entry_3.insert(0, values[1])
                Entry_2.insert(0, values[3])
                Entry_1.insert(0, values[2])

        Entry_5.delete(0, END)
        unwanted_cat()




# All Button Widgets
# Non-Table widgets
# Add to Market
Button_1 = Button(Admin, text="Add to market", relief="flat", bg="#fe1716",fg="black",borderwidth=0,font=font_1,command=add_to_cart)
Button_1.configure(activebackground="#fe1716")
Button_1.place(relx=0.04325,rely=0.878,width=135,height=43)

# Modify
Button_2 = Button(Admin, text="Update", relief="flat", bg="#fe1716", fg="black", borderwidth=0, font=font_1, command=update)
Button_2.configure(activebackground="#fe1716")
Button_2.place(relx=0.161, rely=0.878, width=135, height=43)

# Clear
Button_3 = Button(Admin, text="Clear", relief="flat", bg="#fe1716", fg="black", borderwidth=0, font=font_1,command=clear)
Button_3.configure(activebackground="#fe1716")
Button_3.place(relx=0.278, rely=0.878, width=135, height=43)

# Search
search_img = PhotoImage(file="./images/search.png")
search_button = Button(Admin, image=search_img, borderwidth=0,relief="flat",overrelief="flat", command=search_id)
search_button.place(relx=0.3713, rely=0.1175)

# Table widgets
# Select
Button_4 = Button(Admin, text="Select", relief="flat", bg="#fe1716", fg="black", borderwidth=0, font=font_1,command=select_item)
Button_4.configure(activebackground="#fe1716")
Button_4.place(relx=0.512, rely=0.8855, width=135, height=43)

# Delete item(s)
Button_5 = Button(Admin, text="Delete item(s)", relief="flat", bg="#fe1716",fg="black",borderwidth=0,font=font_1, command=delete_many)
Button_5.configure(activebackground="#fe1716")
Button_5.place(relx=0.686,rely=0.8855,width=135,height=43)

# Clear All
Button_6 = Button(Admin, text="Clear All", relief="flat", bg="#fe1716", fg="black", borderwidth=0, font=font_1, command=clear_all)
Button_6.configure(activebackground="#fe1716")
Button_6.place(relx=0.862, rely=0.8855, width=135, height=43)


Admin.protocol("WM_DELETE_WINDOW", Exit)

Admin.mainloop()
