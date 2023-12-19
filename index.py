import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Constants for weight limits and prices
WEIGHT_LIMITS = {'C': (24.9, 25.1), 'G': (49.9, 50.1), 'S': (49.9, 50.1)}
PRICE_PER_SACK = {'C': 3, 'G': 2, 'S': 2}
SPECIAL_PACK_PRICE = 10

# Function to validate sack weight
def validate_weight(content, weight):
    min_weight, max_weight = WEIGHT_LIMITS[content]
    return min_weight < weight < max_weight

# Function to validate and process a single sack (Task 1)
def process_sack():
    content = content_var.get().upper()
    try:
        weight = float(weight_var.get())
    except ValueError:
        error_label_task1.config(text="Invalid weight. Please enter a number.")
        return

    if content not in WEIGHT_LIMITS:
        error_label_task1.config(text="Invalid content. Use C, G, or S.")
        return

    if validate_weight(content, weight):
        result_label_task1.config(text=f"Accepted: {content} sack weighing {weight} kg")
        error_label_task1.config(text="")
    else:
        error_label_task1.config(text="Sack weight is out of the valid range.")

# Function to process the order and calculate the price (Tasks 2 and 3)
def process_order():
    total_weight = 0
    rejected_sacks = 0
    order_count = {'C': 0, 'G': 0, 'S': 0}

    for content_type in ['C', 'G', 'S']:
        num_sacks = simpledialog.askinteger("Input", f"Enter number of {content_type} sacks:", parent=root)
        if num_sacks is None:
            continue

        for _ in range(num_sacks):
            weight = simpledialog.askfloat("Input", f"Enter weight for a {content_type} sack (kg):", parent=root)
            if weight is None:
                continue

            if validate_weight(content_type, weight):
                total_weight += weight
                order_count[content_type] += 1
            else:
                rejected_sacks += 1

    # Calculate regular price
    regular_price = sum(order_count[ct] * PRICE_PER_SACK[ct] for ct in order_count)

    # Calculate discount
    special_packs = min(order_count['C'], order_count['S'] // 2, order_count['G'] // 2)
    discount_price = regular_price - special_packs * (PRICE_PER_SACK['C'] + 2 * PRICE_PER_SACK['S'] + 2 * PRICE_PER_SACK['G'] - SPECIAL_PACK_PRICE)
    savings = regular_price - discount_price

    # Display order summary
    messagebox.showinfo("Order Summary",
                        f"Total weight of order: {total_weight} kg\n"
                        f"Rejected sacks: {rejected_sacks}\n"
                        f"Regular price: ${regular_price}\n"
                        f"Discounted price: ${discount_price}\n"
                        f"Savings: ${savings}")

# Function to create Task 1 tab
def create_task1_tab(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Task 1")

    global content_var, weight_var, error_label_task1, result_label_task1
    content_var = tk.StringVar()
    weight_var = tk.StringVar()

    ttk.Label(tab, text="Content (C/G/S):").grid(row=0, column=0, padx=10, pady=10)
    ttk.Entry(tab, textvariable=content_var).grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(tab, text="Weight (kg):").grid(row=1, column=0, padx=10, pady=10)
    ttk.Entry(tab, textvariable=weight_var).grid(row=1, column=1, padx=10, pady=10)

    ttk.Button(tab, text="Check Sack", command=process_sack).grid(row=2, column=0, columnspan=2, pady=10)

    error_label_task1 = ttk.Label(tab, text="", foreground="red")
    error_label_task1.grid(row=3, column=0, columnspan=2)

    result_label_task1 = ttk.Label(tab, text="")
    result_label_task1.grid(row=4, column=0, columnspan=2)

# Function to create Task 2 and 3 tab
def create_task23_tab(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Task 2 & 3")

    ttk.Button(tab, text="Process Order", command=process_order).grid(row=0, column=0, padx=10, pady=10)

# Main application setup
root = tk.Tk()
root.title("Building Materials Delivery Service")
notebook = ttk.Notebook(root)

create_task1_tab(notebook)
create_task23_tab(notebook)

notebook.pack(expand=True, fill="both")

root.mainloop()