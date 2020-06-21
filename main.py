from tkinter import ttk
from tkinter import *

import sqlite3
from sqlite3 import Error

class Product:
    def __init__(self, window):
        self.wind = window
        self.wind.title('CRUD Products')
        self.wind.geometry("400x420")

    # Creating a frame container
        frame = LabelFrame(self.wind, text = ' Enter your name')
        frame.grid(row=0, column=3, pady = 10)
    # Name input
        Label(frame, text = 'Name:  ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1,sticky = W+E)

    # Price input
        Label(frame, text='Price:  ').grid(row=2, column=0)
        self.price= Entry(frame)
        self.price.grid(row=2, column=1, sticky = W+E)

    # Button for add product
        self.btn_enter_text='Save Product'
        ttk.Button(frame, text = self.btn_enter_text, command = lambda:self.add_products()).grid(row=3, column=0)
        ttk.Button(frame, text='Update Product', command=lambda: self.update_products()).grid(row=3, column=1)
        self.message = Label(fg = 'red')
        self.message.grid(row=3, column = 2, columnspan = 2,  sticky = W+E)

    # Create an table
        self.tree = ttk.Treeview(height = 10, columns = 4)
        self.tree.grid(row = 4, column = 2, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor = CENTER)
        #self.tree.heading('#2', text = 'Name', anchor = CENTER)

    # Buttons for the Update and Delete
        ttk.Button(self.wind, text='Delete Product', command=lambda: self.delete_product()).grid(row=20, column=2)
        ttk.Button(self.wind, text='Enter Product', command=lambda: self.update_entrys()).grid(row=20, column=3)

    # getting the data from the db
        rows = self.get_products()
        for row in rows:
            self.tree.insert("",index=0,text=row[1],values=[row[2]])

    def run_query(self, query, params = ()):
        with sqlite3.connect('products.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute(query, params)
            conn.commit()
        return res

    def get_products(self):
        data = self.tree.get_children()
        for element in data:
            self.tree.delete(element)
        query = 'SELECT * FROM productos ORDER BY Name DESC'
        rows = self.run_query(query)
        for row in rows:
            self.tree.insert("",index=0,text=row[1],values=[row[2]])
        return rows

    def add_products(self):
        try:
            if self.validation():
                query = 'INSERT INTO productos VALUES(NULL,?,?,1)'
                params = (self.name.get(), self.price.get())
                self.run_query(query, params)
                print('Guardado en la BD')
                self.message['text'] = 'Producto guardado en la BD'
                self.name.delete(0, 'end')
                self.price.delete(0, 'end')
            else:
                self.message['text'] = 'Nombre y precio requerido'
            self.get_products()
        except sqlite3.IntegrityError:
            self.message['text'] = 'No se pudo guardar. Ya existe un producto con éste nombre'

    def delete_product(self):
        item = self.tree.item(self.tree.focus())
        query = 'DELETE FROM productos WHERE Name = ?'
        params = (str(item['text']),)
        self.run_query(query, params)
        self.message['text'] = 'Elemento {} eliminado'.format(item['text'])
        self.get_products()

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def update_entrys(self):
        self.name.delete(0,'end')
        self.price.delete(0,'end')
        self.show_data()

    def show_data(self):
        item = self.tree.item(self.tree.focus())
        print(item)
        if item:
            self.name.insert(0, item['text'])
            self.price.insert(0,item['values'])
        self.btn_enter_text='Update Product'

    def update_products(self):
        item = self.tree.item(self.tree.focus())
        if self.validation():
            query = 'UPDATE productos SET name = ?, price=? WHERE name = ?'
            params = (self.name.get(),self.price.get(),str(item['text']))
            self.run_query(query, params)
            self.message['text'] = 'Elemento {} Modificado'.format(item['text'])
            self.get_products()
            self.name.delete(0, 'end')
            self.price.delete(0, 'end')
        pass

if __name__ == '__main__':
    window = Tk()
    app = Product(window)
    window.mainloop()
