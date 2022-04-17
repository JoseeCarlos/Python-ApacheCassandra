from tkinter.tix import Tree
from cassandra.cluster import Cluster
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

root = Tk()
root.title("Cassandra Insert DB")

cluster = Cluster(['127.0.0.1'],port=9042)
session = cluster.connect('dbprueba', wait_for_all_pools=True)
session.execute('USE dbprueba;')

def render_data():
    tree.delete(*tree.get_children())
    for row in session.execute("""
    SELECT * FROM PERSON;
    """):
        tree.insert("", 0, text=row.id, values=(row.id, row.name, row.last_name, row.age))

def insert_data(person):
    
    session.execute("""
    INSERT INTO PERSON (id, name, last_name, age)
    VALUES (uuid(), %s,  %s, %s);
    """, (person.get("name"), person.get("lastname"), int(person.get("age"))))
    render_data()

def form_data():
    def save_data():
        if not name.get() or not laname.get() or not edad.get():
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return
        person = {
            "name": name.get(),
            "lastname": laname.get(),
            "age": edad.get(),
        }
        insert_data(person)
        top.destroy()
    
    top = Toplevel()
    top.title("Insert Data")

    lname = Label(top, text="Nombre: ")
    name = Entry(top, width=40)
    lname.grid(row=0, column=0, sticky=W)
    name.grid(row=0, column=1, sticky=W)

    lapellido = Label(top, text="Apellido: ")
    laname = Entry(top, width=40)
    lapellido.grid(row=1, column=0, sticky=W)
    laname.grid(row=1, column=1, sticky=W)

    ledad = Label(top, text="Edad: ")
    edad = Entry(top, width=40)
    ledad.grid(row=2, column=0, sticky=W)
    edad.grid(row=2, column=1, sticky=W)

    btn_save = Button(top, text="Guardar", command=save_data)
    btn_save.grid(row=4, column=0, sticky=W)

    top.mainloop()
    

btn = Button(root, text="Insert Data", command=form_data)
btn.grid(row=0, column=0)

tree = ttk.Treeview(root)
tree["columns"] = ("id", "name", "last_name", "age")
tree.column("#0", stretch=NO,width=0)
tree.column("id", stretch=NO, width=100)
tree.column("name", stretch=NO, width=100)
tree.column("last_name", stretch=NO, width=100)
tree.column("age", stretch=NO, width=100)


tree.heading("id", text="id")
tree.heading("name", text="Nombre")
tree.heading("last_name", text="Apellido")
tree.heading("age", text="Edad")

tree.grid(row=1, column=0,sticky=N+S+E+W,columnspan=2)
render_data()
root.mainloop()
