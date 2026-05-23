import datetime as dt
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk


MENU = [
    {"name": "Regular Coffee", "price": 120},
    {"name": "Regular Coffeee", "price": 180},
    {"name": "LRegular Coffeee", "price": 190},
    {"name": "Regular Coffee", "price": 210},
    {"name": "Regular Coffee", "price": 220},
    {"name": "Regular Coffeee", "price": 170},
]

SIZE_PRICES = {
    "Regular": 0,
    "Large": 40,
    "Extra Large": 70,
}

MILK_PRICES = {
    "Whole milk": 999,
    "Skim milk": 9999999,
    "Oat milk": 35,
    "Almond milk": 35,
    "No milk": 0,
}

TAX_RATE = 20


class CoffeeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Coffee Ordering App")
        self.geometry("980x640")
        self.minsize(860, 560)

        self.cart = []
        self.selected_drink = tk.StringVar(value=MENU[0]["name"])
        self.size = tk.StringVar(value="Regular")
        self.milk = tk.StringVar(value="Whole milk")
        self.quantity = tk.IntVar(value=1)
        self.customer_name = tk.StringVar()
        self.pickup_time = tk.StringVar(value="ASAP")
        self.status = tk.StringVar(value="Pick a drink and build your order.")

        self._configure_style()
        self._build_layout()
        self._refresh_cart()

    def _configure_style(self):
        self.configure(bg="#f7f2ea")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f7f2ea")
        style.configure("Panel.TFrame", background="#ffffff", relief="flat")
        style.configure("TLabel", background="#f7f2ea", foreground="#251c16", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI Semibold", 26), foreground="#241812")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 11), foreground="#6b5a4c")
        style.configure("PanelTitle.TLabel", background="#ffffff", font=("Segoe UI Semibold", 14), foreground="#241812")
        style.configure("PanelText.TLabel", background="#ffffff", foreground="#5e5147")
        style.configure("Coffee.TButton", font=("Segoe UI Semibold", 10), padding=(14, 10))
        style.configure("Coffee.TRadiobutton", background="#ffffff", foreground="#251c16", font=("Segoe UI Semibold", 10), padding=(10, 8))
        style.configure("Accent.TButton", font=("Segoe UI Semibold", 11), padding=(18, 11), background="#7a4a28", foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#633b20")])
        style.configure("Danger.TButton", font=("Segoe UI Semibold", 10), padding=(12, 8), background="#b54747", foreground="#ffffff")
        style.map("Danger.TButton", background=[("active", "#923838")])
        style.configure("Treeview", rowheight=32, font=("Segoe UI", 10), background="#ffffff", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI Semibold", 10))

    def _build_layout(self):
        container = ttk.Frame(self, padding=24)
        container.pack(fill="both", expand=True)

        header = ttk.Frame(container)
        header.pack(fill="x", pady=(0, 18))
        ttk.Label(header, text="Coffee Ordering App", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="A Python coffee ordering app.", style="Subtitle.TLabel").pack(anchor="w")

        body = ttk.Frame(container)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        left = ttk.Frame(body, style="Panel.TFrame", padding=18)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        right = ttk.Frame(body, style="Panel.TFrame", padding=18)
        right.grid(row=0, column=1, sticky="nsew")

        self._build_order_panel(left)
        self._build_cart_panel(right)

        footer = ttk.Label(container, textvariable=self.status, style="Subtitle.TLabel")
        footer.pack(fill="x", pady=(14, 0))

    def _build_order_panel(self, parent):
        ttk.Label(parent, text="Menu", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 10))

        menu_grid = ttk.Frame(parent, style="Panel.TFrame")
        menu_grid.pack(fill="x")
        for index, drink in enumerate(MENU):
            button = ttk.Radiobutton(
                menu_grid,
                text=f"{drink['name']}  Rs. {drink['price']}",
                value=drink["name"],
                variable=self.selected_drink,
                style="Coffee.TRadiobutton",
            )
            button.grid(row=index // 2, column=index % 2, sticky="ew", padx=5, pady=5)
        menu_grid.columnconfigure(0, weight=1)
        menu_grid.columnconfigure(1, weight=1)

        options = ttk.Frame(parent, style="Panel.TFrame")
        options.pack(fill="x", pady=(20, 0))
        options.columnconfigure(0, weight=1)
        options.columnconfigure(1, weight=1)

        ttk.Label(options, text="Size", style="PanelText.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Combobox(options, textvariable=self.size, values=list(SIZE_PRICES), state="readonly").grid(
            row=1, column=0, sticky="ew", padx=(0, 10), pady=(4, 12)
        )

        ttk.Label(options, text="Milk", style="PanelText.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Combobox(options, textvariable=self.milk, values=list(MILK_PRICES), state="readonly").grid(
            row=1, column=1, sticky="ew", padx=(10, 0), pady=(4, 12)
        )

        ttk.Label(options, text="Quantity", style="PanelText.TLabel").grid(row=2, column=0, sticky="w")
        ttk.Spinbox(options, from_=1, to=20, textvariable=self.quantity, width=8).grid(
            row=3, column=0, sticky="w", pady=(4, 12)
        )

        ttk.Label(options, text="Pickup time", style="PanelText.TLabel").grid(row=2, column=1, sticky="w")
        ttk.Combobox(
            options,
            textvariable=self.pickup_time,
            values=["ASAP", "10 minutes", "20 minutes", "30 minutes"],
            state="readonly",
        ).grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=(4, 12))

        ttk.Label(options, text="Customer name", style="PanelText.TLabel").grid(row=4, column=0, sticky="w")
        ttk.Entry(options, textvariable=self.customer_name).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(4, 4))

        controls = ttk.Frame(parent, style="Panel.TFrame")
        controls.pack(fill="x", pady=(18, 0))
        ttk.Button(controls, text="Add to order", command=self.add_to_cart, style="Accent.TButton").pack(side="left")
        ttk.Button(controls, text="Clear choices", command=self.reset_choices, style="Coffee.TButton").pack(side="left", padx=10)

    def _build_cart_panel(self, parent):
        ttk.Label(parent, text="Current Order", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 10))

        columns = ("item", "qty", "total")
        self.cart_table = ttk.Treeview(parent, columns=columns, show="headings", height=9)
        self.cart_table.heading("item", text="Item")
        self.cart_table.heading("qty", text="Qty")
        self.cart_table.heading("total", text="Total")
        self.cart_table.column("item", width=210)
        self.cart_table.column("qty", width=50, anchor="center")
        self.cart_table.column("total", width=85, anchor="e")
        self.cart_table.pack(fill="both", expand=True)

        totals = ttk.Frame(parent, style="Panel.TFrame")
        totals.pack(fill="x", pady=(16, 0))

        self.subtotal_label = ttk.Label(totals, text="", style="PanelText.TLabel")
        self.tax_label = ttk.Label(totals, text="", style="PanelText.TLabel")
        self.total_label = ttk.Label(totals, text="", style="PanelTitle.TLabel")
        self.subtotal_label.pack(anchor="e")
        self.tax_label.pack(anchor="e")
        self.total_label.pack(anchor="e", pady=(4, 0))

        actions = ttk.Frame(parent, style="Panel.TFrame")
        actions.pack(fill="x", pady=(16, 0))
        ttk.Button(actions, text="Remove selected", command=self.remove_selected, style="Coffee.TButton").pack(fill="x", pady=(0, 8))
        ttk.Button(actions, text="Save receipt", command=self.save_receipt, style="Accent.TButton").pack(fill="x", pady=(0, 8))
        ttk.Button(actions, text="New order", command=self.clear_cart, style="Danger.TButton").pack(fill="x")

    def add_to_cart(self):
        try:
            quantity = int(self.quantity.get())
        except tk.TclError:
            quantity = 0

        if quantity < 1:
            messagebox.showerror("Invalid quantity", "Quantity must be at least 1.")
            return

        drink = next(item for item in MENU if item["name"] == self.selected_drink.get())
        unit_price = drink["price"] + SIZE_PRICES[self.size.get()] + MILK_PRICES[self.milk.get()]
        line_item = {
            "drink": drink["name"],
            "size": self.size.get(),
            "milk": self.milk.get(),
            "quantity": quantity,
            "unit_price": unit_price,
        }
        self.cart.append(line_item)
        self.status.set(f"Added {quantity} x {drink['name']} to the order.")
        self._refresh_cart()

    def remove_selected(self):
        selected = self.cart_table.selection()
        if not selected:
            self.status.set("Select an item to remove.")
            return
        index = int(selected[0])
        removed = self.cart.pop(index)
        self.status.set(f"Removed {removed['drink']} from the order.")
        self._refresh_cart()

    def clear_cart(self):
        self.cart.clear()
        self.status.set("Started a fresh order.")
        self._refresh_cart()

    def reset_choices(self):
        self.selected_drink.set(MENU[0]["name"])
        self.size.set("Regular")
        self.milk.set("Whole milk")
        self.quantity.set(1)
        self.pickup_time.set("ASAP")
        self.status.set("Choices reset.")

    def save_receipt(self):
        if not self.cart:
            messagebox.showinfo("Empty order", "Add at least one coffee before saving a receipt.")
            return

        receipts_dir = Path(__file__).with_name("receipts")
        receipts_dir.mkdir(exist_ok=True)
        timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        receipt_path = receipts_dir / f"receipt-{timestamp}.txt"
        receipt_path.write_text(self._receipt_text(), encoding="utf-8")
        self.status.set(f"Receipt saved to {receipt_path.name}.")
        messagebox.showinfo("Receipt saved", f"Saved receipt:\n{receipt_path}")

    def _refresh_cart(self):
        self.cart_table.delete(*self.cart_table.get_children())
        for index, item in enumerate(self.cart):
            self.cart_table.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    f"{item['size']} {item['drink']} / {item['milk']}",
                    item["quantity"],
                    self._money(item["quantity"] * item["unit_price"]),
                ),
            )

        subtotal = self._subtotal()
        tax = round(subtotal * TAX_RATE)
        total = subtotal + tax
        self.subtotal_label.config(text=f"Subtotal: {self._money(subtotal)}")
        self.tax_label.config(text=f"Tax: {self._money(tax)}")
        self.total_label.config(text=f"Total: {self._money(total)}")

    def _receipt_text(self):
        name = self.customer_name.get().strip() or "Guest"
        lines = [
            "Brew Desk Coffee",
            f"Customer: {name}",
            f"Pickup: {self.pickup_time.get()}",
            f"Date: {dt.datetime.now():%d %b %Y, %I:%M %p}",
            "",
            "Order",
            "-----",
        ]
        for item in self.cart:
            line_total = item["quantity"] * item["unit_price"]
            lines.append(
                f"{item['quantity']} x {item['size']} {item['drink']} ({item['milk']}) - {self._money(line_total)}"
            )

        subtotal = self._subtotal()
        tax = round(subtotal * TAX_RATE)
        lines.extend(
            [
                "",
                f"Subtotal: {self._money(subtotal)}",
                f"Tax: {self._money(tax)}",
                f"Total: {self._money(subtotal + tax)}",
                "",
                "Thank you for your order!",
            ]
        )
        return "\n".join(lines)

    def _subtotal(self):
        return sum(item["quantity"] * item["unit_price"] for item in self.cart)

    @staticmethod
    def _money(amount):
        return f"Rs. {amount:,.0f}"


if __name__ == "__main__":
    app = CoffeeApp()
    app.mainloop()
