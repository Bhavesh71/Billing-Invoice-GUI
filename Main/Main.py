# Supermarket management system
# Author - BHAVESH L and JOHNEY B

from tkinter import *
from tkinter.font import Font
import os
from tkinter import messagebox
Main_Interface = Tk()
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

products = [
    ['101', 'Maaza 1 litre', '65', 'Beverages'],
    ['102', 'Coco Cola 1 litre', '70', 'Beverages'],
    ['103', 'Fanta 1 litre', '66', 'Beverages'],
    ['104', 'Miranda 1 litre', '72', 'Beverages'],
    ['105', '7 UP 1 litre', '60', 'Beverages'],
    ['106', 'Bovanto 1/2 litre', '35', 'Beverages'],
    ['107', 'Frooti 1/2 litre', '40', 'Beverages'],
    ['108', 'Pepsi 1/2 litre', '30', 'Beverages'],
    ['109', 'Apple Juice 1/2 litre', '25', 'Beverages'],
    ['110', 'Sprite 1/2 litre', '35', 'Beverages'],
    ['111', 'Aavin Milk 1 litre', '50', 'Dairy'],
    ['112', 'Aavin Milk 1/2 litre', '26', 'Dairy'],
    ['113', 'Aavin Milk 250 ml', '12', 'Dairy'],
    ['114', 'Amul Butter 100 g', '46', 'Dairy'],
    ['115', 'Arokya Curd 1 litre', '55', 'Dairy'],
    ['116', 'Aavin Curd 1 litre', '54', 'Dairy'],
    ['117', 'Amul Ghee 500 g', '245', 'Dairy'],
    ['118', 'MM Paneer', '230', 'Dairy'],
    ['119', 'Bhav Cheese 500g', '75', 'Dairy'],
    ['120', 'Cond. Milk 250ml', '90', 'Dairy'],
    ['121', 'Chilli Sauce 500g', '118', 'Sauce'],
    ['122', 'Sweent&Chilli Sauce 500g', '108', 'Sauce'],
    ['123', 'Tomato Sauce 500g', '100', 'Sauce'],
    ['124', 'Soya Sauce 500g', '110', 'Sauce'],
    ['125', 'Hot Tomato Sauce 500g', '115', 'Sauce'],
    ['126', 'Salt Bread', '21', 'Bread'],
    ['127', 'Milk Bread', '22', 'Bread'],
    ['128', 'Wheat Bread', '20', 'Bread'],
    ['129', 'Chicken Wings 400g', '270', 'Meat'],
    ['130', 'Chicken Breast 250g', '240', 'Meat'],
    ['131', 'Pork 500g', '200', 'Meat'],
    ['132', 'Beaf 1Kg', '290', 'Meat'],
    ['133', 'Chicken Boneless 500g', '250', 'Meat'],
    ['134', 'Chicken Leg Pie 1Kg', '190', 'Meat'],
    ['135', 'Full Chicken  ', '470', 'Meat'],
    ['136', '1Kg Basmati Rice', '200', 'Rice'],
    ['137', '1Kg Idli Rice ', '275', 'Rice'],
    ['138', '1Kg Tiffin Rice', '230', 'Rice'],
    ['139', '1Kg Basmati Rice', '200', 'Rice'],
    ['140', 'Ashir Atta 1Kg ', '45', 'Cereals'],
    ['141', 'RS Oats 500g ', '30', 'Cereals'],
    ['142', 'RS Frosted Flakes 500g ', '50', 'Cereals'],
    ['143', 'RS Oats 500g ', '30', 'Cereals'],
    ['144', 'RS  Flakes 200g ', '17', 'Cereals'],
    ['145', 'RS Oats 500g ', '30', 'Cereals'],
    ['146', 'RS Baking Soda 550g ', '235', 'Bakery'],
    ['147', 'RS Baking Powder 1Kg ', '60', 'Bakery'],
    ['148', 'Cake 1Kg', '50', 'Bakery'],
    ['149', 'Choclate Cake 1piece', '15', 'Bakery'],
    ['150', 'Strawberry Pastries 1pie', '15', 'Bakery'],
    ['151', 'Cream Bun', '10', 'Bakery'],
    ['152', 'Butter Biscuits', '12', 'Bakery'],
    ['153', 'Natraj 10 Pencils  ', '50', 'Stationary'],
    ['154', 'Natraj Ge. Box', '60', 'Stationary'],
    ['155', 'Natraj LS Scale', '10', 'Stationary'],
    ['156', 'Natraj SS Scalw', '5', 'Stationary'],
    ['157', 'DOMS ColourPencils 10', '20', 'Stationary'],
    ['158', 'DOMS Oil Pastels', '30', 'Stationary'],
    ['159', 'Natraj Sharpner', '3', 'Stationary'],
    ['160', 'FaberCastle M.pencil 0.7', '15', 'Stationary'],
    ['161', 'Apsara 0.7 led box ', '10', 'Stationary'],
    ['162', 'Lizol 500ml', '65', 'Hygiene'],
    ['163', 'Lizol l Litre', '120', 'Hygiene'],
    ['164', 'Harpic 500ml', '70', 'Hygiene'],
    ['165', 'Colgate Toothpaste BS', '25', 'Hygiene'],
    ['166', 'Pantanjli Toothpaste', '30', 'Hygiene'],
    ['167', 'Oral B Toothbrush', '15', 'Hygiene'],
    ['168', 'Close Up Toothpaste S', '20', 'Hygiene'],
    ['169', 'Colgate Toothbrush', '17', 'Hygiene'],
    ['170', 'MouthWasher 500ml', '50', 'Hygiene'],
    ['171', 'Sanitiser 500ml', '60', 'Hygiene'],
    ['172', 'Horlicks 350g', '49', 'Health'],
    ['173', 'Boost 500g', '100', 'Health'],
    ['174', 'Complan 500g', '45', 'Health'],
    ['175', 'Lays Blue S', '5', 'Snacks'],
    ['176', 'Lays Red S', '5', 'Snacks'],
    ['177', 'Lays Yellow S', '5', 'Snacks'],
    ['178', 'Lays Green S', '5', 'Snacks'],
    ['179', 'Lays Orange S', '5', 'Snacks'],
    ['180', 'Bingo Mad Angles S', '5', 'Snacks'],
    ['181', 'Bingo Mad Angles B', '10', 'Snacks'],
    ['182', 'Taka Tak B', '10', 'Snacks'],
    ['183', 'Lays Blue B', '10', 'Snacks'],
    ['184', 'Lays Blue B', '10', 'Snacks'],
    ['185', 'Lays Green B', '10', 'Snacks'],
    ['186', 'Lays Yellow B', '10', 'Snacks'],
    ['187', 'Lays Red B', '10', 'Snacks'],
    ['188', 'Lays Orange B', '10', 'Snacks'],
    ['189', 'Jim Jam S', '5', 'Snacks'],
    ['190', 'Jim Jam B', '10', 'Snacks'],
    ['191', 'Bourbon Bis ', '10', 'Snacks'],
    ['192', 'Cinnamon 50g ', '10', 'Seasonings'],
    ['193', 'Pepper 50g ', '10', 'Seasonings'],
    ['194', 'Fennugreek 50g ', '5', 'Seasonings'],
    ['195', 'Chinese Sea. 50g ', '10', 'Seasonings'],
    ['196', 'FCB Chicken M.', '10', 'Masalas'],
    ['197', 'FCB Fish F M.', '10', 'Masalas'],
    ['198', 'FCB Mutton M.', '10', 'Masalas'],
    ['199', 'FCB Sambar M.', '10', 'Masalas'],
    ['200', 'Arun cupI.', '15', 'IceCreams'],
    ['201', 'Arun ConeI. S', '17', 'IceCreams'],
    ['202', 'Arun ConeI. M', '25', 'IceCreams'],
    ['203', 'Arun ConeI. B', '35', 'IceCreams'],
    ['204', 'Jamai Kulfi.', '10', 'IceCreams'],
    ['205', 'Aman Family Pack I.', '80', 'IceCreams']]


# Add datas
for data in products:
    try:
        cursor.execute("INSERT INTO products VALUES(:product_id, :product_name, :product_rate, :category)",
                  {
                      "product_id": data[0],
                      "product_name": data[1],
                      "product_rate": data[2],
                      "category": data[3]
                  }
                  )
        dbconn.commit()
    except sqlite3.IntegrityError:
        pass

# Category
category_values = [
    ['Bakery'],
    ['Beverages'],
    ['Bread'],
    ['Cereals'],
    ['Dairy'],
    ['Hygiene'],
    ['IceCreams'],
    ['Masalas'],
    ['Meat'],
    ['Rice'],
    ['Sauce'],
    ['Seasonings'],
    ['Snacks'],
    ['Stationary']]

for data_1 in category_values:
    try:
        cursor.execute("INSERT INTO category VALUES(:category)",
                  {"category": data_1[0]}
                  )
        dbconn.commit()
    except sqlite3.IntegrityError:
        pass

def Exit():
    sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=Main_Interface)
    if sure == True:
        Main_Interface.destroy()

Main_Interface.protocol("WM_DELETE_WINDOW", Exit)


def admpg():
    Main_Interface.withdraw()
    os.system("python Admin_login.py")
    Main_Interface.deiconify()

def emp():
    Main_Interface.withdraw()
    os.system("python Employee.py")
    Main_Interface.deiconify()


# Fixing GUI Dimensions
Main_Interface.geometry("1150x650")
Main_Interface.resizable(0, 0)

# Fixing Title
Main_Interface.title("RS Groceries")

# Fixing GUI Background
Background = PhotoImage(file="./images/Bg_main.png")
Bg_label = Label(Main_Interface, image=Background)
Bg_label.place(x=0, y=0, relwidth=1, relheight=1)


#Fixing GUI Icon
Main_Interface.iconbitmap("./images/Logo.ico")


# Creating Button
font_1 = Font(family="Franklin Gothic Medium",size=15,weight="bold")
# Button 1
button1 = Button(Main_Interface,text="EMPLOYEE",bg="#38b7fe",fg="black",padx=30,pady=10,width=20,font=font_1,activebackground="#38b7fe",activeforeground="black",command=emp)
button1.configure(relief="flat")
button1.configure(overrelief="flat")
button1.configure(borderwidth="0")
button1.place(relx=0.32, rely=0.42, width=180, height=90,anchor=E)

# Button 2
button2 = Button(Main_Interface, text="ADMIN",bg="#38b7fe", fg="black",padx=30,pady=10,width=20,font=font_1,activebackground="#38b7fe",activeforeground="black",command=admpg)
button2.configure(relief="flat")
button2.configure(overrelief="flat")
button2.configure(borderwidth="0")
button2.place(relx=0.70, rely=0.42, width=240, height=90, anchor=W)

dbconn.close()
Main_Interface.mainloop()
