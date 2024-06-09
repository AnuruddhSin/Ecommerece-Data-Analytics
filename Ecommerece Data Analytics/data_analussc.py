import webbrowser

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
import folium
from folium.plugins import HeatMap
from datetime import datetime

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load data from CSV files
ecommerce_data = pd.read_csv("ecommerce_data.csv", encoding='ISO-8859-1')
state_lat_lon_data = pd.read_csv("us_state_long_lat_codes.csv")

# Join the two dataframes on the state
combined_data = ecommerce_data.merge(state_lat_lon_data, left_on="customer_state", right_on="state", how="left")

# Create a tkinter GUI
root = Tk()
root.title("E-commerce Data Analysis Dashboard")

# Create a notebook to organize different sections
notebook = ttk.Notebook(root)
notebook.pack()

# Create frames for different sections
sales_frame = ttk.Frame(notebook)
profit_frame = ttk.Frame(notebook)
quantity_frame = ttk.Frame(notebook)
profit_margin_frame = ttk.Frame(notebook)
sales_by_category_frame = ttk.Frame(notebook)
top_5_products_frame = ttk.Frame(notebook)
map_frame = ttk.Frame(notebook)
profit_states_frame = ttk.Frame(notebook)
profit_trends_frame = ttk.Frame(notebook)

notebook.add(sales_frame, text="YTD Sales")
notebook.add(profit_frame, text="YTD Profit")
notebook.add(quantity_frame, text="YTD Quantity")
notebook.add(profit_margin_frame, text="YTD Profit Margin")
notebook.add(sales_by_category_frame, text="Sales by Category")
notebook.add(top_5_products_frame, text="Top 5 Products")
notebook.add(map_frame, text="Profit by State Map")
notebook.add(profit_states_frame, text="High/Low Profit States")
notebook.add(profit_trends_frame, text="Profit Trends Over Time")

# Function for data analysis
def analyze_data():

    # YTD Sales
    ytd_sales = combined_data.groupby("customer_country")["sales_per_order"].sum() / 1e6

    # Create and display the YTD Sales chart for the sales_frame
    plt.figure(figsize=(10, 5))
    plt.bar(ytd_sales.index, ytd_sales.values)
    plt.title("YTD Sales (Millions)")
    plt.xlabel("Country")
    plt.ylabel("Sales (Millions)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(plt.gcf(), sales_frame)
    canvas.get_tk_widget().pack()

    # YTD Profit
    ytd_profit = combined_data.groupby("customer_country")["profit_per_order"].sum() / 1e6
    # Create and display the YTD Profit chart for the profit_frame
    plt.figure(figsize=(10, 5))
    plt.bar(ytd_profit.index, ytd_profit.values, color='green')
    plt.title("YTD Profit (Millions)")
    plt.xlabel("Country")
    plt.ylabel("Profit (Millions)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(plt.gcf(), profit_frame)
    canvas.get_tk_widget().pack()

    # YTD Quantity
    ytd_quantity = combined_data.groupby("customer_country")["order_quantity"].sum() / 1e6
    # Create and display the YTD Quantity chart for the quantity_frame
    plt.figure(figsize=(10, 5))
    plt.bar(ytd_quantity.index, ytd_quantity.values, color='purple')
    plt.title("YTD Quantity (Millions)")
    plt.xlabel("Country")
    plt.ylabel("Quantity (Millions)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(plt.gcf(), quantity_frame)
    canvas.get_tk_widget().pack()

    # YTD Profit Margin
    ytd_profit_margin = ytd_profit / ytd_sales
    # Create and display the YTD Profit Margin chart for the profit_margin_frame
    plt.figure(figsize=(10, 5))
    plt.bar(ytd_profit_margin.index, ytd_profit_margin.values, color='orange')
    plt.title("YTD Profit Margin")
    plt.xlabel("Country")
    plt.ylabel("Profit Margin")
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(plt.gcf(), profit_margin_frame)
    canvas.get_tk_widget().pack()

    # Sales by Category
    category_sales = combined_data.groupby("product_name")["sales_per_order"].sum() / 1e6
    # Create and display the Sales by Category chart for the sales_by_category_frame
    plt.figure(figsize=(10, 5))
    plt.bar(category_sales.index, category_sales.values, color='blue')
    plt.title("Sales by Category (Millions)")
    plt.xlabel("Category")
    plt.ylabel("Sales (Millions)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(plt.gcf(), sales_by_category_frame)
    canvas.get_tk_widget().pack()

    # Top 5 Products by YTD Sales
    top_5_products = category_sales.nlargest(5)
    # Create and display the Top 5 Products chart for the top_5_products_frame
    plt.figure(figsize=(10, 5))
    plt.bar(top_5_products.index, top_5_products.values, color='red')
    plt.title("Top 5 Products by YTD Sales (Millions)")
    plt.xlabel("Product")
    plt.ylabel("Sales (Millions)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(plt.gcf(), top_5_products_frame)
    canvas.get_tk_widget().pack()

    # Sales by Region
    ytd_sales_by_region = combined_data.groupby("customer_state")["sales_per_order"].sum() / 1e6
    # Create and display the Sales by Region chart
    plt.figure(figsize=(10, 5))
    plt.bar(ytd_sales_by_region.index, ytd_sales_by_region.values, color='teal')
    plt.title("YTD Sales by Region (Millions)")
    plt.xlabel("State")
    plt.ylabel("Sales (Millions)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(plt.gcf(), quantity_frame)  # Reuse quantity_frame
    canvas.get_tk_widget().pack()

    # Bottom 5 Products by YTD Sales
    bottom_5_products = category_sales.nsmallest(5)
    # Create and display the Bottom 5 Products chart for the sales_by_category_frame
    plt.figure(figsize=(10, 5))
    plt.bar(bottom_5_products.index, bottom_5_products.values, color='pink')
    plt.title("Bottom 5 Products by YTD Sales (Millions)")
    plt.xlabel("Product")
    plt.ylabel("Sales (Millions)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(plt.gcf(), sales_by_category_frame)
    canvas.get_tk_widget().pack()

    # YTD Sales by Shipping Type
    sales_by_shipping_type = combined_data.groupby("shipping_type")["sales_per_order"].sum() / 1e6
    # Create and display the YTD Sales by Shipping Type chart
    plt.figure(figsize=(10, 5))
    plt.pie(sales_by_shipping_type, labels=sales_by_shipping_type.index, autopct='%1.1f%%', colors=['gold', 'lightcoral', 'lightskyblue'])
    plt.title("YTD Sales by Shipping Type (Millions)")
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(plt.gcf(), sales_frame)  # Reuse sales_frame
    canvas.get_tk_widget().pack()

    # High Profit and Low Profit States for the Current Year
    current_year = datetime.now().year
    ytd_profit_by_state = combined_data[combined_data['order_year'] == current_year].groupby("customer_state")[
                              "profit_per_order"].sum() / 1e6
    high_profit_states = ytd_profit_by_state.nlargest(5)
    low_profit_states = ytd_profit_by_state.nsmallest(5)

    # Create and display the High Profit and Low Profit States tables in profit_states_frame
    high_profit_label = Label(profit_states_frame, text="High Profit States")
    high_profit_label.pack()
    high_profit_table = ttk.Treeview(profit_states_frame, columns=("State", "Profit (Millions)"), show="headings")
    high_profit_table.heading("State", text="State")
    high_profit_table.heading("Profit (Millions)", text="Profit (Millions)")
    high_profit_table.pack()
    for state, profit in high_profit_states.iteritems():
        high_profit_table.insert("", "end", values=(state, profit))

    low_profit_label = Label(profit_states_frame, text="Low Profit States")
    low_profit_label.pack()
    low_profit_table = ttk.Treeview(profit_states_frame, columns=("State", "Profit (Millions)"), show="headings")
    low_profit_table.heading("State", text="State")
    low_profit_table.heading("Profit (Millions)", text="Profit (Millions)")
    low_profit_table.pack()
    for state, profit in low_profit_states.iteritems():
        low_profit_table.insert("", "end", values=(state, profit))

    # Profit Trends Over Time
    profit_trends = combined_data.groupby("order_year")["profit_per_order"].sum() / 1e6
    # Create and display the Profit Trends Over Time chart for the profit_trends_frame
    plt.figure(figsize=(10, 5))
    plt.plot(profit_trends.index, profit_trends.values, marker='o', color='purple')
    plt.title("Profit Trends Over Time (Millions)")
    plt.xlabel("Year")
    plt.ylabel("Profit (Millions)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(plt.gcf(), profit_trends_frame)
    canvas.get_tk_widget().pack()


# Create and configure GUI elements
analyze_button = Button(root, text="Analyze Data", command=analyze_data)
analyze_button.pack()

# Function to create the profit by state map
def create_profit_map():
    state_profit = combined_data.groupby("customer_state")["profit_per_order"].sum()
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)  # Set the initial map location and zoom
    HeatMap(data=state_profit, name="Profit Heatmap").add_to(m)  # Create a heatmap layer
    folium.LayerControl().add_to(m)  # Add layer control
    m.save("profit_map.html")  # Save the map to an HTML file
    webbrowser.open("profit_map.html")  # Open the map in the default web browser

# Add a button to create and view the profit map
profit_map_button = Button(map_frame, text="View Profit by State Map", command=create_profit_map)
profit_map_button.pack()

root.mainloop()
