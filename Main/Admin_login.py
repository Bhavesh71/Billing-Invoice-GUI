from tkinter import *
from tkinter import messagebox
import os
from tkinter.font import Font

adm = Tk()
adm.geometry("500x715")
adm.resizable(0, 0)
adm.iconbitmap("./images/Logo.ico")
adm.title("Login Page")

user = StringVar()
password = StringVar()

# Admin page
def admpage():
    adm.withdraw()
    os.system("python Admin.py")
    adm.deiconify()


# Fixing GUI Background
Background = PhotoImage(file="./images/Admin_login.png")
Bg_label = Label(adm, image=Background)
Bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Username Entry
font_1 = Font(family="Comic Sans MS",size=15,weight="bold")

entry1 = Entry(adm)
entry1.place(relx=0.225, rely=0.272, width=315, height=26)
entry1.configure(font=font_1)
entry1.configure(relief="flat")
entry1.configure(textvariable=user)


# Password Entry
entry2 = Entry(adm)
entry2.place(relx=0.225, rely=0.405, width=315, height=26)
entry2.configure(font=font_1)
entry2.configure(relief="flat")
entry2.configure(show="•")
entry2.configure(textvariable=password)


def admlog_op():
    Username = user.get()
    Password = password.get()
    if Username == "ADMIN":
        if Password == "1234":
            messagebox.showinfo("Login Page", "The login is successful.")
            entry1.delete(0, END)
            entry2.delete(0, END)
            adm.withdraw()
            admpage()
        else:
            messagebox.showerror("Oops!!", "You are not an admin.")
    else:
        messagebox.showerror("Error", "Incorrect username or password.")

# Confirm Button
font_2 = Font(family="Franklin Gothic Medium",size=15,weight="bold")


button1 = Button(adm)
button1.place(relx=0.230, rely=0.755, width=280, height=43)
button1.configure(relief="flat")
button1.configure(overrelief="flat")
button1.configure(activebackground="#D2463E")
button1.configure(foreground="#ffffff")
button1.configure(background="#D2463E")
button1.configure(font=font_2)
button1.configure(borderwidth="0")
button1.configure(text="""LOGIN""")
button1.configure(command=admlog_op)

# Exit
def Exit():
    adm.destroy()

adm.protocol("WM_DELETE_WINDOW", Exit)

adm.mainloop()
