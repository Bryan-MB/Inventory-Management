# Import Modules
import sqlite3
from tkinter import *
from tkinter.ttk import *
from tkcalendar import Calendar
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import datetime


# Function to connect to the SQLite database
def connect_db():
    try:
        conn = sqlite3.connect('ramens_inventory.db')
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print("Error connecting to the database:", e)
        return None, None


# Establish a database connection at the beginning
conn, cursor = connect_db()
print('Connection to database established')

# Default database
beverage_data = [
    ('Mineral Water', 0, None, '1 box', None, '1 botol'),
    ('Ocha', 0, None, '1 box', None, '1 botol'),
    ('Teh Botol', 0, None, '1 box (12)', None, '1 botol'),
    ('Pokka Green Tea', 0, None, '1 box', None, '1 botol'),
    ('Bir Bintang', 0, None, '1 kerat', None, '1 botol'),
    ('Air Galon', 0, None, '1 gallon', None, '1 gallon'),
]
foodItems_data = [
    ('Noodles', 0, 32000, '1 pack (14 pcs)', 2285, '1 pcs'),
    ('Chicken Chasyu', 0, 19500, '1 roll (16 slices)', 1218.75, '1 slice'),
    ('Chicken Katsu', 0, 8227, '1 serving', None, '1 serving'),
    ('Gyoza', 0, 26009, '150 pcs', 173, '1 pcs'),
    ('Karage', 0, 122347, '30-35 pcs', 4078, '1 serving'),
    ('Naruto', 0, 28000, '1 roll (55 slices)', 1100, '2 slices'),
    ('Tantan', 0, 12000, '1 bag (500 g)', 360, '15 grams'),
    ('Tamago (Omega)', 0, 2500, '1 pcs', 1250, 'half egg'),
    ('Base', 0, 132347.50, '1 stock pot', 2000, '1 x 90ml ledel'),
    ('Kaldu', 0, None, None, None, '1 x 90ml ledel'),
    ('Sambel', 0, None, None, None, 'd?'),
    ('Cheese Powder', 0, 190000, '1 kg', 5700, '30 g'),
    ('Kare', 0, None, None, None, None),
    ('Kari', 0, None, None, None, None),
    ('Kulit Pangsit', 0, 8000, '1 pack (100 pcs)', 50, '1 pcs'),
    ('Nasi', 0, None, None, None, None)
]
rawMaterials_data = [
    ('Ayam Utuh', 0, 39000, '1 ekor (1 kg)', 39, '10 gr'),
    ('Ayam Cincang', 0, 51000, '1 kg', 51, '10 gr'),
    ('Sapi Cincang', 0, 110000, '1 kg', 110, '10 gr'),
    ('Bawang Daun', 0, 20000, '1 kg', 20, '10 gr'),
    ('Bawang Putih', 0, 30000, '1 kg', 30, '10 gr'),
    ('Bawang Bombai', 0, 26000, '1 kg', 26, '10 gr'),
    ('Cabe Kering', 0, 80000, '1 kg', 80, '10 gr'),
    ('Cabe keriting', 0, 32000, '1 kg', 32, '10 gr'),
    ('Cabe Rawit Merah', 0, 60000, '1 kg', 60, '10 gr'),
    ('Daun Ketumbar', 0, 50000, '1 kg', 50, '10 gr'),
    ('Kol', 0, 8500, '1 kg', 8.5, '10 gr'),
    ('Pakcoy', 0, 13000, '1 kg', 13, '10 gr'),
    ('Toge', 0, 11000, '1 kg', 11, '10 gr'),
    ('Tomat', 0, 12000, '1 kg', 12, '10 gr'),
    ('Wortel', 0, 12000, '1 kg', 12, '10 gr'),
    ('Jahe', 0, 24000, '1 kg', 24, '10 gr'),
    ('Jagung', 0, 32500, '1 kg', 33, '10 gr'),
    ('Jamur Kuping', 0, 16000, '1 kg', 16, '10 gr'),
    ('Kentang', 0, 18000, '1 kg', 18, '10 gr')
]
miscellaneous_data = [
    ('Chilli Powder', 0, 10000, '100 gr', 100, '10 gr'),
    ('Chilli Oil', 0, 17900, '1 botol (135 ml)', None, None),
    ('Cuka', 0, None, '1 botol', None, None),
    ('Garam', 0, 10000, '1 kg', 11, '10 gr'),
    ('Merica', 0, 21000, '1 kg', 21, '10 gr'),
    ('Gula', 0, None, None, None, None),
    ('Ajinomoto', 0, 40000, '1 kg', 40, '10 gr'),
    ('Chicken Powder', 0, 85000, '1 pack', 850, '10 gr'),
    ('Marumoto', 0, 127000, '1 pack', 63500, '1/2 pack'),
    ('Max Creamer', 0, 30000, '1 pack', None, None),
    ('Maizena', 0, None, '1 pack', None, None),
    ('Mozarella', 0, None, None, None, None),
    ('Tepung Sagu', 0, None, '1 pack', None, None),
    ('Tepung roti', 0, 22000, '1 pack', None, None),
    ('Minyak Wijen', 0, 35000, '600 ml', 583, '10 ml'),
    ('Minyak goreng (SANIA)', 0, 37500, None, None, None),
    ('Minyak goreng (Bimoli)', 0, 39500, '2 L', None, None),
    ('Fresh Milk', 0, None, None, None, None),
    ('Kikoman', 0, 90000, '1 botol', 57, '1 ml'),
    ('Beras', 0, None, None, None, None),
    ('Beras Ketan', 0, None, None, None, None),
    ('Tabung Gas', 0, None, '1 tabung', None, None)
]
print('Default databases created')

# Menu
menu = {
    "RAMEN": {
        "Sapporo Ramen": 45000,
        "Chicken Chasu Ramen": 38000,
        "Tantanmen Ramen": 38000,
        "Cheese Ramen": 38000,
        "Chicken Katsu Ramen": 40000,
    },
    "LIGHT SNACK": {
        "Gyoza Age": 25000,
        "Gyoza Yaki": 20000,
        "Chicken Karage": 25000,
        "Chicken Karage Mentai": 30000,
    },
    "ADDITIONAL": {
        "Telor": 5000,
        "Mie": 7500,
        "Chasu": 12000,
        "Naruto": 5000,
        "Tantan": 7500,
    },
    "BEVERAGE": {
        "Mineral Water": 6000,
        "Ocha Refill": 7500,
        "Teh Botol": 6000,
        "Pokka Green Tea": 15000,
        "Beer Bintang": 40000,
    },
}

# Date variables
selected_date = None
start_date = None
end_date = None


# Function to create the tables for each category
def create_tables():
    # Create tables for each category: Beverage, FoodItems, RawMaterials, Miscellaneous
    try:
        # Check if data exists in the Beverage table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name ='Beverage'")
        table_exists = cursor.fetchone()
        print('Beverage table check')

        if table_exists is None:
            # Create a table for Beverage if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Beverage (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ItemName TEXT,
                    Quantity FLOAT,
                    BuyCost FLOAT,
                    PurchaseUnit TEXT,
                    CostPerPiece FLOAT,
                    ServingUnit TEXT
                )
            ''')
            print('Beverage table created')

            # Insert data into the Beverage table
            cursor.executemany('''
                INSERT INTO Beverage (ItemName, Quantity, BuyCost, PurchaseUnit, CostPerPiece, ServingUnit)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', beverage_data)
            print('Beverage table inserted')

        # Check if data exists in the FoodItems table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='FoodItems'")
        table_exists = cursor.fetchone()
        print('FoodItems table check')

        if table_exists is None:
            # Create a table for FoodItems
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS FoodItems (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ItemName TEXT,
                    Quantity FLOAT,
                    BuyCost FLOAT,
                    PurchaseUnit TEXT,
                    CostPerPiece FLOAT,
                    ServingUnit TEXT
                )
            ''')
            print('FoodItems table created')

            # Insert data into the FoodItems table
            cursor.executemany('''
                INSERT INTO FoodItems (ItemName, Quantity, BuyCost, PurchaseUnit, CostPerPiece, ServingUnit)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', foodItems_data)
            print('FoodItems table inserted')

        # Check if data exists in the RawMaterials table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='RawMaterials'")
        table_exists = cursor.fetchone()
        print('RawMaterials table check')

        if table_exists is None:
            # Create a table for RawMaterials
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS RawMaterials (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ItemName TEXT,
                    Quantity FLOAT,
                    BuyCost FLOAT,
                    PurchaseUnit TEXT,
                    CostPerPiece FLOAT,
                    ServingUnit TEXT
                )
            ''')
            print('RawMaterials table created')

            # Insert data into the RawMaterials table
            cursor.executemany('''
                INSERT INTO RawMaterials (ItemName, Quantity, BuyCost, PurchaseUnit, CostPerPiece, ServingUnit)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', rawMaterials_data)
            print('RawMaterials table inserted')

        # Check if data exists in the Miscellaneous table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Miscellaneous'")
        table_exists = cursor.fetchone()
        print('Miscellaneous table check')

        if table_exists is None:
            # Create a table for Miscellaneous
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Miscellaneous (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ItemName TEXT,
                    Quantity FLOAT,
                    BuyCost FLOAT,
                    PurchaseUnit TEXT,
                    CostPerPiece FLOAT,
                    ServingUnit TEXT
                )
            ''')
            print('Miscellaneous table created')

            # Insert data into the Miscellaneous table
            cursor.executemany('''
                INSERT INTO Miscellaneous (ItemName, Quantity, BuyCost, PurchaseUnit, CostPerPiece, ServingUnit)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', miscellaneous_data)
            print('Miscellaneous table inserted')

        # Commit the changes to the database
        conn.commit()

    except sqlite3.Error as e:
        print("Error inserting data: ", e)


# Creates the tables for the database
create_tables()
print('Tables created')


# Function to view and modify inventory
def view_modify_inventory():
    # Create a new window to display inventory
    inventory_window = Toplevel(master)
    inventory_window.title("View/Modify Inventory")
    inventory_window.geometry("1000x500")

    # Create a layout on the window
    inventory_window.columnconfigure(0, weight=1)
    inventory_window.columnconfigure(1, weight=1)
    inventory_window.columnconfigure(2, weight=1)
    inventory_window.columnconfigure(3, weight=1)
    inventory_window.rowconfigure(0, weight=1)
    inventory_window.rowconfigure(1, weight=5)
    inventory_window.rowconfigure(2, weight=5)

    # Create top label and combobox
    Label(inventory_window, text='Select Table: ').grid(column=1, row=0, sticky="e")
    combo_var = StringVar()
    combo = Combobox(inventory_window, textvariable=combo_var, justify='center', state='readonly')
    combo['values'] = ("Beverage", "FoodItems", "RawMaterials", "Miscellaneous")
    combo.set("-- category --")
    combo.bind("<<ComboboxSelected>>", lambda event: display_table(combo_var.get(), inventory_window))
    combo.grid(column=2, row=0, sticky="w")


# Function to display selected table
def display_table(selected_table, inventory_window):
    # Fetch selected table
    cursor.execute(f"PRAGMA table_info({selected_table});")
    column_info = cursor.fetchall()
    column_names = [info[1] for info in column_info]
    cursor.execute(f"SELECT * FROM {selected_table};")
    table_content = cursor.fetchall()

    # Create a frame to hold the Treeview and scrollbar
    table_frame = Frame(inventory_window)
    table_frame.grid(column=0, row=1, columnspan=4, sticky="nsew")

    # Create a Treeview widget to display the table content
    table = Treeview(table_frame, columns=column_names, show="headings")

    # Add column headings
    for column_name in column_names:
        table.heading(column_name, text=column_name, anchor="center")
        table.column(column_name, minwidth=0, width=100)

    # Add data rows
    for row in table_content:
        table.insert("", "end", values=row)

    # Create a vertical scrollbar for the Treeview
    vsb = Scrollbar(table_frame, orient="vertical", command=table.yview)
    vsb.grid(row=0, column=1, sticky="ns")
    table.configure(yscrollcommand=vsb.set)

    # Place the Treeview and scrollbar inside the frame
    table.grid(column=0, row=0, sticky="nsew")

    # Configure weights for proper resizing
    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    # Create modification menu: title, ID, and Quantity
    modify_frame = Frame(inventory_window)
    modify_frame.grid(column=0, row=2, columnspan=2, sticky="nsew")
    Label(modify_frame, text='Modify Quantity').grid(column=0, row=0, sticky="nsew", pady=20, padx=20)
    Label(modify_frame, text='ID: ').grid(column=0, row=1, sticky="sw", padx=20)
    id_entry = Entry(modify_frame)
    id_entry.grid(column=2, row=1)
    Label(modify_frame, text='Quantity: ').grid(column=0, row=2, sticky="sw", padx=20)
    quantity_entry = Entry(modify_frame)
    quantity_entry.grid(column=2, row=2)

    # Create the Add button
    add_button = Button(modify_frame, text="Add",
                        command=lambda: modify_quantity('Add', selected_table, id_entry,
                                                        quantity_entry, inventory_window))
    add_button.grid(column=0, row=3, pady=20)

    # Create the Remove button
    remove_button = Button(modify_frame, text="Remove",
                           command=lambda: modify_quantity('Remove', selected_table, id_entry,
                                                           quantity_entry, inventory_window))
    remove_button.grid(column=1, row=3, pady=20)

    # Create the Change button
    change_button = Button(modify_frame, text="Change",
                           command=lambda: modify_quantity('Change', selected_table, id_entry,
                                                           quantity_entry, inventory_window))
    change_button.grid(column=2, row=3, pady=20)

    # Create the Add New Item button
    new_button = Button(inventory_window, text="Add New Item",
                        command=lambda: new_item(selected_table, inventory_window))
    new_button.grid(column=2, row=2, sticky="n", pady=65)

    # Create the Remove Existing Item button
    remove_button = Button(inventory_window, text="Remove Existing Item",
                           command=lambda: remove_item(selected_table, inventory_window))
    remove_button.grid(column=3, row=2, sticky="n", pady=65)


# Function to modify the quantity in the SQL tables
def modify_quantity(mod, selected_table, id_entry, quantity_entry, inventory_window):
    # Store user input into variables
    product_id = id_entry.get()
    quantity_change = float(quantity_entry.get())

    # Select table and data to modify
    cursor.execute(f"SELECT ID, Quantity FROM {selected_table} WHERE ID = ?", (product_id,))
    product_data = cursor.fetchone()

    # Modify the data according to the selected button
    if product_data:
        current_quantity = product_data[1]
        if mod == 'Add':
            new_quantity = current_quantity + quantity_change
        elif mod == 'Remove':
            new_quantity = current_quantity - quantity_change
        else:
            new_quantity = quantity_change

        # Update the table
        try:
            cursor.execute(f'UPDATE {selected_table} SET Quantity = ? WHERE ID = ?', (new_quantity, product_id))
            conn.commit()
            # Display updated table
            display_table(selected_table, inventory_window)
        except sqlite3.Error as e:
            print("Error updating data: ", e)
    else:
        # Handle errors when user inputs an ID that does not exist in the table
        print("Product not found")


# Function to add a new item to the table
def new_item(selected_table, inventory_window):
    # Create a new window for the user to input data of new item
    new_item_window = Toplevel(inventory_window)
    new_item_window.title("Add New Item")

    # Create labels and entry widgets for each column
    column_labels = ["ItemName", "Quantity", "BuyCost", "PurchaseUnit", "CostPerPiece", "ServingUnit"]
    entry_widgets = {}

    for i, column_label in enumerate(column_labels):
        Label(new_item_window, text=column_label).grid(row=i, column=0, sticky="w", padx=5)
        entry_widgets[column_label] = Entry(new_item_window)
        entry_widgets[column_label].grid(row=i, column=1, pady=20)

        # Function to insert the new item into the selected table
        def insert_new_item():
            values = [entry_widgets[column_label].get() for column_label in column_labels]
            cursor.execute(
                f"INSERT INTO {selected_table} (ItemName, Quantity, BuyCost, PurchaseUnit, "
                f"CostPerPiece, ServingUnit) VALUES (?, ?, ?, ?, ?, ?)",
                values)
            conn.commit()
            new_item_window.destroy()
            display_table(selected_table, inventory_window)  # Refresh the table after adding a new item

        # Create a button to submit the new item
        submit_button = Button(new_item_window, text="Submit", command=insert_new_item)
        submit_button.grid(row=len(column_labels), column=0, columnspan=2)


# Function to remove existing item from the table
def remove_item(selected_table, inventory_window):
    # Create a new window for the user to remove an existing item
    remove_item_window = Toplevel(inventory_window)
    remove_item_window.title("Remove Existing Item")

    # Create a label and entry box for the user to input
    Label(remove_item_window, text="Enter ID to remove: ").grid(column=0, row=0)
    id_entry = Entry(remove_item_window)
    id_entry.grid(column=1, row=0)

    # Function remove the item with the given ID from the table
    def delete_item():
        product_id = id_entry.get()
        if product_id:
            try:
                cursor.execute(f"DELETE FROM {selected_table} WHERE ID = ?", (product_id,))
                conn.commit()
                remove_item_window.destroy()
                display_table(selected_table, inventory_window)  # Refresh the table after removing an item
            except sqlite3.Error as e:
                print("Error removing item: ", e)
        else:
            print("Please enter a valid ID.")

    # Create a button to submit the ID for removal
    submit_button = Button(remove_item_window, text="Remove", command=delete_item)
    submit_button.grid(row=1, column=0, columnspan=2)


# Function to calculate inventory usage
def calculate_usage():
    global selected_date

    # Create a new window to display the menu
    usage_window = Toplevel(master)
    usage_window.title("Calculate Usage")

    # Create the list and spinboxes
    row = 0
    spinbox_vars = {}
    for category, items in menu.items():
        Label(usage_window, text=category).grid(row=row, column=0, columnspan=3)
        row += 1
        for item, _ in items.items():
            Label(usage_window, text=item).grid(row=row, column=0, sticky="w")
            spinbox_var = StringVar()
            Spinbox(usage_window, from_=0, to=100, textvariable=spinbox_var, width=5).grid(row=row, column=2,
                                                                                           sticky="e")
            spinbox_vars[(category, item)] = spinbox_var
            row += 1
        Label(usage_window, text="").grid(row=row, column=0)  # Add spacing between categories
        row += 1

    # Create a button to select the date
    (Button(usage_window, text="Select Date", command=lambda: open_calendar(usage_window, row))
     .grid(row=row, column=0, columnspan=3))
    row += 1

    # Create a button to display the summary of orders
    (Button(usage_window, text="Confirm Orders", command=lambda: display_summary(usage_window, spinbox_vars))
     .grid(row=row, column=0, columnspan=3, pady=20))


# Function to open the calendar pop-up
def open_calendar(usage_window, row):
    global selected_date

    # Create a new window for the calendar
    cal_window = Toplevel(usage_window)
    cal_window.title("Calendar")

    # Create the calendar
    cal = Calendar(cal_window, selectmode='day', date_pattern='dd/mm/yyyy')
    cal.grid(row=0, column=0)

    # Function to confirm the date
    def confirm_date(date):
        global selected_date
        selected_date = date
        Label(usage_window, text=f"{selected_date}").grid(row=row, column=0, columnspan=3, sticky="n")
        cal_window.destroy()

    # Create a button to confirm the selected date
    Button(cal_window, text="Confirm Date", command=lambda: confirm_date(cal.get_date())).grid(row=1, column=0)


# Function to create a new window containing the summary of orders
def display_summary(usage_window, spinbox_vars):
    # Check if any spinbox has no value
    if all(spinbox_var.get() == "" for spinbox_var in spinbox_vars.values()):
        error_window = Toplevel(usage_window)
        error_window.title("Error")
        Label(error_window, text="Error: No Orders Added!").pack()
        return

    # Create a new window for the summary
    summary_window = Toplevel(usage_window)
    summary_window.title("Order Summary")
    subtotal = 0
    tax_rate = 0.10  # 10% tax rate

    row = 0
    Label(summary_window, text="Order Summary").grid(row=row, column=0, sticky="w")
    row += 1
    Label(summary_window, text=f"Date: {selected_date}").grid(row=row, column=0, sticky="w")
    row += 1
    Label(summary_window, text="").grid(row=row, column=0)
    row += 1

    # Create the list of summary
    for category, items in menu.items():
        for item, price in items.items():
            spinbox_var = spinbox_vars[(category, item)]
            quantity_spinbox = spinbox_var.get()
            if quantity_spinbox:
                quantity_ordered = int(quantity_spinbox)
                total_price = quantity_ordered * price
                subtotal += total_price

                # Format total_price with commas every three digits from the back
                formatted_total_price = "{:,}".format(total_price)

                # Create a label for the order
                Label(summary_window, text=f"{quantity_ordered} {item}").grid(row=row, column=0, sticky="w")
                Label(summary_window, text=formatted_total_price).grid(row=row, column=1, sticky="e")
                row += 1

    # Calculate tax and total
    tax = subtotal * tax_rate
    total = subtotal + tax

    # Format subtotal, tax, and total with commas
    formatted_subtotal = "{:,}".format(subtotal)
    formatted_tax = "{:,}".format(tax)
    formatted_total = "{:,}".format(total)

    # Display subtotal, tax, and total on the receipt
    row += 1
    Label(summary_window, text="").grid(row=row, column=0)
    row += 1
    Label(summary_window, text="Subtotal").grid(row=row, column=0, sticky="w")
    Label(summary_window, text=formatted_subtotal).grid(row=row, column=1, sticky="e")
    row += 1
    Label(summary_window, text="Tax (10%)").grid(row=row, column=0, sticky="w")
    Label(summary_window, text=formatted_tax).grid(row=row, column=1, sticky="e")
    row += 1
    Label(summary_window, text="Total").grid(row=row, column=0, sticky="w")
    Label(summary_window, text=formatted_total).grid(row=row, column=1, sticky="e")

    # Create a button to confirm the summary and record it in the SQL table
    row += 1
    Label(summary_window, text="").grid(row=row, column=0)
    row += 1
    (Button(summary_window, text="Submit", command=lambda: record(spinbox_vars, summary_window))
     .grid(row=row, column=0, columnspan=3, pady=8))


# Function to record orders
def record(spinbox_vars, summary_window):
    global selected_date

    # Check if a valid date is selected
    if selected_date is None:
        print("Please select a date.")
        return

    # Create a list to store the order details
    order_details = []

    for category, items in menu.items():
        for item, _ in items.items():
            spinbox_var = spinbox_vars[(category, item)]
            quantity_spinbox = spinbox_var.get()
            if quantity_spinbox:
                quantity_ordered = int(quantity_spinbox)
                if quantity_ordered > 0:
                    order_details.append((category, item, quantity_ordered))

    # Check if any orders are placed
    if not order_details:
        return

    try:
        # Check if the DailyOrders table already exists
        cursor.execute("SELECT name from sqlite_master WHERE type='table' AND name ='DailyOrders'")
        table_exists = cursor.fetchone()
        print("DailyOrders table check")

        if table_exists is None:
            # Create a table to store daily orders if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS DailyOrders (
                    OrderDate DATE,
                    Category TEXT,
                    ItemName TEXT,
                    Quantity INTEGER
                )
            ''')
            print("DailyOrders table created")

        # Insert the orders into the DailyOrders table
        for category, item, quantity in order_details:
            cursor.execute('''
                INSERT INTO DailyOrders (OrderDate, Category, ItemName, Quantity)
                VALUES (?, ?, ?, ?)
            ''', (selected_date, category, item, quantity))
            print("DailyOrders table inserted")

        # Commit the changes to the database
        conn.commit()
        print("Orders recorded")

        # Update the table of ingredients based on the orders

        summary_window.destroy()

    except sqlite3.Error as e:
        print("Error recording orders: ", e)


# Function to display the statistics
def statistics():
    # Create a new window to document monthly orders
    stat_window = Toplevel(master)
    stat_window.title("Statistics")
    stat_window.geometry('1000x800')

    # Create a layout on the window
    stat_window.columnconfigure(0, weight=1)
    stat_window.columnconfigure(1, weight=1)
    stat_window.rowconfigure(0, weight=1)
    stat_window.rowconfigure(1, weight=5)
    stat_window.rowconfigure(2, weight=3)
    stat_window.rowconfigure(3, weight=1)

    # Create a frame to hold the start date and end date labels and buttons
    date_frame = Frame(stat_window)
    date_frame.grid(column=0, row=0, sticky='nsew')
    date_frame.columnconfigure(0, weight=1)
    date_frame.columnconfigure(1, weight=1)
    date_frame.columnconfigure(2, weight=1)
    date_frame.columnconfigure(3, weight=1)
    date_frame.columnconfigure(4, weight=1)

    # Create start date and end date buttons
    (Button(date_frame, text="Start Date:", command=lambda: stat_calendar(date_frame, "start_date"))
     .grid(column=0, row=0, sticky='e', pady=10))
    (Button(date_frame, text="End Date:", command=lambda: stat_calendar(date_frame, "end_date"))
     .grid(column=2, row=0, sticky='e', pady=10))

    # Create the "Apply" button to fetch data within the selected time period
    Button(date_frame, text="Apply", command=lambda: fetch_data()).grid(column=4, row=0, sticky='w', pady=10)

    # Function to open the calendar pop-up for the statistics window
    def stat_calendar(date_frame, entry):
        # Create a new window for the calendar
        cal_window = Toplevel(date_frame)
        cal_window.title("Calendar")

        # Create the calendar
        cal = Calendar(cal_window, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.grid(row=0, column=0)

        # Function to confirm the date
        def confirm_date(date, entry):
            if entry == "start_date":
                global start_date
                start_date = date
                Label(date_frame, text=f"{start_date}").grid(column=1, row=0, sticky='w')
            elif entry == "end_date":
                global end_date
                end_date = date
                Label(date_frame, text=f"{end_date}").grid(column=3, row=0, sticky='w')

            cal_window.destroy()

        # Create a button to confirm the selected date
        Button(cal_window, text="Confirm Date", command=lambda: confirm_date(cal.get_date(), entry)).grid(row=1,
                                                                                                          column=0)

    # Function to fetch data
    def fetch_data():
        # Check if both start_date and end_date are selected
        if not (start_date and end_date):
            error_window = Toplevel(stat_window)
            error_window.title("Error")
            Label(error_window, text="Error: Please select both start date and end date!").pack()
            return

        # Fetch data within the selected time period
        query = "SELECT OrderDate, Category, ItemName, Quantity FROM DailyOrders WHERE OrderDate BETWEEN ? AND ?"
        cursor.execute(query, (start_date, end_date))

        # Display the results
        data = cursor.fetchall()
        print(data)
        display_bar(data, stat_window)
        display_line(data, stat_window)
        display_total(data, stat_window)
        # display_finance(data, stat_window)


# Function to display the bar graph of items sold
def display_bar(data, stat_window):
    # Prepare the data
    order_date, categories, item_names, total_quantity = zip(*data)

    # Create the bar graph
    fig, bg = plt.subplots(figsize=(5, 4))
    x = range(len(item_names))
    bg.bar(x, total_quantity, tick_label=item_names)
    bg.set_title("Total Quantity of Each Item Sold")
    bg.set_xlabel("Orders")
    bg.set_ylabel("Quantity Sold")
    bg.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Embed the Matplotlib figure in the stat_window
    bar_graph = FigureCanvasTkAgg(fig, master=stat_window)
    bar_graph.get_tk_widget().grid(row=1, column=0, sticky='nw', padx=30)


# Function to display the bar graph of items sold
def display_line(data, stat_window):
    # Create a dictionary to store total quantity for each category
    category_data = {
        "RAMEN": defaultdict(int),
        "LIGHT SNACK": defaultdict(int),
        "BEVERAGE": defaultdict(int),
        "ADDITIONAL": defaultdict(int)
    }

    # Go through the data and sum the total quantity for each category
    for date_str, category, _, quantity in data:
        day, month, year = map(int, date_str.split('/'))
        date = datetime.datetime(year, month, day)  # Create a datetime object
        category_data[category][date] += quantity

    # Create the line graph
    fig, lg = plt.subplots(figsize=(5, 4))
    lg.set_xlabel("Date")
    lg.set_ylabel("Total Quantity Sold")
    lg.set_title("Total Quantity of Each Category Sold")
    lg.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    line_colors = {
        "RAMEN": "red",
        "LIGHT SNACK": "green",
        "BEVERAGE": "blue",
        "ADDITIONAL": "yellow"
    }

    for category, color in line_colors.items():
        dates = list(category_data[category].keys())
        quantities = list(category_data[category].values())

        # Sort the data by date
        sorted_data = sorted(zip(dates, quantities), key=lambda x: x[0])
        sorted_dates, sorted_quantities = zip(*sorted_data)

        # Create a line for each category
        lg.plot(sorted_dates, sorted_quantities, color=color, label=category)

    # Format the x-axis as dates
    date_format = mdates.DateFormatter('%d/%m/%Y')
    lg.xaxis.set_major_formatter(date_format)
    lg.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Add a legend to the plot
    lg.legend(loc="upper right", fontsize="small")

    # Embed the Matplotlib figure in the stat_window
    line_graph = FigureCanvasTkAgg(fig, master=stat_window)
    line_graph.get_tk_widget().grid(row=1, column=1, sticky='ne', padx=30)


# Function to display the total number of items sold
def display_total(data, stat_window):
    # Create a dictionary to store the total quantity of each category
    sums = {
        "RAMEN": 0,
        "LIGHT SNACK": 0,
        "BEVERAGE": 0,
        "ADDITIONAL": 0
    }

    # Calculate the sum
    for line in data:
        quantity = int(line[3])
        if line[1] in sums:
            sums[line[1]] += quantity

    # Create a frame to hold the labels
    total_frame = Frame(stat_window)
    total_frame.grid(column=0, row=2, sticky='nsew')
    row = 0
    for category, sum_quantity in sums.items():
        Label(total_frame, text=f"Total number of {category} sold: {sum_quantity}").grid(column=0, row=row, sticky='w', padx=30, pady=10)
        row += 1


# Function to display the finances
def display_finance(data, stat_window):
    print("WIP")


# Create the main window
master = Tk()
master.geometry('1000x800')
master.title("Ramens Inventory Management")
Label(master, text="Ramens Inventory Management").pack()

# Create the buttons
view_button = Button(master, text="View/Modify Inventory", command=view_modify_inventory)
view_button.pack(fill=BOTH, expand=True)
calculate_button = Button(master, text="Calculate Usage", command=calculate_usage)
calculate_button.pack(fill=BOTH, expand=True)
statistics_button = Button(master, text="Display Sales Statistics", command=statistics)
statistics_button.pack(fill=BOTH, expand=True)

# Start the main event loop
master.mainloop()

# Close the database connection when the application exits
conn.close()
