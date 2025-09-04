import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class CafeManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)  # Fullscreen

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Load Background Image
        try:
            bg_image = Image.open("C:/Users/prince/Desktop/python/IMAGE/bg.jpg")
            bg_image = bg_image.resize((screen_width, screen_height))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Background Image Load Error:", e)

        # Color Theme
        theme_bg = '#f0e6d6'
        heading_color = '#5b3a29'  # dark coffee brown
        button_fg = 'white'

        # Main Frame on top of background
        overlay = tk.Frame(self.root, bg=theme_bg, bd=5)
        overlay.place(relx=0.5, rely=0.5, anchor='center')

        # Heading
        tk.Label(overlay, text="Cafe Management System", font=('verdana', 22, 'bold'),
                 fg=heading_color, bg=theme_bg).pack(pady=10)

        # Menu Items
        self.menu = {
            "Coffee": 50, "Tea": 30, "Cake": 100, "Pizza": 200,
            "Pasta": 120, "Burger": 150, "Cold Coffee": 70, "Sandwich": 90,
            "Noodles":150
        }
        self.order = {}

        tk.Label(overlay, text="Menu", font=('verdana', 15, 'bold'), bg=theme_bg, fg=heading_color).pack()
        self.menu_display = tk.Text(overlay, height=5, width=40, state=tk.DISABLED, bg="white", fg="black")
        self.menu_display.pack()
        self.update_menu()

        tk.Label(overlay, text="Item Name:", bg=theme_bg, fg="black").pack()
        items = list(self.menu.keys())
        self.selected_item = tk.StringVar()
        self.selected_item.set(items[0])
        self.item_dropdown = tk.OptionMenu(overlay, self.selected_item, *items)
        self.item_dropdown.config(bg="white")
        self.item_dropdown.pack()

        tk.Label(overlay, text="Quantity:", bg=theme_bg, fg="black").pack()
        quantities = [str(i) for i in range(1, 11)]
        self.selected_quantity = tk.StringVar()
        self.selected_quantity.set(quantities[0])
        self.quantity_dropdown = tk.OptionMenu(overlay, self.selected_quantity, *quantities)
        self.quantity_dropdown.config(bg="white")
        self.quantity_dropdown.pack()

        tk.Button(overlay, text="Add to Order", command=self.add_to_order, bg="#4caf50", fg=button_fg).pack(pady=2)
        tk.Button(overlay, text="Calculate Total", command=self.calculate_total, bg="#795548", fg=button_fg).pack(pady=2)
        tk.Button(overlay, text="Clear Order", command=self.clear_order, bg="#d32f2f", fg=button_fg).pack(pady=2)

        tk.Label(overlay, text="Order Summary:", bg=theme_bg, fg="black").pack()
        self.order_summary = tk.Text(overlay, height=10, width=40, state=tk.DISABLED, bg="white", fg="black")
        self.order_summary.pack()

        # Press Esc to close fullscreen
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def update_menu(self):
        self.menu_display.config(state=tk.NORMAL)
        self.menu_display.delete(1.0, tk.END)
        for item, price in self.menu.items():
            self.menu_display.insert(tk.END, f"{item}: ₹{price}\n")
        self.menu_display.config(state=tk.DISABLED)

    def add_to_order(self):
        item = self.selected_item.get().strip().title()
        quantity_str = self.selected_quantity.get().strip()

        if item not in self.menu:
            messagebox.showerror("Error", f"'{item}' menu me available nahi hai!")
            return

        if not quantity_str.isdigit() or int(quantity_str) <= 0:
            messagebox.showerror("Error", "Quantity sirf ek positive number hona chahiye!")
            return

        quantity = int(quantity_str)

        if item in self.order:
            self.order[item] += quantity
        else:
            self.order[item] = quantity

        messagebox.showinfo("Success", f"'{item}' x {quantity} Your order has been recoreded!")
        self.update_order_summary()

    def update_order_summary(self):
        self.order_summary.config(state=tk.NORMAL)
        self.order_summary.delete(1.0, tk.END)
        for item, quantity in self.order.items():
            price = self.menu[item] * quantity
            self.order_summary.insert(tk.END, f"{item} x {quantity}: ₹{price}\n")
        self.order_summary.config(state=tk.DISABLED)

    def calculate_total(self):
        if not self.order:
            messagebox.showerror("Error", "No items in order!")
            return

        total = sum(self.menu[item] * quantity for item, quantity in self.order.items())
        tax = total * 0.05
        service_charge = total * 0.10
        grand_total = total + tax + service_charge

        messagebox.showinfo("Total Bill", f"Subtotal: ₹{total}\nTax (5%): ₹{tax:.2f}\n"
                                          f"Service Charge (10%): ₹{service_charge:.2f}\n"
                                          f"Grand Total: ₹{grand_total:.2f}")

    def clear_order(self):
        self.order.clear()
        self.update_order_summary()
        messagebox.showinfo("Cleared", "Order cleared successfully!")

    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = CafeManagementSystem()
    app.run()


