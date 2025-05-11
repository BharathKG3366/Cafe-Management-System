import mysql.connector
from tkinter import *
from tkinter import messagebox

class CafeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafe Management System")
        
        self.menu_items = {}
        self.create_widgets()
        self.fetch_menu()

    def create_widgets(self):
        self.menu_frame = Frame(self.root)
        self.menu_frame.pack()

        self.order_frame = Frame(self.root)
        self.order_frame.pack()

        self.bill_frame = Frame(self.root)
        self.bill_frame.pack()

        self.menu_label = Label(self.menu_frame, text="Menu", font=("Arial", 16))
        self.menu_label.pack()

        self.menu_listbox = Listbox(self.menu_frame, width=50)
        self.menu_listbox.pack()

        self.quantity_label = Label(self.order_frame, text="Enter Quantity:")
        self.quantity_label.pack()

        self.quantity_entry = Entry(self.order_frame)
        self.quantity_entry.pack()

        self.order_button = Button(self.order_frame, text="Place Order", command=self.place_order)
        self.order_button.pack()

        self.bill_button = Button(self.bill_frame, text="Generate Bill", command=self.generate_bill)
        self.bill_button.pack()

        self.bill_text = Text(self.bill_frame, width=50, height=10)
        self.bill_text.pack()

    def fetch_menu(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Port8',
                database='cafe_management2'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM menu")
            rows = cursor.fetchall()
            for row in rows:
                self.menu_items[row[0]] = (row[1], row[2])  # id: (item_name, price)
                self.menu_listbox.insert(END, f"{row[0]}. {row[1]} - ${row[2]:.2f}")
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def place_order(self):
        try:
            selected_item_index = self.menu_listbox.curselection()[0]
            item_id = selected_item_index + 1
            quantity = int(self.quantity_entry.get())
            item_name, price = self.menu_items[item_id]
            total_price = price * quantity
            self.bill_text.insert(END, f"{item_name} x {quantity} = ${total_price:.2f}\n")
            messagebox.showinfo("Order Placed", f"Order for {item_name} has been placed.")
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select an item from the menu.")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid quantity.")

    def generate_bill(self):
        self.bill_text.insert(END, "Thank you for your order!\n")
        self.bill_text.insert(END, "=================================\n")

if __name__ == "__main__":
    root = Tk()
    app = CafeManagementSystem(root)
    root.mainloop()
