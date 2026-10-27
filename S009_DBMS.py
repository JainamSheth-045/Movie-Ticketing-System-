from tkinter import *
from tkinter import messagebox
import mysql.connector
import next_win

conn = mysql.connector.connect(
    user="root",
    password="pass@123",
    host="localhost",
    database="Atharva_s009_Dbms"
)
cursor = conn.cursor()


def insert():
    try:
        uid = int(e1.get())
        name = e2.get()
        age = int(e3.get())
        contact = e4.get()

        sql = "INSERT INTO `user` VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (uid, name, age, contact))
        conn.commit()

        messagebox.showinfo("Success", "Record inserted")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)

    except Exception as err:
        conn.rollback()
        messagebox.showerror("Error", str(err))


def open_next():
    root.destroy()
    next_win.show_window()


root = Tk()
root.title("Insert User")
root.geometry("350x300")

Label(root, text="User ID").pack()
e1 = Entry(root)
e1.pack()

Label(root, text="User Name").pack()
e2 = Entry(root)
e2.pack()

Label(root, text="Age").pack()
e3 = Entry(root)
e3.pack()

Label(root, text="Contact").pack()
e4 = Entry(root)
e4.pack()

Button(root, text="Insert", command=insert).pack(pady=10)
Button(root, text="Update / Delete / Show",
       command=open_next).pack()

root.mainloop()

cursor.close()
conn.close()