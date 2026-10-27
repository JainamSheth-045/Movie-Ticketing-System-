from tkinter import *
from tkinter import messagebox
import mysql.connector

conn = mysql.connector.connect(
    user="root",
    password="pass@123",
    host="localhost",
    database="Atharva_s009_Dbms"
)
cursor = conn.cursor()


def show():
    cursor.execute("SELECT * FROM `user`")
    records = cursor.fetchall()

    result.delete("1.0", END)

    for row in records:
        result.insert(END, str(row) + "\n")


def update():
    try:
        uid = int(e1.get())
        name = e2.get()
        age = int(e3.get())
        contact = e4.get()

        sql = """UPDATE `user`
                 SET u_name=%s, u_age=%s, u_contact=%s
                 WHERE u_id=%s"""

        cursor.execute(sql, (name, age, contact, uid))
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Record updated")
        else:
            messagebox.showinfo("Info", "User ID not found")

        show()

    except Exception as err:
        conn.rollback()
        messagebox.showerror("Error", str(err))


def delete():
   try:
      uid = int(e1.get())

      # Check related records
      tables = ["cancellation", "ticket", "seat", "offer"]

      for table in tables:
         cursor.execute(
            f"SELECT COUNT(*) FROM {table} WHERE u_id=%s",
            (uid,)
         )

         if cursor.fetchone()[0] > 0:
            messagebox.showerror(
               "Cannot Delete",
               "This user has related records in " + table
               + ". Delete those records first."
            )
            return

      cursor.execute(
         "DELETE FROM `user` WHERE u_id=%s",
         (uid,)
      )
      conn.commit()

      if cursor.rowcount > 0:
         messagebox.showinfo("Success", "User deleted successfully")
      else:
         messagebox.showinfo("Info", "User ID not found")

      show()

   except Exception as err:
      conn.rollback()
      messagebox.showerror("Error", str(err))


def show_window():
    global e1, e2, e3, e4, result

    root = Tk()
    root.title("Manage Users")
    root.geometry("450x500")

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

    Button(root, text="Update", command=update).pack(pady=5)
    Button(root, text="Delete", command=delete).pack(pady=5)
    Button(root, text="Show Records", command=show).pack(pady=5)

    result = Text(root, height=12, width=45)
    result.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: close(root))
    root.mainloop()


def close(root):
    cursor.close()
    conn.close()
    root.destroy()


if __name__ == "__main__":
    show_window()