import tkinter as tk
from tkinter import messagebox, ttk
import os
from datetime import datetime


# ===================== LOGIN SYSTEM ===================== #

def open_cashier_system():
    # OPEN MAIN CASHIER WINDOW
    cashier_window = tk.Tk()
    cashier_window.title("Simple Cashier System")
    cashier_window.geometry("800x650")

    # ---------- FILE SETUP ----------
    FILE_PATH = r"items.txt"
    BILL_HISTORY = r"bill_history.txt"
    ICON_PATH = r"fruits.ico"

    TAX_RATE = 0.05

    # Read existing products
    store = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2 and parts[1].isdigit():
                    store.append({"name": parts[0], "price": int(parts[1])})

    cart = []
    total = 0

    # ---------- FUNCTIONS ----------
    def refresh_products():
        product_table.delete(*product_table.get_children())
        for i, product in enumerate(store, start=1):
            product_table.insert("", "end", values=(i, product["name"], product["price"]))

    def save_products():
        with open(FILE_PATH, "w") as f:
            for product in store:
                f.write(f"{product['name']},{product['price']}\n")

    def add_new_product():
        name = entry_name.get().strip()
        price = entry_price.get().strip()

        if not name or not price.isdigit():
            messagebox.showwarning("Invalid", "Enter valid name and numeric price.")
            return

        store.append({"name": name, "price": int(price)})
        save_products()
        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        refresh_products()
        messagebox.showinfo("Added", f"Product '{name}' added successfully!")

    def add_to_cart():
        nonlocal total
        selected = product_table.focus()
        if not selected:
            messagebox.showwarning("Select", "Select a product first.")
            return

        qty_str = entry_qty.get().strip()
        if not qty_str.isdigit() or int(qty_str) <= 0:
            messagebox.showwarning("Invalid", "Enter valid quantity.")
            return

        item = product_table.item(selected)["values"]
        name = item[1]
        price = item[2]
        qty = int(qty_str)
        subtotal = qty * price

        total += subtotal
        cart.append({"name": name, "qty": qty, "subtotal": subtotal})

        text_bill.insert(tk.END, f"{qty} x {name} = {subtotal} Ks\n")
        entry_qty.delete(0, tk.END)

    def save_bill_history(content):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(BILL_HISTORY, "a") as f:
            f.write(f"--- Bill Saved at {now} ---\n")
            f.write(content)
            f.write("\n" + "=" * 50 + "\n\n")

    def show_total():
        nonlocal total

        subtotal = total
        tax = int(subtotal * TAX_RATE)
        final_amount = subtotal + tax

        text_bill.insert(tk.END, "\n-----------------------------\n")
        text_bill.insert(tk.END, f"Subtotal: {subtotal} Ks\n")
        text_bill.insert(tk.END, f"Tax (5%): {tax} Ks\n")
        text_bill.insert(tk.END, f"Total Amount: {final_amount} Ks\n")
        text_bill.insert(tk.END, "Thank you for shopping!\n")

        bill_text = text_bill.get("1.0", tk.END).strip()
        save_bill_history(bill_text)

        messagebox.showinfo("Saved", "Bill saved to history!")

    def clear_all():
        nonlocal cart, total
        cart = []
        total = 0
        text_bill.delete("1.0", tk.END)
        entry_qty.delete(0, tk.END)

    def open_bill_history():
        if not os.path.exists(BILL_HISTORY):
            messagebox.showinfo("No History", "No bill history found.")
            return

        with open(BILL_HISTORY, "r") as f:
            data = f.read()

        bills = data.strip().split("=" * 50)

        if not bills or bills == [""]:
            messagebox.showinfo("Empty", "No bill history found.")
            return

        for bill in bills:
            bill = bill.strip()
            if bill:
                messagebox.showinfo("Bill Record", bill)

    # Change icon
    if os.path.exists(ICON_PATH):
        cashier_window.iconbitmap(ICON_PATH)

    # ---------- MENU BAR ----------
    menubar = tk.Menu(cashier_window)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="View Bill History", command=open_bill_history)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=cashier_window.quit)

    menubar.add_cascade(label="File", menu=file_menu)
    cashier_window.config(menu=menubar)

    # ---------- PRODUCT LIST ----------
    frame_products = tk.LabelFrame(cashier_window, text="Store Products", padx=10, pady=10)
    frame_products.pack(fill="x", padx=10, pady=5)

    columns = ("#", "Name", "Price")
    product_table = ttk.Treeview(frame_products, columns=columns, show="headings", height=10)
    for col in columns:
        product_table.heading(col, text=col)
        product_table.column(col, width=220, anchor="center")

    scroll_y = ttk.Scrollbar(frame_products, orient="vertical", command=product_table.yview)
    product_table.configure(yscroll=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    product_table.pack(side="left", fill="x")

    refresh_products()

    # ---------- ADD PRODUCT ----------
    frame_add = tk.LabelFrame(cashier_window, text="Add Product", padx=10, pady=10)
    frame_add.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_add, text="Name:").grid(row=0, column=0, padx=5)
    entry_name = tk.Entry(frame_add)
    entry_name.grid(row=0, column=1, padx=5)

    tk.Label(frame_add, text="Price:").grid(row=0, column=2, padx=5)
    entry_price = tk.Entry(frame_add)
    entry_price.grid(row=0, column=3, padx=5)

    tk.Button(frame_add, text="Add", command=add_new_product).grid(row=0, column=4, padx=10)

    # ---------- PURCHASE ----------
    frame_buy = tk.LabelFrame(cashier_window, text="Purchase", padx=10, pady=10)
    frame_buy.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_buy, text="Quantity:").grid(row=0, column=0, padx=5)
    entry_qty = tk.Entry(frame_buy, width=10)
    entry_qty.grid(row=0, column=1, padx=5)

    tk.Button(frame_buy, text="Add to Cart", command=add_to_cart).grid(row=0, column=2, padx=10)
    tk.Button(frame_buy, text="Show Total", command=show_total).grid(row=0, column=3, padx=10)
    tk.Button(frame_buy, text="Clear", command=clear_all).grid(row=0, column=4, padx=10)

    # ---------- BILL AREA ----------
    frame_bill = tk.LabelFrame(cashier_window, text="Receipt", padx=10, pady=10)
    frame_bill.pack(fill="both", expand=True, padx=10, pady=10)

    text_bill = tk.Text(frame_bill, height=20, width=90, font=("Consolas", 11))
    text_bill.pack(side="left", fill="both", expand=True)

    scroll_bill = ttk.Scrollbar(frame_bill, orient="vertical", command=text_bill.yview)
    scroll_bill.pack(side="right", fill="y")
    text_bill.configure(yscrollcommand=scroll_bill.set)

    cashier_window.mainloop()


# ===================== LOGIN WINDOW ===================== #

ICON_PATH = r"fruits.ico"

def check_login():
    user = entry_user.get()
    pw = entry_pass.get()

    if user == "lwin" and pw == "1500":
        messagebox.showinfo("Success", "Login Successful!")
        login_window.destroy()
        open_cashier_system()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")


login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("350x250")
login_window.resizable(False, False)
if os.path.exists(ICON_PATH):
    login_window.iconbitmap(ICON_PATH)

tk.Label(login_window, text="Cashier Login", font=("Arial", 16)).pack(pady=15)

frame = tk.Frame(login_window)
frame.pack()

tk.Label(frame, text="Username: ").grid(row=0, column=0, pady=5)
entry_user = tk.Entry(frame, width=25)
entry_user.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Password: ").grid(row=1, column=0, pady=5)
entry_pass = tk.Entry(frame, width=25, show="*")
entry_pass.grid(row=1, column=1, pady=5)

tk.Button(login_window, text="Login", width=15, command=check_login).pack(pady=15)

login_window.mainloop()
